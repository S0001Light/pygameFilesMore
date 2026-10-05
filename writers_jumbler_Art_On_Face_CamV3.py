from pathlib import Path
from PIL import Image
import cv2
import mediapipe as mp
import pygame
from pygame.locals import *
import sys
import datetime
import random
import math
import urllib.request

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
GRID_X, GRID_Y = 405, 20
GRID_WIDTH = GRID_HEIGHT = 600
ROWS = COLS = 30
CAMERA_INDEX = 0
FPS = 60
MAX_FACES = 6
TRACK_DISTANCE = 130
TRACK_TIMEOUT = 25

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, 32)
pygame.display.set_caption("Writers Jumbler - landmark multi-face art")
clock = pygame.time.Clock()


def open_camera(index):
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(index)
    else:
        cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


camera = open_camera(CAMERA_INDEX)
if not camera.isOpened():
    print("Warning: webcam unavailable.")

# MediaPipe removed the legacy mp.solutions API from current releases.
# This program uses the supported MediaPipe Tasks FaceLandmarker API.
MODEL_FILENAME = "face_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
MODEL_PATH = Path(__file__).resolve().with_name(MODEL_FILENAME)


def ensure_face_model():
    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 100000:
        return
    print("Downloading MediaPipe face-landmark model...")
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    except Exception as error:
        raise RuntimeError(
            "Could not download face_landmarker.task. Download the official "
            "MediaPipe Face Landmarker model and place it beside this script. "
            f"Original error: {error}"
        ) from error


ensure_face_model()
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

landmarker_options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=MAX_FACES,
    min_face_detection_confidence=0.50,
    min_face_presence_confidence=0.50,
    min_tracking_confidence=0.50,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
)
face_landmarker = FaceLandmarker.create_from_options(landmarker_options)

# MediaPipe face-oval landmark order.
FACE_OVAL = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109,
]

fg_color = (0, 0, 0)
bg_color = (0, 0, 0)
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0
last_camera_surface = None
last_rgb_frame = None
frame_number = 0
next_face_id = 1
active_face_id = None

# id -> {center, polygon, bbox, colors, missed}
face_tracks = {}


def blank_artwork():
    return [(255, 255, 255) for _ in range(ROWS * COLS)]


def make_timestamp_filename(ext):
    stamp = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S-%p")
    return f"WritersJumbler_LandmarkFaces_{stamp}.{ext}"


def generate_same_shade_color(color):
    delta = random.randint(-85, 85)
    return tuple(max(0, min(255, value + delta)) for value in color)


def crop_camera_frame(frame):
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    target_ratio = GRID_WIDTH / GRID_HEIGHT
    ratio = w / h
    if ratio > target_ratio:
        crop_w = int(h * target_ratio)
        x = (w - crop_w) // 2
        frame = frame[:, x:x + crop_w]
    elif ratio < target_ratio:
        crop_h = int(w / target_ratio)
        y = (h - crop_h) // 2
        frame = frame[y:y + crop_h, :]
    return cv2.resize(frame, (GRID_WIDTH, GRID_HEIGHT), interpolation=cv2.INTER_LINEAR)


def polygon_center(poly):
    return (
        sum(point[0] for point in poly) / len(poly),
        sum(point[1] for point in poly) / len(poly),
    )


def polygon_bbox(poly):
    xs = [point[0] for point in poly]
    ys = [point[1] for point in poly]
    return min(xs), min(ys), max(xs), max(ys)


def smooth_points(old, new, amount=0.68):
    if not old or len(old) != len(new):
        return new
    return [
        (old[i][0] * amount + new[i][0] * (1.0 - amount),
         old[i][1] * amount + new[i][1] * (1.0 - amount))
        for i in range(len(new))
    ]


def assign_detections(detections):
    """Nearest-center matching gives each visible face its own persistent artwork."""
    global next_face_id, active_face_id

    unmatched_tracks = set(face_tracks.keys())
    assignments = []

    # Largest detections first improves matching when faces overlap.
    detections.sort(
        key=lambda item: (item["bbox"][2] - item["bbox"][0]) *
                         (item["bbox"][3] - item["bbox"][1]),
        reverse=True,
    )

    for detection in detections:
        cx, cy = detection["center"]
        best_id = None
        best_distance = TRACK_DISTANCE
        for track_id in unmatched_tracks:
            tx, ty = face_tracks[track_id]["center"]
            distance = math.hypot(cx - tx, cy - ty)
            if distance < best_distance:
                best_distance = distance
                best_id = track_id

        if best_id is None:
            best_id = next_face_id
            next_face_id += 1
            face_tracks[best_id] = {
                "center": detection["center"],
                "polygon": detection["polygon"],
                "bbox": detection["bbox"],
                "colors": blank_artwork(),
                "missed": 0,
            }
            if active_face_id is None:
                active_face_id = best_id
        else:
            unmatched_tracks.remove(best_id)
            track = face_tracks[best_id]
            detection["polygon"] = smooth_points(track["polygon"], detection["polygon"])
            detection["center"] = polygon_center(detection["polygon"])
            detection["bbox"] = polygon_bbox(detection["polygon"])

        track = face_tracks[best_id]
        track["center"] = detection["center"]
        track["polygon"] = detection["polygon"]
        track["bbox"] = detection["bbox"]
        track["missed"] = 0
        assignments.append(best_id)

    for track_id in list(unmatched_tracks):
        face_tracks[track_id]["missed"] += 1
        if face_tracks[track_id]["missed"] > TRACK_TIMEOUT:
            del face_tracks[track_id]
            if active_face_id == track_id:
                active_face_id = next(iter(face_tracks), None)

    return assignments


def update_camera_and_faces():
    global last_camera_surface, last_rgb_frame, frame_number
    if not camera.isOpened():
        return last_camera_surface

    try:
        ok, frame = camera.read()
    except cv2.error as error:
        print("Temporary webcam error:", error)
        return last_camera_surface
    if not ok or frame is None:
        return last_camera_surface

    frame = crop_camera_frame(frame)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = face_landmarker.detect(mp_image)

    detections = []
    if result.face_landmarks:
        for face in result.face_landmarks:
            polygon = []
            for landmark_index in FACE_OVAL:
                landmark = face[landmark_index]
                polygon.append((
                    max(0.0, min(GRID_WIDTH - 1.0, landmark.x * GRID_WIDTH)),
                    max(0.0, min(GRID_HEIGHT - 1.0, landmark.y * GRID_HEIGHT)),
                ))
            detections.append({
                "polygon": polygon,
                "center": polygon_center(polygon),
                "bbox": polygon_bbox(polygon),
            })

    assign_detections(detections)
    last_rgb_frame = rgb.copy()
    last_camera_surface = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
    frame_number += 1
    return last_camera_surface


def point_inside_polygon(point, polygon):
    # OpenCV handles the face contour test cleanly.
    contour = cv2.UMat if False else None
    import numpy as np
    array = np.array(polygon, dtype=np.float32)
    return cv2.pointPolygonTest(array, point, False) >= 0


def molded_cell_rect(track, row, col, origin_x=0, origin_y=0):
    """Map a grid cell into the landmark-derived face oval."""
    left, top, right, bottom = track["bbox"]
    width = max(1.0, right - left)
    height = max(1.0, bottom - top)
    cell_w = width / COLS
    cell_h = height / ROWS
    center = (left + (col + 0.5) * cell_w, top + (row + 0.5) * cell_h)

    if not point_inside_polygon(center, track["polygon"]):
        return None

    # Sample neighboring points so cells near the landmark boundary shrink naturally.
    samples = [
        center,
        (center[0] - cell_w * 0.42, center[1]),
        (center[0] + cell_w * 0.42, center[1]),
        (center[0], center[1] - cell_h * 0.42),
        (center[0], center[1] + cell_h * 0.42),
    ]
    inside_count = sum(point_inside_polygon(sample, track["polygon"]) for sample in samples)
    scale = max(0.35, inside_count / len(samples))
    draw_w = max(1, int(cell_w * 0.86 * scale))
    draw_h = max(1, int(cell_h * 0.86 * scale))
    return pygame.Rect(
        origin_x + int(center[0] - draw_w / 2),
        origin_y + int(center[1] - draw_h / 2),
        draw_w,
        draw_h,
    )


def visible_track_ids():
    return [track_id for track_id, track in face_tracks.items() if track["missed"] == 0]


def draw_face_artworks(surface, origin_x=0, origin_y=0):
    for track_id in visible_track_ids():
        track = face_tracks[track_id]
        colors = track["colors"]
        for col in range(COLS):
            for row in range(ROWS):
                rect = molded_cell_rect(track, row, col, origin_x, origin_y)
                if rect:
                    pygame.draw.rect(surface, colors[row + col * ROWS], rect)


def face_cell_at(position):
    px, py = position[0] - GRID_X, position[1] - GRID_Y
    for track_id in reversed(visible_track_ids()):
        track = face_tracks[track_id]
        left, top, right, bottom = track["bbox"]
        if not (left <= px <= right and top <= py <= bottom):
            continue
        width, height = right - left, bottom - top
        col = int((px - left) / max(1.0, width) * COLS)
        row = int((py - top) / max(1.0, height) * ROWS)
        if 0 <= row < ROWS and 0 <= col < COLS:
            rect = molded_cell_rect(track, row, col, GRID_X, GRID_Y)
            if rect and rect.collidepoint(position):
                return track_id, row + col * ROWS
    return None


def active_colors():
    if active_face_id in face_tracks:
        return face_tracks[active_face_id]["colors"]
    return None


def apply_to_active(operation):
    colors = active_colors()
    if colors is not None:
        operation(colors)


def shift_south(colors):
    old = colors[:]
    for col in range(COLS):
        for row in range(ROWS):
            colors[row + col * ROWS] = old[((row - 1) % ROWS) + col * ROWS]


def shift_north(colors):
    old = colors[:]
    for col in range(COLS):
        for row in range(ROWS):
            colors[row + col * ROWS] = old[((row + 1) % ROWS) + col * ROWS]


def shift_east(colors):
    old = colors[:]
    for col in range(COLS):
        for row in range(ROWS):
            colors[row + col * ROWS] = old[row + ((col - 1) % COLS) * ROWS]


def symmetry(colors, reverse=False):
    for row in range(ROWS):
        for col in range(COLS // 2):
            left = row + col * ROWS
            right = row + (COLS - col - 1) * ROWS
            if reverse:
                colors[left] = colors[right]
            else:
                colors[right] = colors[left]


def auto_a30(colors):
    for col in range(COLS):
        row = random.randrange(ROWS)
        colors[row + col * ROWS] = fg_color


def blur(colors):
    old = colors[:]
    for col in range(COLS):
        for row in range(ROWS):
            values = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr, cc = row + dr, col + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS:
                        values.append(old[rr + cc * ROWS])
            colors[row + col * ROWS] = tuple(
                sum(value[channel] for value in values) // len(values)
                for channel in range(3)
            )


def make_composite_surface(refresh=True):
    surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
    camera_surface = update_camera_and_faces() if refresh else last_camera_surface
    if camera_surface:
        surface.blit(camera_surface, (0, 0))
    else:
        surface.fill((30, 30, 30))
    draw_face_artworks(surface)
    return surface


def surface_to_image(surface):
    data = pygame.image.tostring(surface, "RGB")
    return Image.frombytes("RGB", surface.get_size(), data)


def save_png():
    filename = make_timestamp_filename("png")
    pygame.image.save(make_composite_surface(True), filename)
    print("Saved:", filename)


def save_gif(movement, count):
    frames = []
    for _ in range(count):
        colors = active_colors()
        if colors is not None:
            movement(colors)
        frames.append(surface_to_image(make_composite_surface(True)))
        pygame.event.pump()
    if not frames:
        return
    filename = make_timestamp_filename("gif")
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=80, loop=0)
    print("Saved:", filename)


class Checkbox:
    def __init__(self, x, y, label, checked=False, callback=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label, self.checked, self.callback = label, checked, callback
        self.font = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked
            if self.callback:
                self.callback(self.checked)

    def draw(self, surface):
        pygame.draw.rect(surface, (230, 230, 230), self.rect, 2)
        if self.checked:
            pygame.draw.line(surface, (230, 230, 230), self.rect.topleft,
                             self.rect.bottomright, 3)
            pygame.draw.line(surface, (230, 230, 230), self.rect.topright,
                             self.rect.bottomleft, 3)
        surface.blit(self.font.render(self.label, True, (230, 230, 230)),
                     (self.rect.x + 35, self.rect.y - 2))


class Slider:
    def __init__(self, x, y, color, callback):
        self.rect = pygame.Rect(x, y, 300, 20)
        self.knob = pygame.Rect(x, y, 10, 20)
        self.value, self.color, self.callback, self.dragging = 0, color, callback, False

    def set_x(self, x):
        self.knob.x = max(self.rect.x, min(x, self.rect.right - self.knob.width))
        self.value = int((self.knob.x - self.rect.x) /
                         (self.rect.width - self.knob.width) * 255)
        self.callback()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
            self.set_x(event.pos[0])
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.set_x(event.pos[0])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), self.knob, border_radius=4)


class SliderGroup:
    def __init__(self, x, y, callback):
        self.callback = callback
        self.r = Slider(x, y, (255, 50, 50), self.update)
        self.g = Slider(x, y + 40, (50, 255, 50), self.update)
        self.b = Slider(x, y + 80, (50, 50, 255), self.update)

    def update(self):
        self.callback((self.r.value, self.g.value, self.b.value))

    def handle_event(self, event):
        for slider in (self.r, self.g, self.b):
            slider.handle_event(event)

    def draw(self, surface):
        for slider in (self.r, self.g, self.b):
            slider.draw(surface)


def set_fg(color):
    global fg_color
    fg_color = color


def set_bg(color):
    global bg_color
    bg_color = color


def set_auto(value):
    global auto_color_enabled
    auto_color_enabled = value


def set_shade(value):
    global color_paint_mode_enabled
    color_paint_mode_enabled = value


fg_group = SliderGroup(50, 40, set_fg)
bg_group = SliderGroup(50, 180, set_bg)
auto_checkbox = Checkbox(50, 340, "Auto Color Cycle", False, set_auto)
shade_checkbox = Checkbox(50, 380, "Color Paint Mode", False, set_shade)
font = pygame.font.SysFont(None, 24)


def paint_at(position, erase=False):
    global active_face_id
    hit = face_cell_at(position)
    if not hit:
        return
    face_id, index = hit
    active_face_id = face_id
    if erase:
        face_tracks[face_id]["colors"][index] = (255, 255, 255)
    else:
        face_tracks[face_id]["colors"][index] = (
            generate_same_shade_color(fg_color) if color_paint_mode_enabled else fg_color
        )


def shutdown():
    camera.release()
    face_landmarker.close()
    pygame.quit()


def main():
    global active_face_id, fg_color, q_press_count
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type in (WINDOWMOVED, WINDOWRESIZED, WINDOWSIZECHANGED):
                    continue
                if event.type in (QUIT, WINDOWCLOSE):
                    running = False
                    continue

                fg_group.handle_event(event)
                bg_group.handle_event(event)
                auto_checkbox.handle_event(event)
                shade_checkbox.handle_event(event)

                if event.type == MOUSEBUTTONDOWN:
                    paint_at(event.pos, erase=(event.button == 3))

                if event.type == KEYDOWN:
                    colors = active_colors()
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_TAB:
                        ids = visible_track_ids()
                        if ids:
                            if active_face_id not in ids:
                                active_face_id = ids[0]
                            else:
                                active_face_id = ids[(ids.index(active_face_id) + 1) % len(ids)]
                    elif event.key == K_q and colors is not None:
                        auto_a30(colors)
                        q_press_count += 1
                        if auto_color_enabled and q_press_count % 2 == 0:
                            fg_color = generate_same_shade_color(fg_color)
                    elif event.key == K_w and colors is not None:
                        symmetry(colors)
                    elif event.key == K_e and colors is not None:
                        symmetry(colors, True)
                    elif event.key == K_p and colors is not None:
                        colors[:] = blank_artwork()
                    elif event.key == K_b and colors is not None:
                        blur(colors)
                    elif event.key == K_s:
                        save_png()
                    elif event.key == K_l:
                        save_gif(shift_south, 30)
                    elif event.key == K_k:
                        save_gif(shift_east, 30)
                    elif event.key == K_n:
                        save_gif(lambda c: (shift_east(c), shift_south(c)), 60)
                    elif event.key == K_m:
                        save_gif(lambda c: (shift_east(c), shift_north(c)), 60)

            screen.fill(bg_color)
            camera_surface = update_camera_and_faces()
            if camera_surface:
                screen.blit(camera_surface, (GRID_X, GRID_Y))
            else:
                pygame.draw.rect(screen, (30, 30, 30),
                                 (GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT))

            left, middle, right = pygame.mouse.get_pressed(3)
            if left:
                paint_at(pygame.mouse.get_pos(), False)
            elif right:
                paint_at(pygame.mouse.get_pos(), True)

            draw_face_artworks(screen, GRID_X, GRID_Y)
            fg_group.draw(screen)
            bg_group.draw(screen)
            auto_checkbox.draw(screen)
            shade_checkbox.draw(screen)

            info = [
                "Click a face to select/paint it",
                "TAB: select next face",
                f"Active: Face {active_face_id}" if active_face_id else "Active: none",
                "Q random | W/E symmetry | P clear",
                "B blur | S PNG | L/K/N/M GIF",
            ]
            for i, text in enumerate(info):
                screen.blit(font.render(text, True, (230, 230, 230)), (50, 440 + i * 28))

            pygame.display.flip()
            clock.tick(FPS)
    finally:
        shutdown()


if __name__ == "__main__":
    main()
