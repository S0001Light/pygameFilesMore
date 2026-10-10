from pathlib import Path
from PIL import Image

import cv2
import mediapipe as mp
import numpy as np
import pygame

from pygame.locals import *

import sys
import datetime
import random
import math
import time
import urllib.request


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

GRID_X = 405
GRID_Y = 20
GRID_WIDTH = 600
GRID_HEIGHT = 600

ROWS = 30
COLS = 30

CAMERA_INDEX = 0
FPS = 60

MAX_PEOPLE = 6

# Distance used when matching a new detection to an existing person.
TRACK_DISTANCE = 180

# Number of detection cycles a person may disappear before removal.
TRACK_TIMEOUT = 30

# Run MediaPipe once every this many displayed frames.
# Increase to 3 or 4 on slower computers.
DETECTION_INTERVAL = 2

# Internal pose detection size.
# Smaller values improve speed.
DETECTION_WIDTH = 384
DETECTION_HEIGHT = 384

MASK_THRESHOLD = 0.20

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.RESIZABLE,
    32,
)

pygame.display.set_caption(
    "Writers Jumbler - Multi-Person Body and Face Art"
)

clock = pygame.time.Clock()


# ============================================================
# CAMERA
# ============================================================

def open_camera(index):
    if sys.platform.startswith("win"):
        capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)

        if not capture.isOpened():
            capture.release()
            capture = cv2.VideoCapture(index)
    else:
        capture = cv2.VideoCapture(index)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return capture


camera = open_camera(CAMERA_INDEX)

if not camera.isOpened():
    print("Warning: webcam unavailable.")


# ============================================================
# MEDIAPIPE POSE MODEL
# ============================================================

MODEL_FILENAME = "pose_landmarker_full.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_full/float16/1/"
    "pose_landmarker_full.task"
)

MODEL_PATH = Path(__file__).resolve().with_name(MODEL_FILENAME)


def ensure_pose_model():
    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 100000:
        return

    print("Downloading MediaPipe Pose Landmarker model...")
    print("This only happens the first time.")

    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    except Exception as error:
        raise RuntimeError(
            "Could not download pose_landmarker_full.task.\n"
            "Download the official MediaPipe Pose Landmarker model and "
            "place it beside this Python script.\n"
            f"Original error: {error}"
        ) from error


ensure_pose_model()

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

pose_options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=MAX_PEOPLE,
    min_pose_detection_confidence=0.45,
    min_pose_presence_confidence=0.45,
    min_tracking_confidence=0.45,
    output_segmentation_masks=True,
)

pose_landmarker = PoseLandmarker.create_from_options(pose_options)


# ============================================================
# MEDIAPIPE POSE LANDMARK INDEXES
# ============================================================

NOSE = 0

LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3

RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6

LEFT_EAR = 7
RIGHT_EAR = 8

MOUTH_LEFT = 9
MOUTH_RIGHT = 10

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LEFT_WRIST = 15
RIGHT_WRIST = 16

LEFT_PINKY = 17
RIGHT_PINKY = 18

LEFT_INDEX = 19
RIGHT_INDEX = 20

LEFT_THUMB = 21
RIGHT_THUMB = 22

LEFT_HIP = 23
RIGHT_HIP = 24

LEFT_KNEE = 25
RIGHT_KNEE = 26

LEFT_ANKLE = 27
RIGHT_ANKLE = 28

LEFT_HEEL = 29
RIGHT_HEEL = 30

LEFT_FOOT = 31
RIGHT_FOOT = 32


# ============================================================
# APPLICATION STATE
# ============================================================

fg_color = (0, 0, 0)
bg_color = (0, 0, 0)

auto_color_enabled = False
color_paint_mode_enabled = False

q_press_count = 0
frame_number = 0
video_timestamp_ms = 0

last_camera_surface = None
last_rgb_frame = None

next_person_id = 1
active_person_id = None

detection_fps = 0.0
last_detection_time = 0.0

# person_id -> tracking information
person_tracks = {}


# ============================================================
# GENERAL HELPERS
# ============================================================

def blank_artwork():
    return [
        (255, 255, 255)
        for _ in range(ROWS * COLS)
    ]


def make_timestamp_filename(extension):
    stamp = datetime.datetime.now().strftime(
        "%m-%d-%Y-%I-%M-%S-%p"
    )

    return (
        f"WritersJumbler_BodyFaces_{stamp}.{extension}"
    )


def generate_same_shade_color(color):
    delta = random.randint(-85, 85)

    return tuple(
        max(0, min(255, value + delta))
        for value in color
    )


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def clamp_point(point):
    return (
        clamp(point[0], 0.0, GRID_WIDTH - 1.0),
        clamp(point[1], 0.0, GRID_HEIGHT - 1.0),
    )


def crop_camera_frame(frame):
    frame = cv2.flip(frame, 1)

    height, width = frame.shape[:2]

    target_ratio = GRID_WIDTH / GRID_HEIGHT
    current_ratio = width / height

    if current_ratio > target_ratio:
        crop_width = int(height * target_ratio)
        start_x = (width - crop_width) // 2
        frame = frame[:, start_x:start_x + crop_width]

    elif current_ratio < target_ratio:
        crop_height = int(width / target_ratio)
        start_y = (height - crop_height) // 2
        frame = frame[start_y:start_y + crop_height, :]

    frame = cv2.resize(
        frame,
        (GRID_WIDTH, GRID_HEIGHT),
        interpolation=cv2.INTER_LINEAR,
    )

    return frame


def polygon_center(polygon):
    if not polygon:
        return 0.0, 0.0

    return (
        sum(point[0] for point in polygon) / len(polygon),
        sum(point[1] for point in polygon) / len(polygon),
    )


def polygon_bbox(polygon):
    if not polygon:
        return 0.0, 0.0, 1.0, 1.0

    xs = [point[0] for point in polygon]
    ys = [point[1] for point in polygon]

    return (
        min(xs),
        min(ys),
        max(xs),
        max(ys),
    )


def expand_bbox(bbox, amount=7):
    left, top, right, bottom = bbox

    return (
        max(0.0, left - amount),
        max(0.0, top - amount),
        min(GRID_WIDTH - 1.0, right + amount),
        min(GRID_HEIGHT - 1.0, bottom + amount),
    )


def smooth_bbox(old_bbox, new_bbox, old_amount=0.60):
    if old_bbox is None:
        return new_bbox

    new_amount = 1.0 - old_amount

    return tuple(
        old_bbox[index] * old_amount
        + new_bbox[index] * new_amount
        for index in range(4)
    )


def smooth_center(old_center, new_center, old_amount=0.60):
    if old_center is None:
        return new_center

    new_amount = 1.0 - old_amount

    return (
        old_center[0] * old_amount
        + new_center[0] * new_amount,

        old_center[1] * old_amount
        + new_center[1] * new_amount,
    )


def smooth_mask(old_mask, new_mask, old_amount=0.55):
    if old_mask is None:
        return new_mask

    if new_mask is None:
        return old_mask

    if old_mask.shape != new_mask.shape:
        return new_mask

    new_amount = 1.0 - old_amount

    return (
        old_mask * old_amount
        + new_mask * new_amount
    ).astype(np.float32)


# ============================================================
# LANDMARK AND BODY HELPERS
# ============================================================

def landmark_point(landmarks, index):
    landmark = landmarks[index]

    return (
        clamp(
            landmark.x * GRID_WIDTH,
            0.0,
            GRID_WIDTH - 1.0,
        ),
        clamp(
            landmark.y * GRID_HEIGHT,
            0.0,
            GRID_HEIGHT - 1.0,
        ),
    )


def landmark_visibility(landmarks, index):
    landmark = landmarks[index]

    visibility = getattr(landmark, "visibility", None)

    if visibility is None:
        return 1.0

    return float(visibility)


def average_points(*points):
    valid_points = [
        point
        for point in points
        if point is not None
    ]

    if not valid_points:
        return 0.0, 0.0

    return (
        sum(point[0] for point in valid_points) / len(valid_points),
        sum(point[1] for point in valid_points) / len(valid_points),
    )


def body_center_from_pose(landmarks):
    points = []

    for index in (
        LEFT_SHOULDER,
        RIGHT_SHOULDER,
        LEFT_HIP,
        RIGHT_HIP,
    ):
        if landmark_visibility(landmarks, index) >= 0.25:
            points.append(landmark_point(landmarks, index))

    if not points:
        return landmark_point(landmarks, NOSE)

    return average_points(*points)


def mask_to_array(mask):
    if mask is None:
        return None

    try:
        array = mask.numpy_view()
    except (AttributeError, RuntimeError):
        return None

    array = np.asarray(array, dtype=np.float32)

    if array.ndim == 3:
        array = array[:, :, 0]

    if array.shape != (GRID_HEIGHT, GRID_WIDTH):
        array = cv2.resize(
            array,
            (GRID_WIDTH, GRID_HEIGHT),
            interpolation=cv2.INTER_LINEAR,
        )

    return np.clip(array, 0.0, 1.0).copy()


def mask_bbox(mask, threshold=MASK_THRESHOLD):
    if mask is None:
        return None

    binary = mask >= threshold
    ys, xs = np.where(binary)

    if xs.size == 0 or ys.size == 0:
        return None

    return (
        float(xs.min()),
        float(ys.min()),
        float(xs.max()),
        float(ys.max()),
    )


def create_fallback_body_polygon(landmarks):
    """
    Create an approximate body silhouette when a segmentation mask
    is unavailable.
    """

    nose = landmark_point(landmarks, NOSE)

    left_ear = landmark_point(landmarks, LEFT_EAR)
    right_ear = landmark_point(landmarks, RIGHT_EAR)

    left_shoulder = landmark_point(
        landmarks,
        LEFT_SHOULDER,
    )

    right_shoulder = landmark_point(
        landmarks,
        RIGHT_SHOULDER,
    )

    left_elbow = landmark_point(
        landmarks,
        LEFT_ELBOW,
    )

    right_elbow = landmark_point(
        landmarks,
        RIGHT_ELBOW,
    )

    left_wrist = landmark_point(
        landmarks,
        LEFT_WRIST,
    )

    right_wrist = landmark_point(
        landmarks,
        RIGHT_WRIST,
    )

    left_index = landmark_point(
        landmarks,
        LEFT_INDEX,
    )

    right_index = landmark_point(
        landmarks,
        RIGHT_INDEX,
    )

    left_hip = landmark_point(
        landmarks,
        LEFT_HIP,
    )

    right_hip = landmark_point(
        landmarks,
        RIGHT_HIP,
    )

    left_knee = landmark_point(
        landmarks,
        LEFT_KNEE,
    )

    right_knee = landmark_point(
        landmarks,
        RIGHT_KNEE,
    )

    left_ankle = landmark_point(
        landmarks,
        LEFT_ANKLE,
    )

    right_ankle = landmark_point(
        landmarks,
        RIGHT_ANKLE,
    )

    left_heel = landmark_point(
        landmarks,
        LEFT_HEEL,
    )

    right_heel = landmark_point(
        landmarks,
        RIGHT_HEEL,
    )

    left_foot = landmark_point(
        landmarks,
        LEFT_FOOT,
    )

    right_foot = landmark_point(
        landmarks,
        RIGHT_FOOT,
    )

    head_width = max(
        30.0,
        math.hypot(
            left_ear[0] - right_ear[0],
            left_ear[1] - right_ear[1],
        ),
    )

    head_top = clamp_point((
        nose[0],
        nose[1] - head_width * 0.95,
    ))

    left_head = clamp_point((
        left_ear[0] - head_width * 0.30,
        left_ear[1],
    ))

    right_head = clamp_point((
        right_ear[0] + head_width * 0.30,
        right_ear[1],
    ))

    points = [
        head_top,
        right_head,
        right_shoulder,
        right_elbow,
        right_wrist,
        right_index,
        right_wrist,
        right_elbow,
        right_hip,
        right_knee,
        right_ankle,
        right_foot,
        right_heel,
        left_heel,
        left_foot,
        left_ankle,
        left_knee,
        left_hip,
        left_elbow,
        left_wrist,
        left_index,
        left_wrist,
        left_elbow,
        left_shoulder,
        left_head,
    ]

    point_array = np.array(
        points,
        dtype=np.float32,
    )

    hull = cv2.convexHull(point_array)

    return [
        (
            float(point[0][0]),
            float(point[0][1]),
        )
        for point in hull
    ]


def point_inside_polygon(point, polygon):
    if not polygon:
        return False

    contour = np.asarray(
        polygon,
        dtype=np.float32,
    )

    return (
        cv2.pointPolygonTest(
            contour,
            point,
            False,
        ) >= 0
    )


# ============================================================
# PERSON TRACKING
# ============================================================

def visible_track_ids():
    return [
        person_id
        for person_id, track in person_tracks.items()
        if track["missed"] == 0
    ]


def assign_detections(detections):
    global next_person_id
    global active_person_id

    unmatched_tracks = set(person_tracks.keys())
    assignments = []

    # Largest people are matched first.
    detections.sort(
        key=lambda item: (
            item["bbox"][2] - item["bbox"][0]
        ) * (
            item["bbox"][3] - item["bbox"][1]
        ),
        reverse=True,
    )

    for detection in detections:
        detection_center = detection["center"]

        best_id = None
        best_distance = TRACK_DISTANCE

        detection_width = (
            detection["bbox"][2]
            - detection["bbox"][0]
        )

        detection_height = (
            detection["bbox"][3]
            - detection["bbox"][1]
        )

        detection_size = max(
            detection_width,
            detection_height,
            1.0,
        )

        for person_id in unmatched_tracks:
            track = person_tracks[person_id]
            track_center = track["center"]

            distance = math.hypot(
                detection_center[0] - track_center[0],
                detection_center[1] - track_center[1],
            )

            track_width = (
                track["bbox"][2]
                - track["bbox"][0]
            )

            track_height = (
                track["bbox"][3]
                - track["bbox"][1]
            )

            track_size = max(
                track_width,
                track_height,
                1.0,
            )

            adaptive_distance = max(
                TRACK_DISTANCE,
                min(
                    detection_size,
                    track_size,
                ) * 0.65,
            )

            if (
                distance < best_distance
                or (
                    best_id is None
                    and distance < adaptive_distance
                )
            ):
                best_distance = distance
                best_id = person_id

        if best_id is None:
            best_id = next_person_id
            next_person_id += 1

            person_tracks[best_id] = {
                "center": detection["center"],
                "polygon": detection["polygon"],
                "bbox": detection["bbox"],
                "mask": detection["mask"],
                "colors": blank_artwork(),
                "missed": 0,
            }

            if active_person_id is None:
                active_person_id = best_id

        else:
            unmatched_tracks.remove(best_id)

            track = person_tracks[best_id]

            detection["center"] = smooth_center(
                track.get("center"),
                detection["center"],
                0.60,
            )

            detection["bbox"] = smooth_bbox(
                track.get("bbox"),
                detection["bbox"],
                0.60,
            )

            detection["mask"] = smooth_mask(
                track.get("mask"),
                detection["mask"],
                0.55,
            )

        track = person_tracks[best_id]

        track["center"] = detection["center"]
        track["polygon"] = detection["polygon"]
        track["bbox"] = detection["bbox"]
        track["mask"] = detection["mask"]
        track["missed"] = 0

        assignments.append(best_id)

    for person_id in list(unmatched_tracks):
        track = person_tracks[person_id]
        track["missed"] += 1

        if track["missed"] > TRACK_TIMEOUT:
            del person_tracks[person_id]

            if active_person_id == person_id:
                visible_ids = visible_track_ids()

                active_person_id = (
                    visible_ids[0]
                    if visible_ids
                    else None
                )

    return assignments


# ============================================================
# CAMERA AND POSE DETECTION
# ============================================================

def update_camera_and_people():
    global last_camera_surface
    global last_rgb_frame
    global frame_number
    global video_timestamp_ms
    global detection_fps
    global last_detection_time

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

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB,
    )

    last_rgb_frame = rgb.copy()

    last_camera_surface = pygame.surfarray.make_surface(
        rgb.swapaxes(0, 1)
    )

    run_detection = (
        frame_number % DETECTION_INTERVAL == 0
    )

    if run_detection:
        detection_start = time.perf_counter()

        detection_rgb = cv2.resize(
            rgb,
            (DETECTION_WIDTH, DETECTION_HEIGHT),
            interpolation=cv2.INTER_AREA,
        )

        detection_rgb = np.ascontiguousarray(
            detection_rgb
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=detection_rgb,
        )

        video_timestamp_ms += max(
            1,
            int(1000 / max(1, FPS // DETECTION_INTERVAL)),
        )

        try:
            pose_result = pose_landmarker.detect_for_video(
                mp_image,
                video_timestamp_ms,
            )
        except Exception as error:
            print("Pose detection error:", error)
            pose_result = None

        detections = []

        if (
            pose_result is not None
            and pose_result.pose_landmarks
        ):
            segmentation_masks = (
                pose_result.segmentation_masks
                if pose_result.segmentation_masks
                else []
            )

            for pose_index, pose_landmarks in enumerate(
                pose_result.pose_landmarks
            ):
                polygon = create_fallback_body_polygon(
                    pose_landmarks
                )

                mask = None

                if pose_index < len(segmentation_masks):
                    mask = mask_to_array(
                        segmentation_masks[pose_index]
                    )

                bbox = mask_bbox(mask)

                if bbox is None:
                    bbox = polygon_bbox(polygon)

                bbox = expand_bbox(bbox, 5)

                center = body_center_from_pose(
                    pose_landmarks
                )

                detections.append({
                    "polygon": polygon,
                    "center": center,
                    "bbox": bbox,
                    "mask": mask,
                })

        assign_detections(detections)

        detection_elapsed = (
            time.perf_counter() - detection_start
        )

        if detection_elapsed > 0:
            current_detection_fps = (
                1.0 / detection_elapsed
            )

            if detection_fps == 0.0:
                detection_fps = current_detection_fps
            else:
                detection_fps = (
                    detection_fps * 0.85
                    + current_detection_fps * 0.15
                )

        last_detection_time = time.perf_counter()

    frame_number += 1

    return last_camera_surface


# ============================================================
# BODY GRID MAPPING
# ============================================================

def molded_cell_rect(
    track,
    row,
    col,
    origin_x=0,
    origin_y=0,
):
    left, top, right, bottom = track["bbox"]

    width = max(1.0, right - left)
    height = max(1.0, bottom - top)

    cell_width = width / COLS
    cell_height = height / ROWS

    center_x = (
        left
        + (col + 0.5) * cell_width
    )

    center_y = (
        top
        + (row + 0.5) * cell_height
    )

    mask = track.get("mask")

    fill_amount = 0.0
    inside = False

    if mask is not None:
        center_ix = int(
            clamp(
                center_x,
                0,
                GRID_WIDTH - 1,
            )
        )

        center_iy = int(
            clamp(
                center_y,
                0,
                GRID_HEIGHT - 1,
            )
        )

        center_value = float(
            mask[center_iy, center_ix]
        )

        x0 = max(
            0,
            int(left + col * cell_width),
        )

        y0 = max(
            0,
            int(top + row * cell_height),
        )

        x1 = min(
            GRID_WIDTH,
            int(left + (col + 1) * cell_width) + 1,
        )

        y1 = min(
            GRID_HEIGHT,
            int(top + (row + 1) * cell_height) + 1,
        )

        if x1 <= x0 or y1 <= y0:
            return None

        sample = mask[y0:y1, x0:x1]

        if sample.size:
            average_value = float(
                np.mean(sample)
            )

            maximum_value = float(
                np.max(sample)
            )

            fill_amount = max(
                center_value,
                average_value,
                maximum_value * 0.70,
            )

            inside = (
                center_value >= MASK_THRESHOLD
                or average_value >= 0.12
                or maximum_value >= 0.45
            )

    else:
        inside = point_inside_polygon(
            (center_x, center_y),
            track["polygon"],
        )

        fill_amount = 1.0 if inside else 0.0

    if not inside:
        return None

    scale = clamp(
        fill_amount,
        0.38,
        1.0,
    )

    draw_width = max(
        1,
        int(cell_width * 0.92 * scale),
    )

    draw_height = max(
        1,
        int(cell_height * 0.92 * scale),
    )

    return pygame.Rect(
        origin_x
        + int(center_x - draw_width / 2),

        origin_y
        + int(center_y - draw_height / 2),

        draw_width,
        draw_height,
    )


def build_track_cell_cache(track):
    cache_key = tuple(
        round(value, 1)
        for value in track["bbox"]
    )

    current_key = track.get("cell_cache_key")

    if current_key == cache_key:
        cached_rects = track.get("cell_cache")

        if cached_rects is not None:
            return cached_rects

    rects = []

    for col in range(COLS):
        for row in range(ROWS):
            rect = molded_cell_rect(
                track,
                row,
                col,
            )

            if rect is not None:
                index = row + col * ROWS
                rects.append((index, rect))

    track["cell_cache_key"] = cache_key
    track["cell_cache"] = rects

    return rects


def draw_person_artworks(
    surface,
    origin_x=0,
    origin_y=0,
):
    for person_id in visible_track_ids():
        track = person_tracks[person_id]
        colors = track["colors"]

        cell_rects = build_track_cell_cache(track)

        for index, base_rect in cell_rects:
            rect = base_rect.move(
                origin_x,
                origin_y,
            )

            pygame.draw.rect(
                surface,
                colors[index],
                rect,
            )

        if person_id == active_person_id:
            left, top, right, bottom = track["bbox"]

            selection_rect = pygame.Rect(
                origin_x + int(left),
                origin_y + int(top),
                max(1, int(right - left)),
                max(1, int(bottom - top)),
            )

            pygame.draw.rect(
                surface,
                (255, 230, 40),
                selection_rect,
                2,
            )


def person_cell_at(position):
    local_x = position[0] - GRID_X
    local_y = position[1] - GRID_Y

    if not (
        0 <= local_x < GRID_WIDTH
        and 0 <= local_y < GRID_HEIGHT
    ):
        return None

    for person_id in reversed(visible_track_ids()):
        track = person_tracks[person_id]

        left, top, right, bottom = track["bbox"]

        if not (
            left <= local_x <= right
            and top <= local_y <= bottom
        ):
            continue

        width = max(1.0, right - left)
        height = max(1.0, bottom - top)

        col = int(
            (local_x - left) / width * COLS
        )

        row = int(
            (local_y - top) / height * ROWS
        )

        col = clamp(col, 0, COLS - 1)
        row = clamp(row, 0, ROWS - 1)

        mask = track.get("mask")

        if mask is not None:
            mask_x = int(
                clamp(
                    local_x,
                    0,
                    GRID_WIDTH - 1,
                )
            )

            mask_y = int(
                clamp(
                    local_y,
                    0,
                    GRID_HEIGHT - 1,
                )
            )

            if mask[mask_y, mask_x] < 0.14:
                continue

        else:
            if not point_inside_polygon(
                (local_x, local_y),
                track["polygon"],
            ):
                continue

        return (
            person_id,
            row + col * ROWS,
        )

    return None


# ============================================================
# ACTIVE ARTWORK
# ============================================================

def active_colors():
    if active_person_id in person_tracks:
        return person_tracks[
            active_person_id
        ]["colors"]

    return None


def apply_to_active(operation):
    colors = active_colors()

    if colors is not None:
        operation(colors)


# ============================================================
# ART EFFECTS
# ============================================================

def shift_south(colors):
    old = colors[:]

    for col in range(COLS):
        for row in range(ROWS):
            source_row = (row - 1) % ROWS

            colors[row + col * ROWS] = (
                old[source_row + col * ROWS]
            )


def shift_north(colors):
    old = colors[:]

    for col in range(COLS):
        for row in range(ROWS):
            source_row = (row + 1) % ROWS

            colors[row + col * ROWS] = (
                old[source_row + col * ROWS]
            )


def shift_east(colors):
    old = colors[:]

    for col in range(COLS):
        for row in range(ROWS):
            source_col = (col - 1) % COLS

            colors[row + col * ROWS] = (
                old[row + source_col * ROWS]
            )


def shift_west(colors):
    old = colors[:]

    for col in range(COLS):
        for row in range(ROWS):
            source_col = (col + 1) % COLS

            colors[row + col * ROWS] = (
                old[row + source_col * ROWS]
            )


def symmetry(colors, reverse=False):
    for row in range(ROWS):
        for col in range(COLS // 2):
            left_index = row + col * ROWS

            right_index = (
                row
                + (COLS - col - 1) * ROWS
            )

            if reverse:
                colors[left_index] = (
                    colors[right_index]
                )
            else:
                colors[right_index] = (
                    colors[left_index]
                )


def auto_a30(colors):
    for col in range(COLS):
        row = random.randrange(ROWS)

        colors[row + col * ROWS] = fg_color


def blur(colors):
    old = colors[:]

    for col in range(COLS):
        for row in range(ROWS):
            values = []

            for delta_col in (-1, 0, 1):
                for delta_row in (-1, 0, 1):
                    sample_row = row + delta_row
                    sample_col = col + delta_col

                    if (
                        0 <= sample_row < ROWS
                        and 0 <= sample_col < COLS
                    ):
                        values.append(
                            old[
                                sample_row
                                + sample_col * ROWS
                            ]
                        )

            colors[row + col * ROWS] = tuple(
                sum(
                    value[channel]
                    for value in values
                ) // len(values)
                for channel in range(3)
            )


def fill_active_with_color(colors):
    for index in range(len(colors)):
        colors[index] = fg_color


def randomize_active(colors):
    for index in range(len(colors)):
        colors[index] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )


# ============================================================
# SAVING
# ============================================================

def make_composite_surface(refresh=False):
    surface = pygame.Surface(
        (GRID_WIDTH, GRID_HEIGHT)
    )

    if refresh:
        camera_surface = update_camera_and_people()
    else:
        camera_surface = last_camera_surface

    if camera_surface is not None:
        surface.blit(camera_surface, (0, 0))
    else:
        surface.fill((30, 30, 30))

    draw_person_artworks(surface)

    return surface


def surface_to_image(surface):
    data = pygame.image.tostring(
        surface,
        "RGB",
    )

    return Image.frombytes(
        "RGB",
        surface.get_size(),
        data,
    )


def save_png():
    filename = make_timestamp_filename("png")

    composite = make_composite_surface(
        refresh=False
    )

    pygame.image.save(
        composite,
        filename,
    )

    print("Saved:", filename)


def save_gif(movement, count):
    frames = []

    for _ in range(count):
        colors = active_colors()

        if colors is not None:
            movement(colors)

        composite = make_composite_surface(
            refresh=True
        )

        frames.append(
            surface_to_image(composite)
        )

        pygame.event.pump()

    if not frames:
        return

    filename = make_timestamp_filename("gif")

    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        optimize=True,
    )

    print("Saved:", filename)


# ============================================================
# INTERFACE CONTROLS
# ============================================================

class Checkbox:
    def __init__(
        self,
        x,
        y,
        label,
        checked=False,
        callback=None,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            20,
            20,
        )

        self.label = label
        self.checked = checked
        self.callback = callback

        self.font = pygame.font.SysFont(
            None,
            24,
        )

    def handle_event(self, event):
        if (
            event.type == MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.checked = not self.checked

            if self.callback:
                self.callback(self.checked)

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (230, 230, 230),
            self.rect,
            2,
        )

        if self.checked:
            pygame.draw.line(
                surface,
                (230, 230, 230),
                self.rect.topleft,
                self.rect.bottomright,
                3,
            )

            pygame.draw.line(
                surface,
                (230, 230, 230),
                self.rect.topright,
                self.rect.bottomleft,
                3,
            )

        label_surface = self.font.render(
            self.label,
            True,
            (230, 230, 230),
        )

        surface.blit(
            label_surface,
            (
                self.rect.x + 35,
                self.rect.y - 2,
            ),
        )


class Slider:
    def __init__(
        self,
        x,
        y,
        color,
        callback,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            300,
            20,
        )

        self.knob = pygame.Rect(
            x,
            y,
            10,
            20,
        )

        self.value = 0
        self.color = color
        self.callback = callback
        self.dragging = False

    def set_x(self, x):
        self.knob.x = max(
            self.rect.x,
            min(
                x,
                self.rect.right
                - self.knob.width,
            ),
        )

        available_width = (
            self.rect.width
            - self.knob.width
        )

        self.value = int(
            (
                self.knob.x
                - self.rect.x
            )
            / available_width
            * 255
        )

        self.callback()

    def handle_event(self, event):
        if (
            event.type == MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.dragging = True
            self.set_x(event.pos[0])

        elif (
            event.type == MOUSEBUTTONUP
            and event.button == 1
        ):
            self.dragging = False

        elif (
            event.type == MOUSEMOTION
            and self.dragging
        ):
            self.set_x(event.pos[0])

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            border_radius=4,
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            self.knob,
            border_radius=4,
        )


class SliderGroup:
    def __init__(
        self,
        x,
        y,
        callback,
    ):
        self.callback = callback

        self.r = Slider(
            x,
            y,
            (255, 50, 50),
            self.update,
        )

        self.g = Slider(
            x,
            y + 40,
            (50, 255, 50),
            self.update,
        )

        self.b = Slider(
            x,
            y + 80,
            (50, 50, 255),
            self.update,
        )

    def update(self):
        self.callback((
            self.r.value,
            self.g.value,
            self.b.value,
        ))

    def handle_event(self, event):
        self.r.handle_event(event)
        self.g.handle_event(event)
        self.b.handle_event(event)

    def draw(self, surface):
        self.r.draw(surface)
        self.g.draw(surface)
        self.b.draw(surface)


# ============================================================
# CONTROL CALLBACKS
# ============================================================

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


fg_group = SliderGroup(
    50,
    40,
    set_fg,
)

bg_group = SliderGroup(
    50,
    180,
    set_bg,
)

auto_checkbox = Checkbox(
    50,
    340,
    "Auto Color Cycle",
    False,
    set_auto,
)

shade_checkbox = Checkbox(
    50,
    380,
    "Color Paint Mode",
    False,
    set_shade,
)

font = pygame.font.SysFont(
    None,
    24,
)

small_font = pygame.font.SysFont(
    None,
    20,
)


# ============================================================
# PAINTING
# ============================================================

def paint_at(position, erase=False):
    global active_person_id

    hit = person_cell_at(position)

    if hit is None:
        return

    person_id, color_index = hit

    active_person_id = person_id

    colors = person_tracks[
        person_id
    ]["colors"]

    if erase:
        colors[color_index] = (
            255,
            255,
            255,
        )
    else:
        if color_paint_mode_enabled:
            colors[color_index] = (
                generate_same_shade_color(
                    fg_color
                )
            )
        else:
            colors[color_index] = fg_color


# ============================================================
# SHUTDOWN
# ============================================================

def shutdown():
    if camera.isOpened():
        camera.release()

    try:
        pose_landmarker.close()
    except Exception:
        pass

    pygame.quit()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    global active_person_id
    global fg_color
    global q_press_count

    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type in (
                    WINDOWMOVED,
                    WINDOWRESIZED,
                    WINDOWSIZECHANGED,
                ):
                    continue

                if event.type in (
                    QUIT,
                    WINDOWCLOSE,
                ):
                    running = False
                    continue

                fg_group.handle_event(event)
                bg_group.handle_event(event)

                auto_checkbox.handle_event(event)
                shade_checkbox.handle_event(event)

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        paint_at(
                            event.pos,
                            erase=False,
                        )

                    elif event.button == 3:
                        paint_at(
                            event.pos,
                            erase=True,
                        )

                if event.type == KEYDOWN:
                    colors = active_colors()

                    if event.key == K_ESCAPE:
                        running = False

                    elif event.key == K_TAB:
                        person_ids = visible_track_ids()

                        if person_ids:
                            if (
                                active_person_id
                                not in person_ids
                            ):
                                active_person_id = (
                                    person_ids[0]
                                )
                            else:
                                current_index = (
                                    person_ids.index(
                                        active_person_id
                                    )
                                )

                                next_index = (
                                    current_index + 1
                                ) % len(person_ids)

                                active_person_id = (
                                    person_ids[next_index]
                                )

                    elif (
                        event.key == K_q
                        and colors is not None
                    ):
                        auto_a30(colors)

                        q_press_count += 1

                        if (
                            auto_color_enabled
                            and q_press_count % 2 == 0
                        ):
                            fg_color = (
                                generate_same_shade_color(
                                    fg_color
                                )
                            )

                    elif (
                        event.key == K_w
                        and colors is not None
                    ):
                        symmetry(
                            colors,
                            reverse=False,
                        )

                    elif (
                        event.key == K_e
                        and colors is not None
                    ):
                        symmetry(
                            colors,
                            reverse=True,
                        )

                    elif (
                        event.key == K_p
                        and colors is not None
                    ):
                        colors[:] = blank_artwork()

                    elif (
                        event.key == K_b
                        and colors is not None
                    ):
                        blur(colors)

                    elif (
                        event.key == K_f
                        and colors is not None
                    ):
                        fill_active_with_color(colors)

                    elif (
                        event.key == K_r
                        and colors is not None
                    ):
                        randomize_active(colors)

                    elif event.key == K_s:
                        save_png()

                    elif event.key == K_l:
                        save_gif(
                            shift_south,
                            30,
                        )

                    elif event.key == K_k:
                        save_gif(
                            shift_east,
                            30,
                        )

                    elif event.key == K_n:
                        save_gif(
                            lambda current_colors: (
                                shift_east(
                                    current_colors
                                ),
                                shift_south(
                                    current_colors
                                ),
                            ),
                            60,
                        )

                    elif event.key == K_m:
                        save_gif(
                            lambda current_colors: (
                                shift_east(
                                    current_colors
                                ),
                                shift_north(
                                    current_colors
                                ),
                            ),
                            60,
                        )

            screen.fill(bg_color)

            camera_surface = update_camera_and_people()

            if camera_surface is not None:
                screen.blit(
                    camera_surface,
                    (GRID_X, GRID_Y),
                )
            else:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    (
                        GRID_X,
                        GRID_Y,
                        GRID_WIDTH,
                        GRID_HEIGHT,
                    ),
                )

            left_button, _, right_button = (
                pygame.mouse.get_pressed(3)
            )

            mouse_position = pygame.mouse.get_pos()

            if left_button:
                paint_at(
                    mouse_position,
                    erase=False,
                )

            elif right_button:
                paint_at(
                    mouse_position,
                    erase=True,
                )

            draw_person_artworks(
                screen,
                GRID_X,
                GRID_Y,
            )

            fg_group.draw(screen)
            bg_group.draw(screen)

            auto_checkbox.draw(screen)
            shade_checkbox.draw(screen)

            visible_people = len(
                visible_track_ids()
            )

            information = [
                "Click body or face to select/paint",
                "Right-click paints white",
                "TAB: select next person",
                (
                    f"Active: Person {active_person_id}"
                    if active_person_id is not None
                    else "Active: none"
                ),
                f"Visible people: {visible_people}",
                "Q random | W/E symmetry",
                "P clear | B blur | F fill | R colors",
                "S PNG | L/K/N/M GIF",
            ]

            information_y = 430

            for index, text in enumerate(information):
                text_surface = font.render(
                    text,
                    True,
                    (230, 230, 230),
                )

                screen.blit(
                    text_surface,
                    (
                        35,
                        information_y
                        + index * 26,
                    ),
                )

            performance_text = (
                f"Display FPS: {clock.get_fps():.0f}"
            )

            performance_surface = small_font.render(
                performance_text,
                True,
                (170, 200, 230),
            )

            screen.blit(
                performance_surface,
                (35, 653),
            )

            detection_text = (
                f"Pose speed: {detection_fps:.1f} detections/sec"
            )

            detection_surface = small_font.render(
                detection_text,
                True,
                (170, 200, 230),
            )

            screen.blit(
                detection_surface,
                (35, 676),
            )

            optimization_text = (
                f"Detection every {DETECTION_INTERVAL} frames"
            )

            optimization_surface = small_font.render(
                optimization_text,
                True,
                (170, 200, 230),
            )

            screen.blit(
                optimization_surface,
                (35, 699),
            )

            pygame.display.flip()
            clock.tick(FPS)

    finally:
        shutdown()


if __name__ == "__main__":
    main()
