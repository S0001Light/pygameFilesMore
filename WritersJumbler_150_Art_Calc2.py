# =========================
# PART 1 OF 2
# =========================
from PIL import Image
import pygame
from pygame.locals import *
import sys
import datetime
import random

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((3500, 1000), 0, 32)
pygame.display.set_caption("Writers Jumbler 150 Art + Pygame Calculator,Q,A,D=First,W,E=Symmetry,P=Erase,V,B,C,X,J,G=Blur,F,H,V,Z=Sharpen,S,F10=Save,L,K=Save,F9=CRT,O,I=Preview")

fg_color = (0, 0, 0)
bg_color = (0, 0, 0)
squares = []
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0

GRID_ROWS = 50
GRID_COLS = 150
GRID_SIZE = 15
GRID_GAP = 5
GRID_START_X = 405
GRID_START_Y = 20

SAVE_W = GRID_COLS * (GRID_SIZE + GRID_GAP)
SAVE_H = GRID_ROWS * (GRID_SIZE + GRID_GAP)

current_page_offset = 0
page_mode_direction = "east"
preview_mode_enabled = False

# Number line list (random source)
number_line_list = []

# ---------------------------------------------------------
# Number line helpers
# ---------------------------------------------------------
def normalize_result(n):
    """If result is not 1–50, auto-generate a random number 1–50."""
    try:
        n = int(n)
    except:
        return random.randint(1, 50)

    if 1 <= n <= 50:
        return n
    else:
        return random.randint(1, 50)


def append_number_line(new_values):
    """Append new values to the global number_line_list."""
    global number_line_list
    number_line_list.extend(new_values)
    print("Updated number line:", number_line_list)
    return number_line_list


def generate_equations_for_pair(a, b):
    """Generate MANY equations for a pair (a,b)."""
    results = []

    # Basic
    results.append(a + b)
    results.append(a - b)
    results.append(b - a)
    results.append(a * b)

    # Safe divisions
    if b != 0:
        results.append(a / b)
    if a != 0:
        results.append(b / a)

    # Extra equations
    results.append((a + b) / 2)      # average
    results.append(abs(a - b))       # absolute difference
    results.append(a * a)            # a^2
    results.append(b * b)            # b^2
    results.append(a)
    results.append(b)
    results.append(b)
    results.append(a)

    # Normalize all
    return [normalize_result(r) for r in results]


def generate_from_numbers(numbers):
    """Option C: use ALL combinations of numbers in pairs."""
    all_results = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            a = numbers[i]
            b = numbers[j]
            all_results.extend(generate_equations_for_pair(a, b))
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
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            squares.append({"rect": rect, "color": (255, 255, 255)})


build_grid()


# ---------------------------------------------------------
# Virtual Page System
# ---------------------------------------------------------
def get_virtual_color(index):
    rows = GRID_ROWS
    cols = GRID_COLS
    r = index % rows
    c = index // rows

    if page_mode_direction == "east":
        c = (c + current_page_offset) % cols
    else:
        r = (r + current_page_offset) % rows

    return squares[r + c * rows]["color"]


# ---------------------------------------------------------
# Marquee Functions
# ---------------------------------------------------------
def marquee_south():
    rows = GRID_ROWS
    cols = GRID_COLS
    for col in range(cols):
        last = squares[(rows - 1) + col * rows]["color"]
        for row in range(rows - 1, 0, -1):
            squares[row + col * rows]["color"] = squares[(row - 1) + col * rows]["color"]
        squares[col * rows]["color"] = last


def marquee_east():
    rows = GRID_ROWS
    cols = GRID_COLS
    for row in range(rows):
        last = squares[row + (cols - 1) * rows]["color"]
        for col in range(cols - 1, 0, -1):
            squares[row + col * rows]["color"] = squares[row + (col - 1) * rows]["color"]
        squares[row]["color"] = last


# ---------------------------------------------------------
# Save PNG
# ---------------------------------------------------------
def save_picture_only():
    surf = pygame.Surface((SAVE_W, SAVE_H))
    for sq in squares:
        shifted = sq["rect"].move(-GRID_START_X, -GRID_START_Y)
        pygame.draw.rect(surf, sq["color"], shifted)
    filename = datetime.datetime.now().strftime("art/WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.png")
    pygame.image.save(surf, filename)
    print("Saved:", filename)


# ---------------------------------------------------------
# Save GIF
# ---------------------------------------------------------
def gif_frame():
    surf = pygame.Surface((SAVE_W, SAVE_H))
    for sq in squares:
        shifted = sq["rect"].move(-GRID_START_X, -GRID_START_Y)
        pygame.draw.rect(surf, sq["color"], shifted)
    data = pygame.image.tostring(surf, "RGB")
    return Image.frombytes("RGB", surf.get_size(), data)


def save_animation_gif_south():
    for _ in range(current_page_offset):
        marquee_south()

    frames = []
    for _ in range(GRID_ROWS):
        marquee_south()
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])
        pygame.display.update()
        pygame.time.delay(30)
        frames.append(gif_frame())

    filename = datetime.datetime.now().strftime("art/WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.gif")
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=50, loop=0)
    print("Saved:", filename)


def save_animation_gif_east():
    for _ in range(current_page_offset):
        marquee_east()

    frames = []
    for _ in range(GRID_COLS):
        marquee_east()
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])
        pygame.display.update()
        pygame.time.delay(30)
        frames.append(gif_frame())

    filename = datetime.datetime.now().strftime("art/WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.gif")
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=150, loop=0)
    print("Saved:", filename)

# ---------------------------------------------------------
# GIF Preview (Option B)
# ---------------------------------------------------------
def preview_animation_south():
    for _ in range(current_page_offset):
        marquee_south()

    for _ in range(GRID_ROWS):
        marquee_south()
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])
        pygame.display.update()
        pygame.time.delay(30)

def preview_animation_east():
    for _ in range(current_page_offset):
        marquee_east()

    for _ in range(GRID_COLS):
        marquee_east()
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])
        pygame.display.update()
        pygame.time.delay(30)
        
# ---------------------------------------------------------
# Auto Functions
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


def autoA150():
    for col in range(GRID_COLS):
        if number_line_list:
            r = random.choice(number_line_list)
        else:
            r = random.randint(1, 50)
        idx = r - 1 + col * GRID_ROWS
        squares[idx]["color"] = fg_color

def autoB150():
    for col in range(GRID_COLS):
        # Pick row from number_line_list or random
        if number_line_list:
            r = random.choice(number_line_list)
        else:
            r = random.randint(1, GRID_ROWS)

        idx = (r - 1) + col * GRID_ROWS
        squares[idx]["color"] = fg_color

        # --- Wrap effect ---
        base = fg_color
        shade = (
            max(base[0] - 40, 0),
            max(base[1] - 40, 0),
            max(base[2] - 40, 0)
        )

        row = r - 1
        neighbors = [
            (row - 1, col),     # up
            (row + 1, col),     # down
            (row, col - 1),     # left
            (row, col + 1),     # right
            (row - 1, col - 1), # up-left
            (row - 1, col + 1), # up-right
            (row + 1, col - 1), # down-left
            (row + 1, col + 1), # down-right
        ]

        for nr, nc in neighbors:
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                nidx = nr + nc * GRID_ROWS
                squares[nidx]["color"] = shade

def random_shade(color):
    r, b, g = color

    mode = random.choice(["dark", "light", "sat+", "sat-", "hue"])

    if mode == "dark":
        factor = random.uniform(0.5, 0.85)
        return (int(r * factor), int(g * factor), int(b * factor))

    if mode == "light":
        factor = random.uniform(1.1, 1.4)
        return (min(int(r * factor), 255),
                min(int(g * factor), 255),
                min(int(b * factor), 255))

    if mode == "sat+":
        boost = random.randint(20, 50)
        return (min(r + boost, 255),
                min(g + boost, 255),
                min(b + boost, 255))

    if mode == "sat-":
        drop = random.randint(20, 50)
        return (max(r - drop, 0),
                max(g - drop, 0),
                max(b - drop, 0))

    if mode == "hue":
        shift = random.randint(-25, 25)
        return (max(min(r + shift, 255), 0),
                max(min(g + shift, 255), 0),
                max(min(b + shift, 255), 0))


def autoC150():
    for col in range(GRID_COLS):
        # Pick row from number_line_list or random
        if number_line_list:
            r = random.choice(number_line_list)
        else:
            r = random.randint(1, GRID_ROWS)

        idx = (r - 1) + col * GRID_ROWS
        squares[idx]["color"] = fg_color

        row = r - 1

        neighbors = [
            (row - 1, col),     # up
            (row + 1, col),     # down
            (row, col - 1),     # left
            (row, col + 1),     # right
            (row - 1, col - 1), # up-left
            (row - 1, col + 1), # up-right
            (row + 1, col - 1), # down-left
            (row + 1, col + 1), # down-right
        ]

        for nr, nc in neighbors:
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                nidx = nr + nc * GRID_ROWS
                squares[nidx]["color"] = random_shade(fg_color)

def generate_same_shade_color(base):
    r, g, b = base
    d = random.randint(-55, 55)
    return (max(0, min(255, r + d)),
            max(0, min(255, g + d)),
            max(0, min(255, b + d)))


def autoColorCycle():
    global fg_color, q_press_count
    q_press_count += 1
    if q_press_count % 2 == 0:
        fg_color = generate_same_shade_color(fg_color)


def erase_all():
    for sq in squares:
        sq["color"] = (255, 255, 255)

def autoBlur1():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            neighbors = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neighbors.append(original[rr + cc * GRID_ROWS])
            avg = tuple(sum(n[i] for n in neighbors) // len(neighbors) for i in range(3))
            squares[r + c * GRID_ROWS]["color"] = avg

def autoBlur2():
    original = [sq["color"] for sq in squares]
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            neighbors = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neighbors.append(original[rr + cc * GRID_ROWS])

            avg = [sum(n[i] for n in neighbors) / len(neighbors) for i in range(3)]
            orig = original[r + c * GRID_ROWS]
            blended = (
                int(orig[0] * 0.5 + avg[0] * 0.5),
                int(orig[1] * 0.5 + avg[1] * 0.5),
                int(orig[2] * 0.5 + avg[2] * 0.5)
            )
            squares[r + c * GRID_ROWS]["color"] = blended
            
def autoGaussianBlur():
    original = [sq["color"] for sq in squares]

    weights = [
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]
    total_weight = 16

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            accum = [0, 0, 0]

            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        w = weights[dr+1][dc+1]
                        col = original[rr + cc * GRID_ROWS]
                        accum[0] += col[0] * w
                        accum[1] += col[1] * w
                        accum[2] += col[2] * w

            squares[r + c * GRID_ROWS]["color"] = (
                accum[0] // total_weight,
                accum[1] // total_weight,
                accum[2] // total_weight
            )
            
def autoSharpen():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            neighbors = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neighbors.append(original[rr + cc * GRID_ROWS])

            avg = [sum(n[i] for n in neighbors) / len(neighbors) for i in range(3)]
            orig = original[r + c * GRID_ROWS]

            # Sharpen = original * 1.5 - blur * 0.5
            sharpened = (
                max(0, min(255, int(orig[0] * 1.5 - avg[0] * 0.5))),
                max(0, min(255, int(orig[1] * 1.5 - avg[1] * 0.5))),
                max(0, min(255, int(orig[2] * 1.5 - avg[2] * 0.5)))
            )

            squares[r + c * GRID_ROWS]["color"] = sharpened

def autoEdgeDetect():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            center = original[r + c * GRID_ROWS]
            edges = 0

            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if dc == 0 and dr == 0:
                        continue
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neigh = original[rr + cc * GRID_ROWS]
                        edges += abs(center[0] - neigh[0])
                        edges += abs(center[1] - neigh[1])
                        edges += abs(center[2] - neigh[2])

            val = min(edges // 8, 255)
            squares[r + c * GRID_ROWS]["color"] = (val, val, val)

def autoPixelate(block=3):
    original = [sq["color"] for sq in squares]

    for c in range(0, GRID_COLS, block):
        for r in range(0, GRID_ROWS, block):

            # sample top-left of block
            sample = original[r + c * GRID_ROWS]

            for cc in range(c, min(c + block, GRID_COLS)):
                for rr in range(r, min(r + block, GRID_ROWS)):
                    squares[rr + cc * GRID_ROWS]["color"] = sample

def autoEmboss():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            rr = min(r+1, GRID_ROWS-1)
            cc = min(c+1, GRID_COLS-1)

            orig = original[r + c * GRID_ROWS]
            neigh = original[rr + cc * GRID_ROWS]

            embossed = (
                max(0, min(255, 128 + orig[0] - neigh[0])),
                max(0, min(255, 128 + orig[1] - neigh[1])),
                max(0, min(255, 128 + orig[2] - neigh[2]))
            )

            squares[r + c * GRID_ROWS]["color"] = embossed
            
def autoBloom():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            orig = original[r + c * GRID_ROWS]
            glow_accum = [0, 0, 0]

            # Bloom strength based on brightness
            brightness = (orig[0] + orig[1] + orig[2]) / 3
            bloom_strength = brightness / 255  # 0.0 to 1.0

            # Spread glow to neighbors
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        neigh = original[rr + cc * GRID_ROWS]
                        glow_accum[0] += neigh[0] * bloom_strength
                        glow_accum[1] += neigh[1] * bloom_strength
                        glow_accum[2] += neigh[2] * bloom_strength

            # Combine original + glow
            bloom = (
                min(int(orig[0] + glow_accum[0] * 0.1), 255),
                min(int(orig[1] + glow_accum[1] * 0.1), 255),
                min(int(orig[2] + glow_accum[2] * 0.1), 255)
            )

            squares[r + c * GRID_ROWS]["color"] = bloom

def autoMedianBlur():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            neighR = []
            neighG = []
            neighB = []

            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        col = original[rr + cc * GRID_ROWS]
                        neighR.append(col[0])
                        neighG.append(col[1])
                        neighB.append(col[2])

            neighR.sort()
            neighG.sort()
            neighB.sort()

            mid = len(neighR) // 2

            median_color = (
                neighR[mid],
                neighG[mid],
                neighB[mid]
            )

            squares[r + c * GRID_ROWS]["color"] = median_color

def autoMedianSharpen():
    original = [sq["color"] for sq in squares]

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):

            neighR = []
            neighG = []
            neighB = []

            # Collect neighbors for median
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        col = original[rr + cc * GRID_ROWS]
                        neighR.append(col[0])
                        neighG.append(col[1])
                        neighB.append(col[2])

            neighR.sort()
            neighG.sort()
            neighB.sort()

            mid = len(neighR) // 2

            median = (
                neighR[mid],
                neighG[mid],
                neighB[mid]
            )

            orig = original[r + c * GRID_ROWS]

            # Sharpen using median instead of blur
            sharpened = (
                max(0, min(255, int(orig[0] * 1.3 - median[0] * 0.3))),
                max(0, min(255, int(orig[1] * 1.3 - median[1] * 0.3))),
                max(0, min(255, int(orig[2] * 1.3 - median[2] * 0.3)))
            )

            squares[r + c * GRID_ROWS]["color"] = sharpened

def copyTopToBottom():
    rows = GRID_ROWS
    cols = GRID_COLS
    half = rows // 2
    original = [sq["color"] for sq in squares]

    for col in range(cols):
        for row in range(half):
            top_index = row + col * rows
            bottom_index = (rows - row - 1) + col * rows
            squares[bottom_index]["color"] = original[top_index]


def copyBottomToTop():
    rows = GRID_ROWS
    cols = GRID_COLS
    half = rows // 2
    original = [sq["color"] for sq in squares]

    for col in range(cols):
        for row in range(half):
            top_index = row + col * rows
            bottom_index = (rows - row - 1) + col * rows
            squares[top_index]["color"] = original[bottom_index]


# ---------------------------------------------------------
# UI Classes (Pygame)
# ---------------------------------------------------------
class Checkbox:
    def __init__(self, x, y, label, checked=False, callback=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = checked
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
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
    def __init__(self, x, y, w, h, value=0, max_value=255, color=(200, 200, 200), callback=None):
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
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x,
                        min(event.pos[0], self.rect.x + self.rect.width - self.knob.width))
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
        self.r = Slider(x, y, 300, 20, 0, color=(205, 50, 50), callback=self.update)
        self.g = Slider(x, y + 40, 300, 20, 0, color=(50, 205, 50), callback=self.update)
        self.b = Slider(x, y + 80, 300, 20, 0, color=(50, 50, 205), callback=self.update)

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


# =========================
# PART 2 OF 2
# =========================

# ---------------------------------------------------------
# Calculator UI (Pygame)
# ---------------------------------------------------------
class CalculatorUI:
    def __init__(self, x, y):
        # Move calculator LEFT and DOWN
        self.x = x - 30
        self.y = y + 180

        self.font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.label_font = pygame.font.SysFont("Courier New", 18, bold=True)

        self.entry_text = ""
        self.display_text = ""

        self.buttons = []
        self.display_rect = pygame.Rect(self.x, self.y, 300, 40)

        self.label_text = "Seven Numbers,seperate with comma"

        self.hover_button = None  # track hover

        self.build_buttons()

    def build_buttons(self):
        w, h = 50, 40
        start_y = self.y + 60

        digits = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("0", 3, 0)
        ]

        for text, row, col in digits:
            bx = self.x + col * (w + 10)
            by = start_y + row * (h + 10)
            rect = pygame.Rect(bx, by, w, h)
            self.buttons.append(("digit", text, rect))

        gen_rect = pygame.Rect(self.x + 3 * (w + 10), start_y, w + 40, h)
        self.buttons.append(("generate", "GEN", gen_rect))

        clr_rect = pygame.Rect(self.x + 3 * (w + 10), start_y + (h + 10), w + 40, h)
        self.buttons.append(("clear", "CLR", clr_rect))
        comma_rect = pygame.Rect(self.x + 3 * (w + 10), start_y + 2 * (h + 10), w + 40, h)
        self.buttons.append(("comma", ",", comma_rect))



    # ---------------------------------------------------------
    # Handle input
    # ---------------------------------------------------------
    def handle_event(self, event):
        global number_line_list

        # Hover detection
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hover_button = None
            for kind, text, rect in self.buttons:
                if rect.collidepoint(mx, my):
                    self.hover_button = rect
                    break

        # Keyboard input
        if event.type == pygame.KEYDOWN:

            if pygame.K_KP0 <= event.key <= pygame.K_KP9:
                digit = event.key - pygame.K_KP0
                self.add_digit(digit)

            elif pygame.K_0 <= event.key <= pygame.K_9:
                digit = event.key - pygame.K_0
                self.add_digit(digit)

            elif event.key == pygame.K_BACKSPACE:
                self.entry_text = self.entry_text[:-1]

            elif event.key == pygame.K_RETURN:
                self.generate_equations()

        # Mouse input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for kind, text, rect in self.buttons:
                if rect.collidepoint(mx, my):

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


    # ---------------------------------------------------------
    # Add digit with comma + space formatting
    # ---------------------------------------------------------
    def add_digit(self, digit):
        # If entry is empty, start a new number
        if self.entry_text == "":
            self.entry_text = str(digit)
            return

        # If last char is a digit, append to form double-digit numbers
        if self.entry_text[-1].isdigit():
            self.entry_text += str(digit)
            return

        # If last char is comma or space, start a new number
        self.entry_text += str(digit)


    # ---------------------------------------------------------
    # Generate equations
    # ---------------------------------------------------------
    def generate_equations(self):
        global number_line_list

        try:
            nums = [int(n.strip()) for n in self.entry_text.split(",")]
        except:
            self.display_text = "ERR"
            return

        if len(nums) < 2:
            self.display_text = "Need >=2 nums"
            return

        new_vals = generate_from_numbers(nums)
        append_number_line(new_vals)

        self.display_text = "Added"
        self.entry_text = ""

    def add_comma(self):
        if self.entry_text == "":
            return
        if self.entry_text[-1].isdigit():
            self.entry_text += ", "

    # ---------------------------------------------------------
    # Draw calculator
    # ---------------------------------------------------------
    def draw(self, surf):
        # Panel + border
        panel_rect = pygame.Rect(self.x - 10, self.y - 40, 380, 300)
        pygame.draw.rect(surf, (20, 20, 20), panel_rect)
        pygame.draw.rect(surf, (255, 255, 0), panel_rect, 4)
        pygame.draw.rect(surf, (120, 120, 0), panel_rect, 2)

        # Label
        label_surf = self.label_font.render(self.label_text, True, (255, 255, 0))
        surf.blit(label_surf, (self.x, self.y - 25))

        # Entry box
        pygame.draw.rect(surf, (40, 40, 40), self.display_rect)
        pygame.draw.rect(surf, (200, 200, 200), self.display_rect, 2)

        entry_surf = self.font.render(self.entry_text, True, (0, 255, 200))
        surf.blit(entry_surf, (self.display_rect.x + 5, self.display_rect.y + 8))

        # Buttons
        for kind, text, rect in self.buttons:

            # Hover highlight
            if rect == self.hover_button:
                pygame.draw.rect(surf, (100, 100, 100), rect)
            else:
                pygame.draw.rect(surf, (60, 60, 60), rect)

            pygame.draw.rect(surf, (200, 200, 200), rect, 2)

            ts = self.font.render(text, True, (0, 255, 200))
            surf.blit(ts, (rect.x + 10, rect.y + 8))

        # Confirmation text
        disp = self.font.render(self.display_text, True, (0, 255, 200))
        surf.blit(disp, (self.x, self.y + 45))


# ---------------------------------------------------------
# UI Instances (Pygame)
# ---------------------------------------------------------
fg_group = SliderGroup(50, 40, lambda c: globals().__setitem__("fg_color", c))
bg_group = SliderGroup(50, 180, lambda c: globals().__setitem__("bg_color", c))
mode_group = CheckboxGroup()

auto_color_checkbox = Checkbox(50, 440, "Auto Color Cycle", False,
                               lambda c: globals().__setitem__("auto_color_enabled", c))
color_paint_checkbox = Checkbox(50, 480, "Color Paint Mode", False,
                                lambda c: globals().__setitem__("color_paint_mode_enabled", c))

calculator = CalculatorUI(50, 540)  # place calculator below controls

def saveCRT(crt_output, filename="crt_output.bmp"):
    surf = pygame.Surface((GRID_COLS, GRID_ROWS))

    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            color = crt_output[r + c * GRID_ROWS]
            surf.set_at((c, r), color)

    pygame.image.save(surf, filename)
    print("Saved CRT image:", filename)


# ---------------------------------------------------------
# Main Loop (Pygame)
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_q:
                autoA150()
                if auto_color_enabled:
                    autoColorCycle()
            if event.key == K_a:
                autoB150()
                if auto_color_enabled:
                    autoColorCycle()
            if event.key == K_d:
                autoC150()
                if auto_color_enabled:
                    autoColorCycle()
            if event.key == K_f:
                autoSharpen()
            if event.key == K_g:
                autoGaussianBlur()
            if event.key == K_h:
                autoEdgeDetect()
            if event.key == K_j:
                autoPixelate()
            if event.key == K_z:
                autoEmboss()
            if event.key == K_x:
                autoBloom()
            if event.key == K_c:
                autoMedianBlur()
            if event.key == K_v:
                autoMedianSharpen()
            if event.key == K_w:
                autoSymmetryPainter()
            if event.key == K_e:
                autoSymmetryPainterReverse()
            if event.key == K_r:
                copyTopToBottom()
            if event.key == K_t:
                copyBottomToTop()
            if event.key == K_s:
                save_picture_only()
            if event.key == K_p:
                erase_all()
            if event.key == K_v:
                autoBlur1()
            if event.key == K_b:
                autoBlur2()
            if event.key == K_l:
                save_animation_gif_south()
            if event.key == K_k:
                save_animation_gif_east()
            if event.key == K_o:
                preview_animation_south()
            if event.key == K_i:
                preview_animation_east()
            elif event.key == pygame.K_COMMA:
                self.add_comma()
    

        fg_group.handle_event(event)
        bg_group.handle_event(event)
        mode_group.handle_event(event)
        auto_color_checkbox.handle_event(event)
        color_paint_checkbox.handle_event(event)
        calculator.handle_event(event)

    screen.fill(bg_color)

    # Draw squares
    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])

    # Draw UI
    fg_group.draw(screen)
    bg_group.draw(screen)
    mode_group.draw(screen)
    auto_color_checkbox.draw(screen)
    color_paint_checkbox.draw(screen)
    calculator.draw(screen)

    # Painting
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:
        for i, sq in enumerate(squares):
            if sq["rect"].collidepoint(mouse_pos):
                rows = GRID_ROWS
                cols = GRID_COLS
                r = i % rows
                c = i // rows

                real_index = r + c * rows

                if mode_group.is_paint_mode():
                    if color_paint_mode_enabled:
                        squares[real_index]["color"] = generate_same_shade_color(fg_color)
                    else:
                        squares[real_index]["color"] = fg_color
                else:
                    squares[real_index]["color"] = (255, 255, 255)
                break


    pygame.display.update()

