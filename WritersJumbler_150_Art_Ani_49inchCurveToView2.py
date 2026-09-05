from PIL import Image
import pygame
from pygame.locals import *
import sys
import datetime
import random

pygame.init()
screen = pygame.display.set_mode((3500, 1000), 0, 32)
pygame.display.set_caption("Writers Jumbler 150 Art - Q = First,W,E=Symmetry,P=Erase,B=Blur,S=Save,L,K=Save,O,I=Preview")

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
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

# Page system (internal only)
current_page_offset = 0
page_mode_direction = "east"
preview_mode_enabled = False   # internal only, no checkbox

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
# Virtual Page System (internal only)
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
# Marquee Functions (for GIF / preview)
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
    filename = datetime.datetime.now().strftime("WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.png")
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

    filename = datetime.datetime.now().strftime("WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.gif")
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

    filename = datetime.datetime.now().strftime("WritersJumbler_150_Art_%m-%d-%Y-%I-%M-%S-%p.gif")
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

def autoA30():
    for col in range(GRID_COLS):
        r = random.randint(0, GRID_ROWS - 1)
        idx = r + col * GRID_ROWS
        squares[idx]["color"] = fg_color

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

def autoBlur():
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
    def __init__(self, x, y, w, h, value=0, max_value=255, color=(200,200,200), callback=None):
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
        pygame.draw.rect(surf, (255,255,255), self.knob, border_radius=4)

class SliderGroup:
    def __init__(self, x, y, callback):
        self.callback = callback
        self.r = Slider(x, y, 300, 20, 0, color=(205,50,50), callback=self.update)
        self.g = Slider(x, y+40, 300, 20, 0, color=(50,205,50), callback=self.update)
        self.b = Slider(x, y+80, 300, 20, 0, color=(50,50,205), callback=self.update)

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
# UI Instances
# ---------------------------------------------------------
fg_group = SliderGroup(50, 40, lambda c: globals().__setitem__("fg_color", c))
bg_group = SliderGroup(50, 180, lambda c: globals().__setitem__("bg_color", c))
mode_group = CheckboxGroup()

auto_color_checkbox = Checkbox(50, 440, "Auto Color Cycle", False,
                               lambda c: globals().__setitem__("auto_color_enabled", c))
color_paint_checkbox = Checkbox(50, 480, "Color Paint Mode", False,
                                lambda c: globals().__setitem__("color_paint_mode_enabled", c))

# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_q:
                autoA30()
                if auto_color_enabled:
                    autoColorCycle()
            if event.key == K_w:
                autoSymmetryPainter()
            if event.key == K_e:
                autoSymmetryPainterReverse()
            if event.key == K_s:
                save_picture_only()
            if event.key == K_p:
                erase_all()
            if event.key == K_b:
                autoBlur()
            if event.key == K_l:
                save_animation_gif_south()
            if event.key == K_k:
                save_animation_gif_east()
            if event.key == K_o:
                preview_animation_south()
            if event.key == K_i:
                preview_animation_east()

        fg_group.handle_event(event)
        bg_group.handle_event(event)
        mode_group.handle_event(event)
        auto_color_checkbox.handle_event(event)
        color_paint_checkbox.handle_event(event)

    screen.fill(bg_color)

    # Draw squares (normal mode only)
    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])

    # Draw UI
    fg_group.draw(screen)
    bg_group.draw(screen)
    mode_group.draw(screen)
    auto_color_checkbox.draw(screen)
    color_paint_checkbox.draw(screen)

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
                    squares[real_index]["color"] = (255,255,255)
                break

    pygame.display.update()
