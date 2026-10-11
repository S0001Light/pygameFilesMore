from PIL import Image
import pygame
from pygame.locals import *
import sys
import datetime
import random
import os

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
pygame.init()

# Fixed non-resizable window sized for the 75 x 25 grid.
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1000
FIXED_WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(FIXED_WINDOW_SIZE, 0, 32)
pygame.display.set_caption(
    "Writers Jumbler 75 Art + Pygame Calculator, "
    "Q,A,D=First,W,E=Symmetry,P=Erase,V,B,C,X,J,G=Blur,"
    "F,H,V,Z=Sharpen,S=Save,L,K=Save GIF,O,I=Preview"
)

fg_color = (0, 0, 0)
bg_color = (0, 0, 0)
squares = []
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0

GRID_ROWS = 25
GRID_COLS = 75
GRID_SIZE = 15
GRID_GAP = 5
GRID_START_X = 405
GRID_START_Y = 20

SAVE_W = GRID_COLS * (GRID_SIZE + GRID_GAP)
SAVE_H = GRID_ROWS * (GRID_SIZE + GRID_GAP)

current_page_offset = 0
page_mode_direction = "east"
preview_mode_enabled = False
number_line_list = []

os.makedirs("art", exist_ok=True)

# ---------------------------------------------------------
# Number line helpers
# ---------------------------------------------------------
def normalize_result(n):
    """Keep generated row values within the current 1-to-25 grid height."""
    try:
        n = int(n)
    except (TypeError, ValueError, OverflowError):
        return random.randint(1, GRID_ROWS)

    if 1 <= n <= GRID_ROWS:
        return n
    return random.randint(1, GRID_ROWS)


def append_number_line(new_values):
    global number_line_list
    number_line_list.extend(new_values)
    print("Updated number line:", number_line_list)
    return number_line_list


def generate_equations_for_pair(a, b):
    results = [a + b, a - b, b - a, a * b]
    if b != 0:
        results.append(a / b)
    if a != 0:
        results.append(b / a)
    results.extend([(a + b) / 2, abs(a - b), a * a, b * b, a, b, b, a])
    return [normalize_result(r) for r in results]


def generate_from_numbers(numbers):
    all_results = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            all_results.extend(generate_equations_for_pair(numbers[i], numbers[j]))
    return all_results

# ---------------------------------------------------------
# Build Grid
# ---------------------------------------------------------
def build_grid():
    global squares
    squares = []
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS):
            x = GRID_START_X + col * (GRID_SIZE + GRID_GAP)
            y = GRID_START_Y + row * (GRID_SIZE + GRID_GAP)
            squares.append({"rect": pygame.Rect(x, y, GRID_SIZE, GRID_SIZE),
                            "color": (255, 255, 255)})


build_grid()

# ---------------------------------------------------------
# Virtual Page System
# ---------------------------------------------------------
def get_virtual_color(index):
    r = index % GRID_ROWS
    c = index // GRID_ROWS
    if page_mode_direction == "east":
        c = (c + current_page_offset) % GRID_COLS
    else:
        r = (r + current_page_offset) % GRID_ROWS
    return squares[r + c * GRID_ROWS]["color"]

# ---------------------------------------------------------
# Marquee Functions
# ---------------------------------------------------------
def marquee_south():
    for col in range(GRID_COLS):
        last = squares[(GRID_ROWS - 1) + col * GRID_ROWS]["color"]
        for row in range(GRID_ROWS - 1, 0, -1):
            squares[row + col * GRID_ROWS]["color"] = squares[(row - 1) + col * GRID_ROWS]["color"]
        squares[col * GRID_ROWS]["color"] = last


def marquee_east():
    for row in range(GRID_ROWS):
        last = squares[row + (GRID_COLS - 1) * GRID_ROWS]["color"]
        for col in range(GRID_COLS - 1, 0, -1):
            squares[row + col * GRID_ROWS]["color"] = squares[row + (col - 1) * GRID_ROWS]["color"]
        squares[row]["color"] = last

# ---------------------------------------------------------
# Save and preview
# ---------------------------------------------------------
def grid_surface():
    surf = pygame.Surface((SAVE_W, SAVE_H))
    surf.fill((255, 255, 255))
    for sq in squares:
        shifted = sq["rect"].move(-GRID_START_X, -GRID_START_Y)
        pygame.draw.rect(surf, sq["color"], shifted)
    return surf


def save_picture_only():
    filename = datetime.datetime.now().strftime(
        "art/WritersJumbler_75_Art_%m-%d-%Y-%I-%M-%S-%p.png")
    pygame.image.save(grid_surface(), filename)
    print("Saved:", filename)


def gif_frame():
    surf = grid_surface()
    data = pygame.image.tostring(surf, "RGB")
    return Image.frombytes("RGB", surf.get_size(), data)


def draw_grid_now():
    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])
    pygame.display.update()


def save_animation_gif_south():
    frames = []
    for _ in range(GRID_ROWS):
        marquee_south()
        draw_grid_now()
        pygame.time.delay(30)
        frames.append(gif_frame())
    filename = datetime.datetime.now().strftime(
        "art/WritersJumbler_75_Art_South_%m-%d-%Y-%I-%M-%S-%p.gif")
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=50, loop=0)
    print("Saved:", filename)


def save_animation_gif_east():
    frames = []
    for _ in range(GRID_COLS):
        marquee_east()
        draw_grid_now()
        pygame.time.delay(30)
        frames.append(gif_frame())
    filename = datetime.datetime.now().strftime(
        "art/WritersJumbler_75_Art_East_%m-%d-%Y-%I-%M-%S-%p.gif")
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=150, loop=0)
    print("Saved:", filename)


def preview_animation_south():
    for _ in range(GRID_ROWS):
        marquee_south()
        draw_grid_now()
        pygame.time.delay(30)


def preview_animation_east():
    for _ in range(GRID_COLS):
        marquee_east()
        draw_grid_now()
        pygame.time.delay(30)

# ---------------------------------------------------------
# Auto Functions
# ---------------------------------------------------------
def autoSymmetryPainter():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS // 2):
            squares[row + (GRID_COLS - col - 1) * GRID_ROWS]["color"] = squares[row + col * GRID_ROWS]["color"]


def autoSymmetryPainterReverse():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS // 2):
            squares[row + col * GRID_ROWS]["color"] = squares[row + (GRID_COLS - col - 1) * GRID_ROWS]["color"]


def choose_row():
    if number_line_list:
        return normalize_result(random.choice(number_line_list))
    return random.randint(1, GRID_ROWS)


def autoA75():
    for col in range(GRID_COLS):
        squares[(choose_row() - 1) + col * GRID_ROWS]["color"] = fg_color


def autoB75():
    for col in range(GRID_COLS):
        row = choose_row() - 1
        squares[row + col * GRID_ROWS]["color"] = fg_color
        shade = tuple(max(channel - 40, 0) for channel in fg_color)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                squares[nr + nc * GRID_ROWS]["color"] = shade


def random_shade(color):
    r, g, b = color
    mode = random.choice(["dark", "light", "sat+", "sat-", "hue"])
    if mode == "dark":
        factor = random.uniform(0.5, 0.85)
        return tuple(int(v * factor) for v in (r, g, b))
    if mode == "light":
        factor = random.uniform(1.1, 1.4)
        return tuple(min(int(v * factor), 255) for v in (r, g, b))
    if mode == "sat+":
        boost = random.randint(20, 50)
        return tuple(min(v + boost, 255) for v in (r, g, b))
    if mode == "sat-":
        drop = random.randint(20, 50)
        return tuple(max(v - drop, 0) for v in (r, g, b))
    shift = random.randint(-25, 25)
    return tuple(max(0, min(v + shift, 255)) for v in (r, g, b))


def autoC75():
    for col in range(GRID_COLS):
        row = choose_row() - 1
        squares[row + col * GRID_ROWS]["color"] = fg_color
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                squares[nr + nc * GRID_ROWS]["color"] = random_shade(fg_color)


def generate_same_shade_color(base):
    d = random.randint(-55, 55)
    return tuple(max(0, min(255, value + d)) for value in base)


def autoColorCycle():
    global fg_color, q_press_count
    q_press_count += 1
    if q_press_count % 2 == 0:
        fg_color = generate_same_shade_color(fg_color)


def erase_all():
    for sq in squares:
        sq["color"] = (255, 255, 255)


def neighborhood(original, r, c):
    colors = []
    for dc in (-1, 0, 1):
        for dr in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                colors.append(original[rr + cc * GRID_ROWS])
    return colors


def autoBlur1():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            colors = neighborhood(original, r, c)
            squares[r + c * GRID_ROWS]["color"] = tuple(
                sum(v[i] for v in colors) // len(colors) for i in range(3))


def autoBlur2():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            colors = neighborhood(original, r, c)
            avg = [sum(v[i] for v in colors) / len(colors) for i in range(3)]
            orig = original[r + c * GRID_ROWS]
            squares[r + c * GRID_ROWS]["color"] = tuple(
                int(orig[i] * 0.5 + avg[i] * 0.5) for i in range(3))


def autoGaussianBlur():
    original = [sq["color"] for sq in squares]
    weights = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            accum = [0, 0, 0]
            used_weight = 0
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        w = weights[dr + 1][dc + 1]
                        color = original[rr + cc * GRID_ROWS]
                        used_weight += w
                        for i in range(3):
                            accum[i] += color[i] * w
            squares[r + c * GRID_ROWS]["color"] = tuple(v // used_weight for v in accum)


def autoSharpen():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            colors = neighborhood(original, r, c)
            avg = [sum(v[i] for v in colors) / len(colors) for i in range(3)]
            orig = original[r + c * GRID_ROWS]
            squares[r + c * GRID_ROWS]["color"] = tuple(
                max(0, min(255, int(orig[i] * 1.5 - avg[i] * 0.5))) for i in range(3))


def autoEdgeDetect():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            center = original[r + c * GRID_ROWS]
            edges = 0
            for neigh in neighborhood(original, r, c):
                edges += sum(abs(center[i] - neigh[i]) for i in range(3))
            val = min(edges // 8, 255)
            squares[r + c * GRID_ROWS]["color"] = (val, val, val)


def autoPixelate(block=3):
    original = [sq["color"] for sq in squares]
    for c in range(0, GRID_COLS, block):
        for r in range(0, GRID_ROWS, block):
            sample = original[r + c * GRID_ROWS]
            for cc in range(c, min(c + block, GRID_COLS)):
                for rr in range(r, min(r + block, GRID_ROWS)):
                    squares[rr + cc * GRID_ROWS]["color"] = sample


def autoEmboss():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            rr, cc = min(r + 1, GRID_ROWS - 1), min(c + 1, GRID_COLS - 1)
            orig = original[r + c * GRID_ROWS]
            neigh = original[rr + cc * GRID_ROWS]
            squares[r + c * GRID_ROWS]["color"] = tuple(
                max(0, min(255, 128 + orig[i] - neigh[i])) for i in range(3))


def autoBloom():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            orig = original[r + c * GRID_ROWS]
            strength = sum(orig) / 765
            glow = [0, 0, 0]
            for neigh in neighborhood(original, r, c):
                for i in range(3):
                    glow[i] += neigh[i] * strength
            squares[r + c * GRID_ROWS]["color"] = tuple(
                min(int(orig[i] + glow[i] * 0.1), 255) for i in range(3))


def autoMedianBlur():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            colors = neighborhood(original, r, c)
            channels = [sorted(color[i] for color in colors) for i in range(3)]
            middle = len(colors) // 2
            squares[r + c * GRID_ROWS]["color"] = tuple(ch[middle] for ch in channels)


def autoMedianSharpen():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            colors = neighborhood(original, r, c)
            channels = [sorted(color[i] for color in colors) for i in range(3)]
            middle = len(colors) // 2
            median = tuple(ch[middle] for ch in channels)
            orig = original[r + c * GRID_ROWS]
            squares[r + c * GRID_ROWS]["color"] = tuple(
                max(0, min(255, int(orig[i] * 1.3 - median[i] * 0.3))) for i in range(3))


def copyTopToBottom():
    original = [sq["color"] for sq in squares]
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS // 2):
            squares[(GRID_ROWS - row - 1) + col * GRID_ROWS]["color"] = original[row + col * GRID_ROWS]


def copyBottomToTop():
    original = [sq["color"] for sq in squares]
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS // 2):
            squares[row + col * GRID_ROWS]["color"] = original[(GRID_ROWS - row - 1) + col * GRID_ROWS]

# ---------------------------------------------------------
# UI Classes
# ---------------------------------------------------------
class Checkbox:
    def __init__(self, x, y, label, checked=False, callback=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = checked
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.checked = not self.checked
            if self.callback:
                self.callback(self.checked)

    def draw(self, surf):
        pygame.draw.rect(surf, (230, 230, 230), self.rect, 2)
        if self.checked:
            pygame.draw.line(surf, (230, 230, 230),
                             (self.rect.x + 4, self.rect.y + 10),
                             (self.rect.x + 10, self.rect.y + 16), 3)
            pygame.draw.line(surf, (230, 230, 230),
                             (self.rect.x + 10, self.rect.y + 16),
                             (self.rect.x + 16, self.rect.y + 4), 3)
        font = pygame.font.SysFont(None, 24)
        surf.blit(font.render(self.label, True, (230, 230, 230)),
                  (self.rect.x + 50, self.rect.y - 2))


class Slider:
    def __init__(self, x, y, w, h, value=0, max_value=255,
                 color=(200, 200, 200), callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.knob = pygame.Rect(x, y, 10, h)
        self.max_value = max_value
        self.value = value
        self.color = color
        self.dragging = False
        self.callback = callback
        self.update_knob()

    def update_knob(self):
        ratio = self.value / self.max_value
        self.knob.x = self.rect.x + int(ratio * (self.rect.width - self.knob.width))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.knob.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x, min(event.pos[0], self.rect.right - self.knob.width))
            self.knob.x = new_x
            ratio = (self.knob.x - self.rect.x) / (self.rect.width - self.knob.width)
            self.value = int(ratio * self.max_value)
            if self.callback:
                self.callback(self.value)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surf, (255, 255, 255), self.knob, border_radius=4)


class SliderGroup:
    def __init__(self, x, y, callback):
        self.callback = callback
        self.r = Slider(x, y, 300, 20, color=(205, 50, 50), callback=self.update)
        self.g = Slider(x, y + 40, 300, 20, color=(50, 205, 50), callback=self.update)
        self.b = Slider(x, y + 80, 300, 20, color=(50, 50, 205), callback=self.update)

    def update(self, _):
        self.callback((self.r.value, self.g.value, self.b.value))

    def handle_event(self, event):
        self.r.handle_event(event)
        self.g.handle_event(event)
        self.b.handle_event(event)

    def draw(self, surf):
        self.r.draw(surf)
        self.g.draw(surf)
        self.b.draw(surf)


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

    def draw(self, surf):
        self.paint.draw(surf)
        self.erase.draw(surf)

    def is_paint_mode(self):
        return self.paint.checked

    def is_erase_mode(self):
        return self.erase.checked

# ---------------------------------------------------------
# Calculator UI
# ---------------------------------------------------------
class CalculatorUI:
    def __init__(self, x, y):
        self.x = x - 30
        self.y = y + 180
        self.font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.label_font = pygame.font.SysFont("Courier New", 18, bold=True)
        self.entry_text = ""
        self.display_text = ""
        self.buttons = []
        self.display_rect = pygame.Rect(self.x, self.y, 300, 40)
        self.label_text = "Seven Numbers, separate with comma"
        self.hover_button = None
        self.build_buttons()

    def build_buttons(self):
        w, h = 50, 40
        start_y = self.y + 60
        digits = [("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
                  ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
                  ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
                  ("0", 3, 0)]
        for text, row, col in digits:
            rect = pygame.Rect(self.x + col * (w + 10),
                               start_y + row * (h + 10), w, h)
            self.buttons.append(("digit", text, rect))
        self.buttons.append(("generate", "GEN", pygame.Rect(self.x + 180, start_y, 90, h)))
        self.buttons.append(("clear", "CLR", pygame.Rect(self.x + 180, start_y + 50, 90, h)))
        self.buttons.append(("comma", ",", pygame.Rect(self.x + 180, start_y + 100, 90, h)))

    def handle_event(self, event):
        global number_line_list
        if event.type == pygame.MOUSEMOTION:
            self.hover_button = None
            for _, _, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    self.hover_button = rect
                    break

        if event.type == pygame.KEYDOWN:
            if pygame.K_KP0 <= event.key <= pygame.K_KP9:
                self.add_digit(event.key - pygame.K_KP0)
            elif pygame.K_0 <= event.key <= pygame.K_9:
                self.add_digit(event.key - pygame.K_0)
            elif event.key == pygame.K_BACKSPACE:
                self.entry_text = self.entry_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.generate_equations()
            elif event.key == pygame.K_COMMA:
                self.add_comma()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for kind, text, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    if kind == "digit":
                        self.add_digit(int(text))
                    elif kind == "generate":
                        self.generate_equations()
                    elif kind == "clear":
                        number_line_list = []
                        self.entry_text = ""
                        self.display_text = ""
                    elif kind == "comma":
                        self.add_comma()
                    break

    def add_digit(self, digit):
        self.entry_text += str(digit)

    def add_comma(self):
        if self.entry_text and self.entry_text[-1].isdigit():
            self.entry_text += ", "

    def generate_equations(self):
        try:
            nums = [int(n.strip()) for n in self.entry_text.split(",") if n.strip()]
        except ValueError:
            self.display_text = "ERR"
            return
        if len(nums) < 2:
            self.display_text = "Need >=2 nums"
            return
        append_number_line(generate_from_numbers(nums))
        self.display_text = "Added"
        self.entry_text = ""

    def draw(self, surf):
        panel_rect = pygame.Rect(self.x - 10, self.y - 40, 380, 300)
        pygame.draw.rect(surf, (20, 20, 20), panel_rect)
        pygame.draw.rect(surf, (255, 255, 0), panel_rect, 4)
        pygame.draw.rect(surf, (120, 120, 0), panel_rect, 2)
        label = self.label_font.render(self.label_text, True, (255, 255, 0))
        surf.blit(label, (self.x, self.y - 25))
        pygame.draw.rect(surf, (40, 40, 40), self.display_rect)
        pygame.draw.rect(surf, (200, 200, 200), self.display_rect, 2)
        entry = self.font.render(self.entry_text, True, (0, 255, 200))
        surf.blit(entry, (self.display_rect.x + 5, self.display_rect.y + 8))
        for _, text, rect in self.buttons:
            pygame.draw.rect(surf, (100, 100, 100) if rect == self.hover_button else (60, 60, 60), rect)
            pygame.draw.rect(surf, (200, 200, 200), rect, 2)
            surf.blit(self.font.render(text, True, (0, 255, 200)), (rect.x + 10, rect.y + 8))
        surf.blit(self.font.render(self.display_text, True, (0, 255, 200)),
                  (self.x, self.y + 45))

# ---------------------------------------------------------
# UI Instances
# ---------------------------------------------------------
fg_group = SliderGroup(50, 40, lambda c: globals().__setitem__("fg_color", c))
bg_group = SliderGroup(50, 180, lambda c: globals().__setitem__("bg_color", c))
mode_group = CheckboxGroup()
auto_color_checkbox = Checkbox(
    50, 440, "Auto Color Cycle", False,
    lambda c: globals().__setitem__("auto_color_enabled", c))
color_paint_checkbox = Checkbox(
    50, 480, "Color Paint Mode", False,
    lambda c: globals().__setitem__("color_paint_mode_enabled", c))
calculator = CalculatorUI(50, 540)


def saveCRT(crt_output, filename="crt_output.bmp"):
    surf = pygame.Surface((GRID_COLS, GRID_ROWS))
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            surf.set_at((c, r), crt_output[r + c * GRID_ROWS])
    pygame.image.save(surf, filename)
    print("Saved CRT image:", filename)

# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            continue

        # If Windows sends a resize/maximize event, restore the fixed display.
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(FIXED_WINDOW_SIZE, 0, 32)
            continue

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_q:
                autoA75()
                if auto_color_enabled:
                    autoColorCycle()
            elif event.key == K_a:
                autoB75()
                if auto_color_enabled:
                    autoColorCycle()
            elif event.key == K_d:
                autoC75()
                if auto_color_enabled:
                    autoColorCycle()
            elif event.key == K_f:
                autoSharpen()
            elif event.key == K_g:
                autoGaussianBlur()
            elif event.key == K_h:
                autoEdgeDetect()
            elif event.key == K_j:
                autoPixelate()
            elif event.key == K_z:
                autoEmboss()
            elif event.key == K_x:
                autoBloom()
            elif event.key == K_c:
                autoMedianBlur()
            elif event.key == K_v:
                autoMedianSharpen()
            elif event.key == K_w:
                autoSymmetryPainter()
            elif event.key == K_e:
                autoSymmetryPainterReverse()
            elif event.key == K_r:
                copyTopToBottom()
            elif event.key == K_t:
                copyBottomToTop()
            elif event.key == K_s:
                save_picture_only()
            elif event.key == K_p:
                erase_all()
            elif event.key == K_b:
                autoBlur2()
            elif event.key == K_l:
                save_animation_gif_south()
            elif event.key == K_k:
                save_animation_gif_east()
            elif event.key == K_o:
                preview_animation_south()
            elif event.key == K_i:
                preview_animation_east()

        fg_group.handle_event(event)
        bg_group.handle_event(event)
        mode_group.handle_event(event)
        auto_color_checkbox.handle_event(event)
        color_paint_checkbox.handle_event(event)
        calculator.handle_event(event)

    screen.fill(bg_color)

    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])

    fg_group.draw(screen)
    bg_group.draw(screen)
    mode_group.draw(screen)
    auto_color_checkbox.draw(screen)
    color_paint_checkbox.draw(screen)
    calculator.draw(screen)

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        for sq in squares:
            if sq["rect"].collidepoint(mouse_pos):
                if mode_group.is_paint_mode():
                    sq["color"] = (generate_same_shade_color(fg_color)
                                   if color_paint_mode_enabled else fg_color)
                elif mode_group.is_erase_mode():
                    sq["color"] = (255, 255, 255)
                break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
