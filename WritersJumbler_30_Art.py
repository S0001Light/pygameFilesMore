import pygame
from pygame.locals import *
from sys import exit
import time
import datetime
import random
last_click_time = 0
pygame.init()
screen = pygame.display.set_mode((1024, 768), 0, 32)
pygame.display.set_caption("Writers Jumbler 30 Art - start with keyboard letter q, then either w, e, r, t, y, u=erase, also, press S on the keyboard to Save")
def autoSymmetryPainter():
    cols = 30
    rows = 30

    for row in range(rows):
        for col in range(cols // 2):
            left_index = row + col * rows
            right_index = row + (cols - col - 1) * rows

            squares[right_index]["color"] = squares[left_index]["color"]

def autoSymmetryPainterVertical():
    cols = 30
    rows = 30

    for col in range(cols):
        for row in range(rows // 2):
            top_index = row + col * rows
            bottom_index = (rows - row - 1) + col * rows

            squares[bottom_index]["color"] = squares[top_index]["color"]

def autoSymmetryPainterQuad():
    cols = 30
    rows = 30

    for col in range(cols // 2):
        for row in range(rows // 2):

            tl = row + col * rows
            tr = row + (cols - col - 1) * rows
            bl = (rows - row - 1) + col * rows
            br = (rows - row - 1) + (cols - col - 1) * rows

            color = squares[tl]["color"]

            squares[tr]["color"] = color
            squares[bl]["color"] = color
            squares[br]["color"] = color
def autoDiagonalMirror():
    rows = 30
    cols = 30

    for row in range(rows):
        for col in range(cols):
            src_index = row + col * rows
            dst_index = col + row * rows

            # Only mirror painted squares
            if squares[src_index]["color"] != (255,255,255):
                squares[dst_index]["color"] = fg_color

def autoCrossMirror():
    rows = 30
    cols = 30

    for col in range(cols):
        for row in range(rows):

            idx = row + col * rows

            # Horizontal mirror target
            h_idx = row + (cols - col - 1) * rows

            # Vertical mirror target
            v_idx = (rows - row - 1) + col * rows

            # Both mirror target (quad)
            hv_idx = (rows - row - 1) + (cols - col - 1) * rows

            if squares[idx]["color"] != (255,255,255):
                squares[h_idx]["color"] = fg_color
                squares[v_idx]["color"] = fg_color
                squares[hv_idx]["color"] = fg_color

def autoA30():
    # Your JS code generates 30 random numbers in blocks of 30
    chosen_indices = []

    # 0, 30, 60, ..., 870  (30 blocks)
    for offset in range(0, 900, 30):
        n = random.randint(1, 30)
        chosen_indices.append(n + offset)

    # Now paint those squares black
    for idx in chosen_indices:
        if idx < len(squares):
            squares[idx]["color"] = fg_color

def handle_square_click(event):
    global last_click_time

    pos = event.pos
    clicked = None

    for sq in squares:
        if sq["rect"].collidepoint(pos):
            clicked = sq
            break

    if clicked is None:
        return

    now = time.time()

    # RIGHT CLICK = reset
    if event.button == 3:
        clicked["color"] = (255,255,255)
        return

    # LEFT CLICK
    if event.button == 1:
        # double-click = reset
        if now:
            clicked["color"] = fg_color

        last_click_time = now

# ---------------------------------------------------------
# Slider with callback
# ---------------------------------------------------------
class Slider:
    def __init__(self, x, y, w, h, value=0, max_value=255, color=(200,200,200), callback=None):
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
        self.knob_rect.x = self.rect.x + int(ratio * (self.rect.width - self.knob_rect.width))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width - self.knob_rect.width))
            self.knob_rect.x = new_x

            ratio = (self.knob_rect.x - self.rect.x) / (self.rect.width - self.knob_rect.width)
            self.value = int(ratio * self.max_value)

            if self.callback:
                self.callback(self.value)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surf, (255,255,255), self.knob_rect, border_radius=4)


# ---------------------------------------------------------
# SliderGroup (R, G, B)
# ---------------------------------------------------------
class SliderGroup:
    def __init__(self, x, y, label, callback):
        self.label = label
        self.callback = callback
        red= (255, 50, 50)
        green = (50, 255, 50)
        blue = (50, 50, 255)
        self.r = Slider(x, y,     300, 20, 128, color=red, callback=self.update)
        self.g = Slider(x, y+40,  300, 20, 128, color=green, callback=self.update)
        self.b = Slider(x, y+80,  300, 20, 128, color=blue, callback=self.update)

        self.color = (128,128,128)

    def update(self, _):
        self.color = (self.r.value, self.g.value, self.b.value)
        self.callback(self.color)

    def handle_event(self, event):
        self.r.handle_event(event)
        self.g.handle_event(event)
        self.b.handle_event(event)

    def draw(self, surf):
        self.r.draw(surf)
        self.g.draw(surf)
        self.b.draw(surf)


# ---------------------------------------------------------
# Callback functions
# ---------------------------------------------------------
fg_color = (128,128,128)
bg_color = (50,50,50)

def on_fg_change(new_color):
    global fg_color
    fg_color = new_color

def on_bg_change(new_color):
    global bg_color
    bg_color = new_color


# ---------------------------------------------------------
# Create slider groups
# ---------------------------------------------------------
fg_group = SliderGroup(50, 40, "FG", on_fg_change)
bg_group = SliderGroup(50, 180, "BG", on_bg_change)
squares = []
def function00():
    y = 20 + 0
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (405, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (425, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (445, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (465, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (485, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (505, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (525, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (545, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (565, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (585, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (605, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (625, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (645, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (665, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (685, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (705, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (725, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (745, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (765, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (785, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (805, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (825, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (845, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (865, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (885, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (905, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (925, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (945, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (965, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 0
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 20
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 40
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 60
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 80
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 100
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 120
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 140
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 160
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 180
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 200
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 220
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 240
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 260
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 280
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 300
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 320
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 340
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 360
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 380
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 400
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 420
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 440
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 460
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 480
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 500
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 520
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 540
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 560
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    y = 20 + 580
    one_rct_size = (985, y)
    two_rct_size = (15, 15)
    rect = Rect((one_rct_size), (two_rct_size))
    squares.append({"rect": rect, "color": (255,255,255)})

    return

function00()

def saveAsBMP():
    word = "WritersJumbler_30_Art_"
    dthm = datetime.datetime.now()
    m = str(dthm.strftime("%m"))
    dy = str(dthm.strftime("%d"))
    y = str(dthm.strftime("%Y"))
    h = str(dthm.strftime("%I"))
    mins = str(dthm.strftime("%M"))
    amPm = str(dthm.strftime("%p"))
    sec = str(dthm.strftime("%S"))
    dash = "-"
    d = str(m + dash + dy + dash + y + dash + h + dash + mins + dash + sec + dash + amPm)
    zS = word + d + ".bmp"
    getImage = screen
    pygame.image.save(getImage, zS)
    return
def erase_all():
    for sq in squares:
        sq["color"] = (255, 255, 255)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_q:
                autoA30()
            if event.key == pygame.K_w:
                autoSymmetryPainter()
            if event.key == pygame.K_e:
                autoSymmetryPainterVertical()
            if event.key == pygame.K_r:
                autoSymmetryPainterQuad()
            if event.key == pygame.K_t:
                autoDiagonalMirror()
            if event.key == pygame.K_y:
                autoCrossMirror()
            if event.key == K_s:
                saveAsBMP()
            if event.key == pygame.K_u:
                erase_all()
       
    screen.fill(bg_color)
    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])
    
    fg_group.draw(screen)
    bg_group.draw(screen)
    fg_group.handle_event(event)
    bg_group.handle_event(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        handle_square_click(event)

    pygame.display.update()

