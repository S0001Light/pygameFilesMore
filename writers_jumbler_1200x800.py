from PIL import Image
import os
import sys

# Keep one DPI scale for the entire process. This must be set before pygame
# imports/initializes SDL, otherwise Windows can resize the window when it is
# moved between monitors that use different scaling percentages.
if sys.platform.startswith("win"):
    # Use one process-wide DPI instead of changing DPI when crossing monitors.
    # Also disable SDL's DPI-coordinate scaling so the requested 1024x768
    # client area remains the same SDL size on every monitor.
    os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "system"
    os.environ["SDL_WINDOWS_DPI_SCALING"] = "0"

import pygame
from pygame.locals import *
import datetime
import random

pygame.init()

# ---------------------------------------------------------
# Window and artwork constants
# ---------------------------------------------------------
BASE_SCREEN_WIDTH = 1200
BASE_SCREEN_HEIGHT = 800
ART_X = 405
ART_Y = 20
ART_WIDTH = 600
ART_HEIGHT = 600
SCREEN_WIDTH = BASE_SCREEN_WIDTH
SCREEN_HEIGHT = BASE_SCREEN_HEIGHT
MIN_ART_SIZE = 20
MAX_ART_SIZE = 100
DEFAULT_ART_SIZE = 30
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(
    "Writers Jumbler Art Size Chooser - q,w,e,p,b,h,j,s,l,k,n,m"
)
clock = pygame.time.Clock()

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
fg_color = (0, 0, 0)
bg_color = (0, 0, 0)
canvas_color = (255, 255, 255)
squares = []
art_size = DEFAULT_ART_SIZE
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0

# ---------------------------------------------------------
# Filename helper
# ---------------------------------------------------------
def make_timestamp_filename(ext):
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S-%p")
    return f"WritersJumbler_{art_size}x{art_size}_Art_{timestamp}.{ext}"

# ---------------------------------------------------------
# Grid geometry
# ---------------------------------------------------------
def get_cell_rect(row, col, local=False):
    """Return an exact cell rectangle that tiles the 600x600 artwork area."""
    left = (col * ART_WIDTH) // art_size
    right = ((col + 1) * ART_WIDTH) // art_size
    top = (row * ART_HEIGHT) // art_size
    bottom = ((row + 1) * ART_HEIGHT) // art_size

    if not local:
        left += ART_X
        right += ART_X
        top += ART_Y
        bottom += ART_Y

    return pygame.Rect(left, top, right - left, bottom - top)


def get_square_draw_rect(row, col, local=False):
    """Return a square with a size-aware gap so the grid remains visible."""
    cell = get_cell_rect(row, col, local)
    smallest_side = min(cell.width, cell.height)

    if smallest_side >= 20:
        gap = 8
    elif smallest_side >= 12:
        gap = 4
    elif smallest_side >= 8:
        gap = 2
    else:
        gap = 1

    inset_left = gap // 2
    inset_top = gap // 2
    width = max(1, cell.width - gap)
    height = max(1, cell.height - gap)

    return pygame.Rect(
        cell.x + inset_left,
        cell.y + inset_top,
        width,
        height,
    )

# ---------------------------------------------------------
# Grid builder
# ---------------------------------------------------------
def build_grid(new_size=None):
    global art_size

    if new_size is not None:
        art_size = max(MIN_ART_SIZE, min(MAX_ART_SIZE, int(new_size)))

    squares.clear()

    for col in range(art_size):
        for row in range(art_size):
            squares.append({
                "row": row,
                "col": col,
                "color": canvas_color,
            })

    print(f"Artwork size changed to {art_size} x {art_size}")


def square_index(row, col):
    return row + col * art_size


build_grid(DEFAULT_ART_SIZE)

# ---------------------------------------------------------
# Marquee functions
# ---------------------------------------------------------
def marquee_south():
    for col in range(art_size):
        last_color = squares[square_index(art_size - 1, col)]["color"]
        for row in range(art_size - 1, 0, -1):
            squares[square_index(row, col)]["color"] = squares[
                square_index(row - 1, col)
            ]["color"]
        squares[square_index(0, col)]["color"] = last_color


def marquee_north():
    for col in range(art_size):
        first_color = squares[square_index(0, col)]["color"]
        for row in range(art_size - 1):
            squares[square_index(row, col)]["color"] = squares[
                square_index(row + 1, col)
            ]["color"]
        squares[square_index(art_size - 1, col)]["color"] = first_color


def marquee_east():
    for row in range(art_size):
        last_color = squares[square_index(row, art_size - 1)]["color"]
        for col in range(art_size - 1, 0, -1):
            squares[square_index(row, col)]["color"] = squares[
                square_index(row, col - 1)
            ]["color"]
        squares[square_index(row, 0)]["color"] = last_color

# ---------------------------------------------------------
# Symmetry and random painter
# ---------------------------------------------------------
def autoSymmetryPainter():
    for row in range(art_size):
        for col in range(art_size // 2):
            left = square_index(row, col)
            right = square_index(row, art_size - col - 1)
            squares[right]["color"] = squares[left]["color"]


def autoSymmetryPainterReverse():
    for row in range(art_size):
        for col in range(art_size // 2):
            left = square_index(row, col)
            right = square_index(row, art_size - col - 1)
            squares[left]["color"] = squares[right]["color"]


def auto_art_painter():
    """Paint one random square in every column, regardless of grid size."""
    for col in range(art_size):
        row = random.randrange(art_size)
        squares[square_index(row, col)]["color"] = fg_color

# ---------------------------------------------------------
# Auto-color cycle
# ---------------------------------------------------------
def generate_same_shade_color(base_color):
    r, g, b = base_color
    delta = random.randint(-85, 85)
    return (
        max(0, min(255, r + delta)),
        max(0, min(255, g + delta)),
        max(0, min(255, b + delta)),
    )


def autoColorCycle():
    global fg_color, q_press_count
    q_press_count += 1
    if q_press_count % 2 == 0:
        fg_color = generate_same_shade_color(fg_color)
        fg_group.set_color(fg_color)
        print("Auto-color changed:", fg_color)

# ---------------------------------------------------------
# Blur
# ---------------------------------------------------------
def autoBlur():
    original = [square["color"] for square in squares]

    for col in range(art_size):
        for row in range(art_size):
            neighbors = []

            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = row + dr
                    cc = col + dc

                    if 0 <= rr < art_size and 0 <= cc < art_size:
                        neighbors.append(original[square_index(rr, cc)])

            squares[square_index(row, col)]["color"] = (
                sum(color[0] for color in neighbors) // len(neighbors),
                sum(color[1] for color in neighbors) // len(neighbors),
                sum(color[2] for color in neighbors) // len(neighbors),
            )

# ---------------------------------------------------------
# Sharpen and 9-color-block tools
# ---------------------------------------------------------
def autoSharpen():
    """Sharpen each grid color using a 3x3 unsharp-style neighborhood."""
    original = [square["color"] for square in squares]

    for col in range(art_size):
        for row in range(art_size):
            center = original[square_index(row, col)]
            neighbors = []

            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = row + dr
                    cc = col + dc
                    if 0 <= rr < art_size and 0 <= cc < art_size:
                        neighbors.append(original[square_index(rr, cc)])

            average = tuple(
                sum(color[channel] for color in neighbors) / len(neighbors)
                for channel in range(3)
            )

            sharpened = tuple(
                max(0, min(255, int(round(center[channel] * 2.0 - average[channel]))))
                for channel in range(3)
            )
            squares[square_index(row, col)]["color"] = sharpened


def paint_9_color_blocks():
    """Paint nine random 3x3 color blocks at random grid positions."""
    if art_size < 3:
        return

    for _ in range(9):
        start_row = random.randint(0, art_size - 3)
        start_col = random.randint(0, art_size - 3)
        block_color = (
            generate_same_shade_color(fg_color)
            if color_paint_mode_enabled
            else fg_color
        )

        for dr in range(3):
            for dc in range(3):
                squares[square_index(start_row + dr, start_col + dc)]["color"] = block_color

# ---------------------------------------------------------
# Artwork rendering and saving
# ---------------------------------------------------------
def render_art_surface():
    surface = pygame.Surface((ART_WIDTH, ART_HEIGHT))
    surface.fill((0, 0, 0))

    for square in squares:
        rect = get_square_draw_rect(
            square["row"],
            square["col"],
            local=True,
        )
        pygame.draw.rect(surface, square["color"], rect)

    return surface


def surface_to_image(surface):
    data = pygame.image.tostring(surface, "RGB")
    return Image.frombytes("RGB", surface.get_size(), data)


def save_picture_only():
    filename = make_timestamp_filename("png")
    pygame.image.save(render_art_surface(), filename)
    print("Saved:", filename)


def gif_frame():
    return surface_to_image(render_art_surface())


def save_gif(movement, frame_count):
    frames = []

    for _ in range(frame_count):
        movement()
        frames.append(gif_frame())
        pygame.event.pump()

    filename = make_timestamp_filename("gif")
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print("Saved:", filename)


def save_animation_gif_south():
    save_gif(marquee_south, art_size)


def save_animation_gif_east():
    save_gif(marquee_east, art_size)


def save_animation_gif_south_east():
    def movement():
        marquee_east()
        marquee_south()

    save_gif(movement, art_size * 2)


def save_animation_gif_north_east():
    def movement():
        marquee_east()
        marquee_north()

    save_gif(movement, art_size * 2)

# ---------------------------------------------------------
# UI classes
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
        surface.blit(text, (self.rect.x + 40, self.rect.y - 2))


class Slider:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        value=0,
        max_value=255,
        color=(200, 200, 200),
        callback=None,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_rect = pygame.Rect(x, y, 10, height)
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

    def set_value(self, value, call_callback=False):
        self.value = max(0, min(self.max_value, int(value)))
        self.update_knob()
        if call_callback and self.callback:
            self.callback(self.value)

    def set_from_mouse(self, mouse_x):
        new_x = max(
            self.rect.x,
            min(mouse_x, self.rect.right - self.knob_rect.width),
        )
        self.knob_rect.x = new_x
        ratio = (new_x - self.rect.x) / (
            self.rect.width - self.knob_rect.width
        )
        self.value = int(ratio * self.max_value)

        if self.callback:
            self.callback(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.set_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_from_mouse(event.pos[0])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            self.knob_rect,
            border_radius=4,
        )


class SliderGroup:
    def __init__(self, x, y, callback):
        self.callback = callback
        self.r = Slider(x, y, 300, 20, color=(255, 50, 50), callback=self.update)
        self.g = Slider(x, y + 40, 300, 20, color=(50, 255, 50), callback=self.update)
        self.b = Slider(x, y + 80, 300, 20, color=(50, 50, 255), callback=self.update)

    def update(self, unused_value):
        self.callback((self.r.value, self.g.value, self.b.value))

    def set_color(self, color):
        self.r.set_value(color[0])
        self.g.set_value(color[1])
        self.b.set_value(color[2])

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


class Dropdown:
    def __init__(
        self,
        x,
        y,
        width,
        values,
        selected,
        callback,
        visible_rows=10,
    ):
        self.rect = pygame.Rect(x, y, width, 34)
        self.values = list(values)
        self.selected = selected
        self.callback = callback
        self.visible_rows = visible_rows
        self.row_height = 28
        self.open = False
        self.scroll_index = max(0, self.values.index(selected) - visible_rows // 2)
        self.hover_index = None
        self.font = pygame.font.SysFont(None, 24)
        self.label_font = pygame.font.SysFont(None, 22)

    def maximum_scroll(self):
        return max(0, len(self.values) - self.visible_rows)

    def clamp_scroll(self):
        self.scroll_index = max(0, min(self.maximum_scroll(), self.scroll_index))

    def list_rect(self):
        row_count = min(self.visible_rows, len(self.values))
        return pygame.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            row_count * self.row_height,
        )

    def selected_text(self):
        return f"{self.selected} x {self.selected}"

    def toggle(self):
        self.open = not self.open
        if self.open:
            selected_index = self.values.index(self.selected)
            self.scroll_index = selected_index - self.visible_rows // 2
            self.clamp_scroll()

    def close(self):
        self.open = False
        self.hover_index = None

    def choose(self, value):
        self.selected = value
        self.close()
        if self.callback:
            self.callback(value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()
                return True

            if self.open:
                list_rect = self.list_rect()

                if event.button in (4, 5) and list_rect.collidepoint(event.pos):
                    direction = -1 if event.button == 4 else 1
                    self.scroll_index += direction
                    self.clamp_scroll()
                    return True

                if event.button == 1 and list_rect.collidepoint(event.pos):
                    local_y = event.pos[1] - list_rect.y
                    visible_index = local_y // self.row_height
                    value_index = self.scroll_index + visible_index

                    if 0 <= value_index < len(self.values):
                        self.choose(self.values[value_index])
                    return True

                if event.button == 1:
                    self.close()

        elif event.type == pygame.MOUSEWHEEL and self.open:
            mouse_pos = pygame.mouse.get_pos()
            if self.list_rect().collidepoint(mouse_pos):
                self.scroll_index -= event.y
                self.clamp_scroll()
                return True

        elif event.type == pygame.MOUSEMOTION and self.open:
            if self.list_rect().collidepoint(event.pos):
                local_y = event.pos[1] - self.list_rect().y
                visible_index = local_y // self.row_height
                value_index = self.scroll_index + visible_index
                if 0 <= value_index < len(self.values):
                    self.hover_index = value_index
                else:
                    self.hover_index = None
            else:
                self.hover_index = None

        elif event.type == pygame.KEYDOWN and self.open:
            selected_index = self.values.index(self.selected)

            if event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.key == pygame.K_UP:
                selected_index = max(0, selected_index - 1)
                self.selected = self.values[selected_index]
                self.scroll_index = min(self.scroll_index, selected_index)
                self.clamp_scroll()
                return True
            if event.key == pygame.K_DOWN:
                selected_index = min(len(self.values) - 1, selected_index + 1)
                self.selected = self.values[selected_index]
                if selected_index >= self.scroll_index + self.visible_rows:
                    self.scroll_index = selected_index - self.visible_rows + 1
                self.clamp_scroll()
                return True
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.choose(self.selected)
                return True

        return False

    def draw(self, surface):
        # Main closed control
        pygame.draw.rect(surface, (35, 35, 35), self.rect, border_radius=5)
        pygame.draw.rect(surface, (210, 210, 210), self.rect, 2, border_radius=5)

        text = self.font.render(self.selected_text(), True, (245, 245, 245))
        surface.blit(text, (self.rect.x + 10, self.rect.y + 7))

        arrow_x = self.rect.right - 18
        arrow_y = self.rect.centery
        if self.open:
            points = [
                (arrow_x - 5, arrow_y + 3),
                (arrow_x + 5, arrow_y + 3),
                (arrow_x, arrow_y - 4),
            ]
        else:
            points = [
                (arrow_x - 5, arrow_y - 3),
                (arrow_x + 5, arrow_y - 3),
                (arrow_x, arrow_y + 4),
            ]
        pygame.draw.polygon(surface, (235, 235, 235), points)

        if not self.open:
            return

        # Dropdown list
        list_rect = self.list_rect()
        pygame.draw.rect(surface, (24, 24, 24), list_rect)
        pygame.draw.rect(surface, (220, 220, 220), list_rect, 2)

        end_index = min(
            len(self.values),
            self.scroll_index + self.visible_rows,
        )

        for visible_row, value_index in enumerate(
            range(self.scroll_index, end_index)
        ):
            value = self.values[value_index]
            row_rect = pygame.Rect(
                list_rect.x + 2,
                list_rect.y + visible_row * self.row_height + 1,
                list_rect.width - 4,
                self.row_height,
            )

            if value_index == self.hover_index:
                pygame.draw.rect(surface, (75, 75, 75), row_rect)
            elif value == self.selected:
                pygame.draw.rect(surface, (55, 85, 120), row_rect)

            row_text = self.label_font.render(
                f"{value} x {value}",
                True,
                (245, 245, 245),
            )
            surface.blit(row_text, (row_rect.x + 8, row_rect.y + 4))

        # Compact scrollbar
        if len(self.values) > self.visible_rows:
            track_rect = pygame.Rect(
                list_rect.right - 8,
                list_rect.y + 3,
                5,
                list_rect.height - 6,
            )
            pygame.draw.rect(surface, (70, 70, 70), track_rect)

            thumb_height = max(
                18,
                int(track_rect.height * self.visible_rows / len(self.values)),
            )
            travel = track_rect.height - thumb_height
            ratio = self.scroll_index / max(1, self.maximum_scroll())
            thumb_rect = pygame.Rect(
                track_rect.x,
                track_rect.y + int(travel * ratio),
                track_rect.width,
                thumb_height,
            )
            pygame.draw.rect(surface, (210, 210, 210), thumb_rect)

# ---------------------------------------------------------
# UI callbacks
# ---------------------------------------------------------
def on_fg_change(new_color):
    global fg_color
    fg_color = new_color


def on_bg_change(new_color):
    global bg_color
    bg_color = new_color


def toggle_auto_color(checked):
    global auto_color_enabled
    auto_color_enabled = checked


def toggle_color_paint_mode(checked):
    global color_paint_mode_enabled
    color_paint_mode_enabled = checked


def on_art_size_change(new_size):
    # Only rebuild grid density. Window and artwork stay fixed.
    build_grid(new_size)


fg_group = SliderGroup(50, 40, on_fg_change)
bg_group = SliderGroup(50, 180, on_bg_change)
mode_group = CheckboxGroup()
auto_color_checkbox = Checkbox(
    50,
    420,
    "Auto Color Cycle",
    False,
    toggle_auto_color,
)
color_paint_checkbox = Checkbox(
    50,
    460,
    "Color Paint Mode",
    False,
    toggle_color_paint_mode,
)
art_size_dropdown = Dropdown(
    50,
    550,
    300,
    range(MIN_ART_SIZE, MAX_ART_SIZE + 1),
    DEFAULT_ART_SIZE,
    on_art_size_change,
    visible_rows=7,
)
ui_font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)

# ---------------------------------------------------------
# Painting
# ---------------------------------------------------------
def square_at_position(position):
    mouse_x, mouse_y = position

    if not (
        ART_X <= mouse_x < ART_X + ART_WIDTH
        and ART_Y <= mouse_y < ART_Y + ART_HEIGHT
    ):
        return None

    local_x = mouse_x - ART_X
    local_y = mouse_y - ART_Y
    col = min(art_size - 1, (local_x * art_size) // ART_WIDTH)
    row = min(art_size - 1, (local_y * art_size) // ART_HEIGHT)
    return squares[square_index(row, col)]


def paint_square(square, erase=False):
    if erase or mode_group.is_erase_mode():
        square["color"] = canvas_color
    elif mode_group.is_paint_mode():
        if color_paint_mode_enabled:
            square["color"] = generate_same_shade_color(fg_color)
        else:
            square["color"] = fg_color


def handle_square_click(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    square = square_at_position(event.pos)
    if square is None:
        return

    if event.button == 3:
        paint_square(square, erase=True)
    elif event.button == 1:
        paint_square(square)


def handle_hover_paint(position, erase=False):
    square = square_at_position(position)
    if square is not None:
        paint_square(square, erase=erase)

# ---------------------------------------------------------
# Drawing
# ---------------------------------------------------------
def draw_artwork(surface):
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        (ART_X, ART_Y, ART_WIDTH, ART_HEIGHT),
    )

    for square in squares:
        rect = get_square_draw_rect(square["row"], square["col"])
        pygame.draw.rect(surface, square["color"], rect)

    pygame.draw.rect(
        surface,
        (160, 160, 160),
        (ART_X - 1, ART_Y - 1, ART_WIDTH + 2, ART_HEIGHT + 2),
        1,
    )


def draw_ui(surface):
    fg_group.draw(surface)
    bg_group.draw(surface)
    mode_group.draw(surface)
    auto_color_checkbox.draw(surface)
    color_paint_checkbox.draw(surface)

    label = ui_font.render("Art Size", True, (235, 235, 235))
    surface.blit(label, (50, 520))

    help_lines = [
        "Choose any size from 20 to 100",
        "Mouse wheel scrolls the open list",
        "Grid changes inside the fixed 600 x 600 artwork area",
        "H = Sharpen    J = nine 3x3 color blocks",
    ]
    for index, line in enumerate(help_lines):
        text = small_font.render(line, True, (185, 185, 185))
        surface.blit(text, (50, 600 + index * 22))

    # Draw last so the open list appears above other controls.
    art_size_dropdown.draw(surface)

# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------
def main():
    running = True

    while running:
        for event in pygame.event.get():
            # These are normal window-management events. They must never close,
            # resize, or rebuild the artwork.
            harmless_window_events = (
                pygame.WINDOWMOVED,
                pygame.WINDOWMINIMIZED,
                pygame.WINDOWMAXIMIZED,
                pygame.WINDOWRESTORED,
                pygame.WINDOWSHOWN,
                pygame.WINDOWHIDDEN,
                pygame.WINDOWEXPOSED,
                pygame.WINDOWFOCUSGAINED,
                pygame.WINDOWFOCUSLOST,
                pygame.WINDOWENTER,
                pygame.WINDOWLEAVE,
                pygame.WINDOWRESIZED,
                pygame.WINDOWSIZECHANGED,
            )

            if event.type in harmless_window_events:
                continue

            # SDL may emit a display-change notification when crossing monitors.
            # It is informational only; never rebuild or resize the window for it.
            window_display_changed = getattr(pygame, "WINDOWDISPLAYCHANGED", None)
            if window_display_changed is not None and event.type == window_display_changed:
                continue

            if event.type in (pygame.WINDOWCLOSE, QUIT):
                running = False
                continue

            dropdown_used = art_size_dropdown.handle_event(event)

            if not dropdown_used and not art_size_dropdown.open:
                fg_group.handle_event(event)
                bg_group.handle_event(event)
                mode_group.handle_event(event)
                auto_color_checkbox.handle_event(event)
                color_paint_checkbox.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_square_click(event)

            if event.type == KEYDOWN and not art_size_dropdown.open:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_q:
                    auto_art_painter()
                    if auto_color_enabled:
                        autoColorCycle()
                elif event.key == K_w:
                    autoSymmetryPainter()
                elif event.key == K_e:
                    autoSymmetryPainterReverse()
                elif event.key == K_p:
                    for square in squares:
                        square["color"] = canvas_color
                elif event.key == K_b:
                    autoBlur()
                elif event.key == K_h:
                    autoSharpen()
                elif event.key == K_j:
                    paint_9_color_blocks()
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

        # Keep processing events while minimized, but skip rendering until
        # Windows restores the display surface.
        if pygame.display.get_surface() is None or not pygame.display.get_init():
            clock.tick(15)
            continue

        screen.fill(bg_color)

        if not art_size_dropdown.open:
            mouse_buttons = pygame.mouse.get_pressed(3)
            mouse_position = pygame.mouse.get_pos()

            if mouse_buttons[0]:
                handle_hover_paint(mouse_position)
            elif mouse_buttons[2]:
                handle_hover_paint(mouse_position, erase=True)

        draw_artwork(screen)
        draw_ui(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
