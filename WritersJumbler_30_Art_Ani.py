from PIL import Image
import pygame
from pygame.locals import *
import sys
import time
import datetime
import random

last_click_time = 0
pygame.init()
screen = pygame.display.set_mode((1024, 768), 0, 32)
pygame.display.set_caption("Writers Jumbler 30 Art - start with keyboard letter q, then either w, e, r, t, y, u, i, o,  p=erase, b=blur, s=saves, animation=l,k,n,m")
def marquee_south(rows, cols):
    # Move each column downward by 1
    for col in range(cols):
        last_color = squares[(rows-1) + col*rows]["color"]
        for row in range(rows-1, 0, -1):
            squares[row + col*rows]["color"] = squares[(row-1) + col*rows]["color"]
        squares[col*rows]["color"] = last_color
def marquee_north(rows, cols):
    # Move each column upward by 1
    for col in range(cols):
        first_color = squares[0 + col*rows]["color"]
        for row in range(0, rows-1):
            squares[row + col*rows]["color"] = squares[(row+1) + col*rows]["color"]
        squares[(rows-1) + col*rows]["color"] = first_color
def marquee_east(rows, cols):
    # Move each row right by 1
    for row in range(rows):
        last_color = squares[row + (cols-1)*rows]["color"]
        for col in range(cols-1, 0, -1):
            squares[row + col*rows]["color"] = squares[row + (col-1)*rows]["color"]
        squares[row] = {"rect": squares[row]["rect"], "color": last_color}
def surface_to_image(surface):
    data = pygame.image.tostring(surface, "RGB")
    img = Image.frombytes("RGB", surface.get_size(), data)
    return img
def save_animation_gif1(filename="WJ_S_Animation.gif", frames=30, rows=30, cols=30):
    gif_frames = []

    for i in range(frames):
        marquee_south(rows, cols)

        # Draw the grid
        screen.fill(bg_color)
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])

        pygame.display.flip()

        # Convert to Pillow image
        img = surface_to_image(screen)
        gif_frames.append(img)

    # Save GIF
    gif_frames[0].save(
        filename,
        save_all=True,
        append_images=gif_frames[1:],
        duration=80,   # ms per frame
        loop=0
    )
def save_animation_gif2(filename="WJ_E_Animation.gif", frames=30, rows=30, cols=30):
    gif_frames = []

    for i in range(frames):
        marquee_east(rows, cols)

        # Draw the grid
        screen.fill(bg_color)
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])

        pygame.display.flip()

        # Convert to Pillow image
        img = surface_to_image(screen)
        gif_frames.append(img)

    # Save GIF
    gif_frames[0].save(
        filename,
        save_all=True,
        append_images=gif_frames[1:],
        duration=80,   # ms per frame
        loop=0
    )
def save_animation_gif3(filename="WJ_SE_Animation.gif", frames=60, rows=30, cols=30):
    gif_frames = []

    for i in range(frames):
        marquee_east(rows, cols)
        marquee_south(rows, cols)
        # Draw the grid
        screen.fill(bg_color)
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])

        pygame.display.flip()

        # Convert to Pillow image
        img = surface_to_image(screen)
        gif_frames.append(img)

    # Save GIF
    gif_frames[0].save(
        filename,
        save_all=True,
        append_images=gif_frames[1:],
        duration=80,   # ms per frame
        loop=0
    )
def save_animation_gif4(filename="WJ_NE_Animation.gif", frames=60, rows=30, cols=30):
    gif_frames = []

    for i in range(frames):
        marquee_east(rows, cols)
        marquee_north(rows, cols)
        # Draw the grid
        screen.fill(bg_color)
        for sq in squares:
            pygame.draw.rect(screen, sq["color"], sq["rect"])

        pygame.display.flip()

        # Convert to Pillow image
        img = surface_to_image(screen)
        gif_frames.append(img)

    # Save GIF
    gif_frames[0].save(
        filename,
        save_all=True,
        append_images=gif_frames[1:],
        duration=80,   # ms per frame
        loop=0
    )
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
def autoRadialSymmetry():
    rows = 30
    cols = 30

    for col in range(cols):
        for row in range(rows):

            idx = row + col * rows

            if squares[idx]["color"] == (255,255,255):
                continue

            # 90° rotation
            r1 = col
            c1 = rows - row - 1
            idx1 = r1 + c1 * rows

            # 180° rotation
            r2 = rows - row - 1
            c2 = cols - col - 1
            idx2 = r2 + c2 * rows

            # 270° rotation
            r3 = cols - col - 1
            c3 = row
            idx3 = r3 + c3 * rows

            squares[idx1]["color"] = fg_color
            squares[idx2]["color"] = fg_color
            squares[idx3]["color"] = fg_color
def autoFractalPainter():
    rows = 30
    cols = 30

    for col in range(cols // 2):
        for row in range(rows // 2):

            idx = row + col * rows

            if squares[idx]["color"] == (255,255,255):
                continue

            # Quadrant 1 → Quadrant 2
            q2 = row + (col + cols//2) * rows

            # Quadrant 1 → Quadrant 3
            q3 = (row + rows//2) + col * rows

            # Quadrant 1 → Quadrant 4
            q4 = (row + rows//2) + (col + cols//2) * rows

            squares[q2]["color"] = fg_color
            squares[q3]["color"] = fg_color
            squares[q4]["color"] = fg_color
def autoPatternFill():
    rows = 30
    cols = 30

    for col in range(cols):
        for row in range(rows):

            src_row = row % 10
            src_col = col % 10

            src_idx = src_row + src_col * rows
            dst_idx = row + col * rows

            if squares[src_idx]["color"] != (255,255,255):
                squares[dst_idx]["color"] = fg_color
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

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    pos = event.pos
    clicked = None

    for sq in squares:
        if sq["rect"].collidepoint(pos):
            clicked = sq
            break

    if clicked is None:
        return

    # RIGHT CLICK = erase (optional)
    if event.button == 3:
        clicked["color"] = (255,255,255)
        return

    # LEFT CLICK = paint OR erase depending on mode
    if event.button == 1:
        if mode_group.is_paint_mode():
            clicked["color"] = fg_color
        elif mode_group.is_erase_mode():
            clicked["color"] = (255,255,255)


def handle_hover_paint(pos):
    for sq in squares:
        if sq["rect"].collidepoint(pos):
            sq["color"] = fg_color
            break

class Checkbox:
    def __init__(self, x, y, label, checked=False, callback=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = checked
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)

    def draw(self, surf):
        pygame.draw.rect(surf, (230,230,230), self.rect, 2)
        if self.checked:
            pygame.draw.line(surf, (230,230,230), (self.rect.x+4, self.rect.y+10), (self.rect.x+10, self.rect.y+16), 3)
            pygame.draw.line(surf, (230,230,230), (self.rect.x+10, self.rect.y+16), (self.rect.x+16, self.rect.y+4), 3)

        font = pygame.font.SysFont(None, 24)
        txt = font.render(self.label, True, (230,230,230))
        surf.blit(txt, (self.rect.x + 50, self.rect.y - 2))




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
mode_group = CheckboxGroup()
squares = []
def handle_hover_paint(pos):
    for sq in squares:
        if sq["rect"].collidepoint(pos):
            sq["color"] = fg_color
            break
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
def autoBlur():
    rows = 30
    cols = 30

    # Copy current colors so blur uses original values
    original = [sq["color"] for sq in squares]

    def get_color(r, c):
        idx = r + c * rows
        return original[idx]

    for c in range(cols):
        for r in range(rows):

            neighbors = []
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < rows and 0 <= cc < cols:
                        neighbors.append(get_color(rr, cc))

            # Average RGB
            if neighbors:
                avg_r = sum(n[0] for n in neighbors) // len(neighbors)
                avg_g = sum(n[1] for n in neighbors) // len(neighbors)
                avg_b = sum(n[2] for n in neighbors) // len(neighbors)

                idx = r + c * rows
                squares[idx]["color"] = (avg_r, avg_g, avg_b)

while True:
    word = "WritersJumbler_"
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
    zS = word + d
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYDOWN:
            if event.key == K_q: autoA30()
            if event.key == K_w: autoSymmetryPainter()
            if event.key == K_e: autoSymmetryPainterVertical()
            if event.key == K_r: autoSymmetryPainterQuad()
            if event.key == K_t: autoDiagonalMirror()
            if event.key == K_y: autoCrossMirror()
            if event.key == K_u: autoRadialSymmetry()
            if event.key == K_i: autoFractalPainter()
            if event.key == K_o: autoPatternFill()
            if event.key == K_s: saveAsBMP()
            if event.key == K_p: erase_all()
            if event.key == K_b: autoBlur()
            if event.key == K_n: save_animation_gif1(zS+"_marquee_s.gif")
            if event.key == K_m: save_animation_gif2(zS+"_marquee_e.gif")
            if event.key == K_l: save_animation_gif3(zS+"_marquee_se.gif")
            if event.key == K_k: save_animation_gif4(zS+"_marquee_ne.gif")

        # FIX: sliders must receive every event
        fg_group.handle_event(event)
        bg_group.handle_event(event)
        mode_group.handle_event(event)

    screen.fill(bg_color)

    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])
    
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mode_group.is_paint_mode():
        if mouse_buttons[0]:  # left button held
            handle_hover_paint(mouse_pos)

    if mouse_buttons[0]:  # left button held
        for sq in squares:
            if sq["rect"].collidepoint(mouse_pos):
                if mode_group.is_paint_mode():
                    sq["color"] = fg_color
                elif mode_group.is_erase_mode():
                    sq["color"] = (255,255,255)
                break

    fg_group.draw(screen)
    bg_group.draw(screen)
    mode_group.draw(screen)

    pygame.display.update()
