from PIL import Image
import cv2
import pygame
from pygame.locals import *
import sys
import datetime
import random


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GRID_ROWS = 30
GRID_COLS = 30
GRID_X = 405
GRID_Y = 20
GRID_WIDTH = 600
GRID_HEIGHT = 600
SQUARE_SIZE = 10
SQUARE_SPACING = 20
CAMERA_INDEX = 0
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(
    "Writers Jumbler 30 Art - q,w,e,p=erase,b=blur,s=save,l,k,n,m"
)
clock = pygame.time.Clock()


# ---------------------------------------------------------
# Webcam setup
# ---------------------------------------------------------
def open_camera(camera_index=0):
    # CAP_DSHOW usually reduces webcam startup delay on Windows.
    if sys.platform.startswith("win"):
        capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not capture.isOpened():
            capture.release()
            capture = cv2.VideoCapture(camera_index)
    else:
        capture = cv2.VideoCapture(camera_index)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return capture


camera = open_camera(CAMERA_INDEX)

if camera.isOpened():
    print("Webcam opened successfully.")
else:
    print("Warning: Could not open webcam. Check camera permissions or CAMERA_INDEX.")


# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
fg_color = (0, 0, 0)
bg_color = (0, 0, 0)
squares = []
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0
last_camera_surface = None


# ---------------------------------------------------------
# Filename helper
# ---------------------------------------------------------
def make_timestamp_filename(ext):
    word = "WritersJumbler_30_Art_"
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S-%p")
    return f"{word}{timestamp}.{ext}"


# ---------------------------------------------------------
# Grid builder
# ---------------------------------------------------------
def build_grid(rows=GRID_ROWS, cols=GRID_COLS):
    squares.clear()

    for col in range(cols):
        for row in range(rows):
            x = GRID_X + col * SQUARE_SPACING
            y = GRID_Y + row * SQUARE_SPACING
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            squares.append({"rect": rect, "color": (255, 255, 255)})


build_grid()


# ---------------------------------------------------------
# Webcam frame conversion
# ---------------------------------------------------------
def get_camera_surface():
    global last_camera_surface

    if not camera.isOpened():
        return last_camera_surface

    success, frame = camera.read()
    if not success or frame is None:
        return last_camera_surface

    # Horizontal mirror, like looking into a mirror.
    frame = cv2.flip(frame, 1)

    # Center-crop to the grid's aspect ratio so the image is not stretched.
    frame_height, frame_width = frame.shape[:2]
    target_ratio = GRID_WIDTH / GRID_HEIGHT
    frame_ratio = frame_width / frame_height

    if frame_ratio > target_ratio:
        crop_width = int(frame_height * target_ratio)
        start_x = (frame_width - crop_width) // 2
        frame = frame[:, start_x:start_x + crop_width]
    elif frame_ratio < target_ratio:
        crop_height = int(frame_width / target_ratio)
        start_y = (frame_height - crop_height) // 2
        frame = frame[start_y:start_y + crop_height, :]

    frame = cv2.resize(
        frame,
        (GRID_WIDTH, GRID_HEIGHT),
        interpolation=cv2.INTER_LINEAR,
    )

    # Convert OpenCV BGR pixels to RGB pixels for Pygame.
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.swapaxes(0, 1)

    last_camera_surface = pygame.surfarray.make_surface(frame)
    return last_camera_surface


# ---------------------------------------------------------
# Marquee functions
# ---------------------------------------------------------
def marquee_south(rows, cols):
    for col in range(cols):
        last_color = squares[(rows - 1) + col * rows]["color"]
        for row in range(rows - 1, 0, -1):
            squares[row + col * rows]["color"] = squares[
                (row - 1) + col * rows
            ]["color"]
        squares[col * rows]["color"] = last_color


def marquee_north(rows, cols):
    for col in range(cols):
        first_color = squares[col * rows]["color"]
        for row in range(rows - 1):
            squares[row + col * rows]["color"] = squares[
                (row + 1) + col * rows
            ]["color"]
        squares[(rows - 1) + col * rows]["color"] = first_color


def marquee_east(rows, cols):
    for row in range(rows):
        last_color = squares[row + (cols - 1) * rows]["color"]
        for col in range(cols - 1, 0, -1):
            squares[row + col * rows]["color"] = squares[
                row + (col - 1) * rows
            ]["color"]
        squares[row]["color"] = last_color


# ---------------------------------------------------------
# Symmetry + autoA30
# ---------------------------------------------------------
def autoSymmetryPainter():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS // 2):
            left = row + col * GRID_ROWS
            right = row + (GRID_COLS - col - 1) * GRID_ROWS
            squares[right]["color"] = squares[left]["color"]


def autoSymmetryPainterReverse():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS // 2):
            left = row + col * GRID_ROWS
            right = row + (GRID_COLS - col - 1) * GRID_ROWS
            squares[left]["color"] = squares[right]["color"]


def autoA30():
    for offset in range(0, GRID_ROWS * GRID_COLS, GRID_ROWS):
        n = random.randint(1, GRID_ROWS)
        idx = n + offset
        if idx < len(squares):
            squares[idx]["color"] = fg_color


# ---------------------------------------------------------
# Auto Color Cycle
# ---------------------------------------------------------
def generate_same_shade_color(base_color):
    r, g, b = base_color
    delta = random.randint(-85, 85)
    nr = max(0, min(255, r + delta))
    ng = max(0, min(255, g + delta))
    nb = max(0, min(255, b + delta))
    return nr, ng, nb


def autoColorCycle():
    global fg_color, q_press_count
    q_press_count += 1
    if q_press_count % 2 == 0:
        fg_color = generate_same_shade_color(fg_color)
        print("Auto-color changed:", fg_color)


# ---------------------------------------------------------
# Blur
# ---------------------------------------------------------
def autoBlur():
    original = [sq["color"] for sq in squares]

    def get_color(row, col):
        return original[row + col * GRID_ROWS]

    for col in range(GRID_COLS):
        for row in range(GRID_ROWS):
            neighbors = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = row + dr
                    cc = col + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neighbors.append(get_color(rr, cc))

            avg_r = sum(color[0] for color in neighbors) // len(neighbors)
            avg_g = sum(color[1] for color in neighbors) // len(neighbors)
            avg_b = sum(color[2] for color in neighbors) // len(neighbors)
            squares[row + col * GRID_ROWS]["color"] = (avg_r, avg_g, avg_b)


# ---------------------------------------------------------
# Save PNG/GIF with mirrored webcam background and squares
# ---------------------------------------------------------
def surface_to_image(surface):
    data = pygame.image.tostring(surface, "RGB")
    return Image.frombytes("RGB", surface.get_size(), data)


def make_composite_surface(refresh_camera=True):
    """Build the exact 600x600 saved image: camera first, squares second."""
    surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

    camera_surface = get_camera_surface() if refresh_camera else last_camera_surface
    if camera_surface is not None:
        surface.blit(camera_surface, (0, 0))
    else:
        surface.fill((30, 30, 30))

    for sq in squares:
        shifted = sq["rect"].move(-GRID_X, -GRID_Y)
        pygame.draw.rect(surface, sq["color"], shifted)

    return surface


def save_picture_only():
    surface = make_composite_surface(refresh_camera=True)
    filename = make_timestamp_filename("png")
    pygame.image.save(surface, filename)
    print("Saved webcam background + squares:", filename)


# ---------------------------------------------------------
# Save GIF with live mirrored webcam background and squares
# ---------------------------------------------------------
def gif_frame():
    return surface_to_image(make_composite_surface(refresh_camera=True))


def save_animation_gif_south():
    frames = []
    for _ in range(GRID_ROWS):
        marquee_south(GRID_ROWS, GRID_COLS)
        frames.append(gif_frame())

    filename = make_timestamp_filename("gif")
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print("Saved:", filename)


def save_animation_gif_east():
    frames = []
    for _ in range(GRID_COLS):
        marquee_east(GRID_ROWS, GRID_COLS)
        frames.append(gif_frame())

    filename = make_timestamp_filename("gif")
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print("Saved:", filename)


def save_animation_gif_south_east():
    frames = []
    for _ in range(60):
        marquee_east(GRID_ROWS, GRID_COLS)
        marquee_south(GRID_ROWS, GRID_COLS)
        frames.append(gif_frame())

    filename = make_timestamp_filename("gif")
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print("Saved:", filename)


def save_animation_gif_north_east():
    frames = []
    for _ in range(60):
        marquee_east(GRID_ROWS, GRID_COLS)
        marquee_north(GRID_ROWS, GRID_COLS)
        frames.append(gif_frame())

    filename = make_timestamp_filename("gif")
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print("Saved:", filename)


# ---------------------------------------------------------
# UI Classes
# ---------------------------------------------------------
class Checkbox:
    def __init__(self, x, y, label, checked=False, callback=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = checked
        self.callback = callback
        self.font = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)

    def draw(self, surface):
        pygame.draw.rect(surface, (230, 230, 230), self.rect, 2)
        if self.checked:
            pygame.draw.line(
                surface,
                (230, 230, 230),
                (self.rect.x + 4, self.rect.y + 10),
                (self.rect.x + 10, self.rect.y + 16),
                3,
            )
            pygame.draw.line(
                surface,
                (230, 230, 230),
                (self.rect.x + 10, self.rect.y + 16),
                (self.rect.x + 16, self.rect.y + 4),
                3,
            )

        text = self.font.render(self.label, True, (230, 230, 230))
        surface.blit(text, (self.rect.x + 50, self.rect.y - 2))


class Slider:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        value=0,
        max_value=255,
        color=(200, 200, 200),
        callback=None,
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.knob_rect = pygame.Rect(x, y, 10, h)
        self.max_value = max_value
        self.value = value
        self.color = color
        self.dragging = False
        self.callback = callback
        self.update_knob()

    def update_knob(self):
        ratio = self.value / self.max_value
        self.knob_rect.x = self.rect.x + int(
            ratio * (self.rect.width - self.knob_rect.width)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                self.set_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_from_mouse(event.pos[0])

    def set_from_mouse(self, mouse_x):
        new_x = max(
            self.rect.x,
            min(mouse_x, self.rect.x + self.rect.width - self.knob_rect.width),
        )
        self.knob_rect.x = new_x
        ratio = (self.knob_rect.x - self.rect.x) / (
            self.rect.width - self.knob_rect.width
        )
        self.value = int(ratio * self.max_value)
        if self.callback:
            self.callback(self.value)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), self.knob_rect, border_radius=4)


class SliderGroup:
    def __init__(self, x, y, label, callback):
        self.label = label
        self.callback = callback
        self.r = Slider(x, y, 300, 20, 0, color=(255, 50, 50), callback=self.update)
        self.g = Slider(
            x, y + 40, 300, 20, 0, color=(50, 255, 50), callback=self.update
        )
        self.b = Slider(
            x, y + 80, 300, 20, 0, color=(50, 50, 255), callback=self.update
        )
        self.color = (0, 0, 0)

    def update(self, _):
        self.color = self.r.value, self.g.value, self.b.value
        self.callback(self.color)

    def handle_event(self, event):
        self.r.handle_event(event)
        self.g.handle_event(event)
        self.b.handle_event(event)

    def draw(self, surface):
        self.r.draw(surface)
        self.g.draw(surface)
        self.b.draw(surface)


class CheckboxGroup:
    def __init__(self):
        self.paint = Checkbox(50, 320, "Paint Mode", True, self.on_paint)
        self.erase = Checkbox(50, 360, "Erase Mode", False, self.on_erase)

    def on_paint(self, checked):
        if checked:
            self.erase.checked = False

    def on_erase(self, checked):
        if checked:
            self.paint.checked = False

    def handle_event(self, event):
        self.paint.handle_event(event)
        self.erase.handle_event(event)

    def draw(self, surface):
        self.paint.draw(surface)
        self.erase.draw(surface)

    def is_paint_mode(self):
        return self.paint.checked

    def is_erase_mode(self):
        return self.erase.checked


# ---------------------------------------------------------
# Checkbox callbacks
# ---------------------------------------------------------
def toggle_color_paint_mode(checked):
    global color_paint_mode_enabled
    color_paint_mode_enabled = checked


def toggle_auto_color(checked):
    global auto_color_enabled
    auto_color_enabled = checked


# ---------------------------------------------------------
# Slider callbacks
# ---------------------------------------------------------
def on_fg_change(new_color):
    global fg_color
    fg_color = new_color


def on_bg_change(new_color):
    global bg_color
    bg_color = new_color


fg_group = SliderGroup(50, 40, "FG", on_fg_change)
bg_group = SliderGroup(50, 180, "BG", on_bg_change)
mode_group = CheckboxGroup()
auto_color_checkbox = Checkbox(
    50, 440, "Auto Color Cycle", False, toggle_auto_color
)
color_paint_checkbox = Checkbox(
    50, 480, "Color Paint Mode", False, toggle_color_paint_mode
)


# ---------------------------------------------------------
# Painting
# ---------------------------------------------------------
def handle_square_click(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    for sq in squares:
        if sq["rect"].collidepoint(event.pos):
            if event.button == 3:
                sq["color"] = (255, 255, 255)
                return

            if event.button == 1:
                if mode_group.is_paint_mode():
                    if color_paint_mode_enabled:
                        sq["color"] = generate_same_shade_color(fg_color)
                    else:
                        sq["color"] = fg_color
                else:
                    sq["color"] = (255, 255, 255)
            return


def handle_hover_paint(pos):
    for sq in squares:
        if sq["rect"].collidepoint(pos):
            if mode_group.is_paint_mode():
                if color_paint_mode_enabled:
                    sq["color"] = generate_same_shade_color(fg_color)
                else:
                    sq["color"] = fg_color
            elif mode_group.is_erase_mode():
                sq["color"] = (255, 255, 255)
            break


# ---------------------------------------------------------
# Shutdown helper
# ---------------------------------------------------------
def shutdown():
    if camera is not None:
        camera.release()
    pygame.quit()


# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------
def main():
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    continue

                fg_group.handle_event(event)
                bg_group.handle_event(event)
                mode_group.handle_event(event)
                auto_color_checkbox.handle_event(event)
                color_paint_checkbox.handle_event(event)

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_q:
                        autoA30()
                        if auto_color_enabled:
                            autoColorCycle()
                    elif event.key == K_w:
                        autoSymmetryPainter()
                    elif event.key == K_e:
                        autoSymmetryPainterReverse()
                    elif event.key == K_p:
                        for sq in squares:
                            sq["color"] = (255, 255, 255)
                    elif event.key == K_b:
                        autoBlur()
                    elif event.key == K_s:
                        save_picture_only()
                    elif event.key == K_l:
                        save_animation_gif_south()
                    elif event.key == K_k:
                        save_animation_gif_east()
                    elif event.key == K_n:
                        save_animation_gif_south_east()
                    elif event.key == K_m:
                        save_animation_gif_north_east()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_square_click(event)

            screen.fill(bg_color)

            # The camera is drawn first, directly behind the square grid.
            camera_surface = get_camera_surface()
            if camera_surface is not None:
                screen.blit(camera_surface, (GRID_X, GRID_Y))
            else:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    (GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT),
                )

            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            if mouse_buttons[0]:
                handle_hover_paint(mouse_pos)

            # Draw grid squares after the webcam so they appear on top.
            for sq in squares:
                pygame.draw.rect(screen, sq["color"], sq["rect"])

            color_paint_checkbox.draw(screen)
            fg_group.draw(screen)
            bg_group.draw(screen)
            mode_group.draw(screen)
            auto_color_checkbox.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

    finally:
        shutdown()


if __name__ == "__main__":
    main()
