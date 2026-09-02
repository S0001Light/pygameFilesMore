from PIL import Image
import pygame
from pygame.locals import *
import sys
import time
import datetime
import random
import math

pygame.init()
screen = pygame.display.set_mode((1024, 768), 0, 32)
pygame.display.set_caption("Writers Jumbler 30 Art - Q,W,E,R,T,P=Erase,B=blur,S=save, M,N,L,K")

def hsv_to_rgb(h, s, v):
    i = int(h * 6)
    f = h * 6 - i
    p = int(255 * v * (1 - s))
    q = int(255 * v * (1 - f * s))
    t = int(255 * v * (1 - (1 - f) * s))
    v = int(255 * v)

    i = i % 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)
def draw_hue_wheel(surface, x, y, w, h):
    for i in range(w):
        hue = i / w
        for j in range(h):
            v = 1 - (j / h)
            color = hsv_to_rgb(hue, 1, v)
            surface.set_at((x + i, y + j), color)
def spectrum_square_click(mx, my, x, y, w, h):
    if x <= mx < x + w and y <= my < y + h:
        hue = (mx - x) / w
        v = 1 - ((my - y) / h)
        return hsv_to_rgb(hue, 1, v)
    return None


# FG Spectrum
FG_SPEC_X, FG_SPEC_Y = 50, 50
FG_SPEC_W, FG_SPEC_H = 260, 130

# BG Spectrum
BG_SPEC_X, BG_SPEC_Y = 50, 170
BG_SPEC_W, BG_SPEC_H = 260, 130

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
fg_color = (0,0,0)
bg_color = (0,0,0)
squares = []
auto_color_enabled = False   # NEW BUTTON TOGGLE
color_paint_mode_enabled = False

q_press_count = 0

# ---------------------------------------------------------
# Filename helper
# ---------------------------------------------------------
def make_timestamp_filename(ext):
    word = "WritersJumbler_30_Art_"
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S-%p")
    return f"{word}{timestamp}.{ext}"

def drawButton(label, x, y, callback):
    # button size
    w, h = 80, 30

    # draw rectangle
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (180, 180, 180), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    # draw text
    font = pygame.font.SysFont(None, 24)
    text = font.render(label, True, (0, 0, 0))
    screen.blit(text, (x + 10, y + 5))

    # return rect so main loop can detect clicks
    return rect

# ---------------------------------------------------------
# Grid builder
# ---------------------------------------------------------
def build_grid(rows=30, cols=30):
    squares.clear()
    start_x = 405
    start_y = 20
    size = 15
    spacing = 20

    for col in range(cols):
        for row in range(rows):
            x = start_x + col * spacing
            y = start_y + row * spacing
            rect = pygame.Rect(x, y, size, size)
            squares.append({"rect": rect, "color": (255,255,255)})
        
build_grid()

# ---------------------------------------------------------
# Marquee functions
# ---------------------------------------------------------
def marquee_south(rows, cols):
    for col in range(cols):
        last_color = squares[(rows-1) + col*rows]["color"]
        for row in range(rows-1, 0, -1):
            squares[row + col*rows]["color"] = squares[(row-1) + col*rows]["color"]
        squares[col*rows]["color"] = last_color

def marquee_north(rows, cols):
    for col in range(cols):
        first_color = squares[0 + col*rows]["color"]
        for row in range(0, rows-1):
            squares[row + col*rows]["color"] = squares[(row+1) + col*rows]["color"]
        squares[(rows-1) + col*rows]["color"] = first_color

def marquee_east(rows, cols):
    for row in range(rows):
        last_color = squares[row + (cols-1)*rows]["color"]
        for col in range(cols-1, 0, -1):
            squares[row + col*rows]["color"] = squares[row + (col-1)*rows]["color"]
        squares[row]["color"] = last_color

# ---------------------------------------------------------
# Symmetry + autoA30
# ---------------------------------------------------------
def autoSymmetryPainter():
    cols = 30
    rows = 30
    for row in range(rows):
        for col in range(cols//2):
            left = row + col*rows
            right = row + (cols-col-1)*rows
            squares[right]["color"] = squares[left]["color"]

def autoSymmetryPainterReverse():
    cols = 30
    rows = 30
    for row in range(rows):
        for col in range(cols//2):
            left = row + col*rows
            right = row + (cols-col-1)*rows
            squares[left]["color"] = squares[right]["color"]

def symmetryBottomToTop():
    total = len(squares)
    rows = int(total ** 0.5)
    cols = rows

    for col in range(cols):
        for row in range(rows // 2):
            top_index = row + col * rows
            bottom_index = (rows - row - 1) + col * rows

            squares[top_index]["color"] = squares[bottom_index]["color"]

def symmetryTopToBottom():
    total = len(squares)
    rows = int(total ** 0.5)
    cols = rows

    for col in range(cols):
        for row in range(rows // 2):
            top_index = row + col * rows
            bottom_index = (rows - row - 1) + col * rows

            squares[bottom_index]["color"] = squares[top_index]["color"]

def autoA30():
    for offset in range(0,900,30):
        n = random.randint(1,30)
        idx = n + offset
        if idx < len(squares):
            squares[idx]["color"] = fg_color

# ---------------------------------------------------------
# Auto Color Cycle (NEW BUTTON CONTROL)
# ---------------------------------------------------------
def generate_same_shade_color(base_color):
    r,g,b = base_color
    delta = random.randint(-55,55)
    nr = max(0,min(255,r+delta))
    ng = max(0,min(255,g+delta))
    nb = max(0,min(255,b+delta))
    return (nr,ng,nb)

def autoColorCycle():
    global fg_color, q_press_count
    q_press_count += 1
    if q_press_count % 2 == 0:
        fg_color = generate_same_shade_color(fg_color)
        print("Auto‑color changed:", fg_color)

# ---------------------------------------------------------
# Blur
# ---------------------------------------------------------
def autoBlur():
    rows = 30
    cols = 30
    original = [sq["color"] for sq in squares]

    def get_color(r,c):
        return original[r + c*rows]

    for c in range(cols):
        for r in range(rows):
            neighbors = []
            for dc in (-1,0,1):
                for dr in (-1,0,1):
                    rr = r+dr
                    cc = c+dc
                    if 0 <= rr < rows and 0 <= cc < cols:
                        neighbors.append(get_color(rr,cc))
            avg_r = sum(n[0] for n in neighbors)//len(neighbors)
            avg_g = sum(n[1] for n in neighbors)//len(neighbors)
            avg_b = sum(n[2] for n in neighbors)//len(neighbors)
            squares[r + c*rows]["color"] = (avg_r,avg_g,avg_b)

# ---------------------------------------------------------
# Save PNG (picture only)
# ---------------------------------------------------------
def surface_to_image(surface):
    data = pygame.image.tostring(surface,"RGB")
    return Image.frombytes("RGB",surface.get_size(),data)

def save_picture_only():
    surf = pygame.Surface((600,600))
    for sq in squares:
        shifted = sq["rect"].move(-405,-20)
        pygame.draw.rect(surf,sq["color"],shifted)
    filename = make_timestamp_filename("png")
    pygame.image.save(surf,filename)
    print("Saved:",filename)

# ---------------------------------------------------------
# Save GIF (picture only)
# ---------------------------------------------------------
def gif_frame():
    surf = pygame.Surface((600,600))
    for sq in squares:
        shifted = sq["rect"].move(-405,-20)
        pygame.draw.rect(surf,sq["color"],shifted)
    return surface_to_image(surf)

def save_animation_gif_south():
    frames=[]
    for _ in range(30):
        marquee_south(30,30)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_east():
    frames=[]
    for _ in range(30):
        marquee_east(30,30)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_south_east():
    frames=[]
    for _ in range(60):
        marquee_east(30,30)
        marquee_south(30,30)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_north_east():
    frames=[]
    for _ in range(60):
        marquee_east(30,30)
        marquee_north(30,30)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

# ---------------------------------------------------------
# UI Classes
# ---------------------------------------------------------
class Checkbox:
    def __init__(self,x,y,label,checked=False,callback=None):
        self.rect = pygame.Rect(x,y,20,20)
        self.label = label
        self.checked = checked
        self.callback = callback

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)

    def draw(self,surf):
        pygame.draw.rect(surf,(230,230,230),self.rect,2)
        if self.checked:
            pygame.draw.line(surf,(230,230,230),(self.rect.x+4,self.rect.y+10),(self.rect.x+10,self.rect.y+16),3)
            pygame.draw.line(surf,(230,230,230),(self.rect.x+10,self.rect.y+16),(self.rect.x+16,self.rect.y+4),3)
        font = pygame.font.SysFont(None,24)
        txt = font.render(self.label,True,(230,230,230))
        surf.blit(txt,(self.rect.x+50,self.rect.y-2))
    

class Slider:
    def __init__(self,x,y,w,h,value=0,max_value=255,color=(200,200,200),callback=None):
        self.rect = pygame.Rect(x,y,w,h)
        self.knob_rect = pygame.Rect(x,y,10,h)
        self.max_value=max_value
        self.value=value
        self.color=color
        self.dragging=False
        self.callback=callback
        self.update_knob()

    def update_knob(self):
        ratio=self.value/self.max_value
        self.knob_rect.x=self.rect.x+int(ratio*(self.rect.width-self.knob_rect.width))

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging=True
        elif event.type==pygame.MOUSEBUTTONUP:
            self.dragging=False
        elif event.type==pygame.MOUSEMOTION and self.dragging:
            new_x=max(self.rect.x,min(event.pos[0],self.rect.x+self.rect.width-self.knob_rect.width))
            self.knob_rect.x=new_x
            ratio=(self.knob_rect.x-self.rect.x)/(self.rect.width-self.knob_rect.width)
            self.value=int(ratio*self.max_value)
            if self.callback:
                self.callback(self.value)

    def draw(self,surf):
        pygame.draw.rect(surf,self.color,self.rect,border_radius=4)
        pygame.draw.rect(surf,(255,255,255),self.knob_rect,border_radius=4)

class SliderGroup:
    def __init__(self,x,y,label,callback):
        self.label=label
        self.callback=callback
        self.r=Slider(x,y,300,20,0,color=(255,50,50),callback=self.update)
        self.g=Slider(x,y+40,300,20,0,color=(50,255,50),callback=self.update)
        self.b=Slider(x,y+80,300,20,0,color=(50,50,255),callback=self.update)
        self.color=(128,128,128)

    def update(self,_):
        self.color=(self.r.value,self.g.value,self.b.value)
        self.callback(self.color)

    def handle_event(self,event):
        self.r.handle_event(event)
        self.g.handle_event(event)
        self.b.handle_event(event)

    def draw(self,surf):
        self.r.draw(surf)
        self.g.draw(surf)
        self.b.draw(surf)

class CheckboxGroup:
    def __init__(self):
        self.paint=Checkbox(50,320,"Paint Mode",True,self.on_paint)
        self.erase=Checkbox(50,360,"Erase Mode",False,self.on_erase)

    def on_paint(self,checked):
        if checked:
            self.erase.checked=False

    def on_erase(self,checked):
        if checked:
            self.paint.checked=False

    def handle_event(self,event):
        self.paint.handle_event(event)
        self.erase.handle_event(event)

    def draw(self,surf):
        self.paint.draw(surf)
        self.erase.draw(surf)

    def is_paint_mode(self):
        return self.paint.checked

    def is_erase_mode(self):
        return self.erase.checked

# ---------------------------------------------------------
# Color Paint Mode Checkbox (FIXED)
# ---------------------------------------------------------
def toggle_color_paint_mode(checked):
    global color_paint_mode_enabled
    color_paint_mode_enabled = checked

color_paint_checkbox = Checkbox(
    50, 480,
    "Color Paint Mode",
    False,
    toggle_color_paint_mode
)

# ---------------------------------------------------------
# Slider callbacks
# ---------------------------------------------------------
mode_group = CheckboxGroup()

# ---------------------------------------------------------
# Auto Color Cycle Checkbox (NEW)
# ---------------------------------------------------------
def toggle_auto_color(checked):
    global auto_color_enabled
    auto_color_enabled = checked

auto_color_checkbox = Checkbox(50, 440, "Auto Color Cycle", False, toggle_auto_color)

# ---------------------------------------------------------
# Painting
# ---------------------------------------------------------
def handle_square_click(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    pos = event.pos
    for sq in squares:
        if sq["rect"].collidepoint(pos):

            if event.button == 3:
                sq["color"] = (255,255,255)
                return

            if event.button == 1:
                if mode_group.is_paint_mode():
                    if color_paint_mode_enabled:
                        sq["color"] = generate_same_shade_color(fg_color)
                    else:
                        sq["color"] = fg_color
                else:
                    sq["color"] = (255,255,255)
            return


def handle_hover_paint(pos):
    for sq in squares:
        if sq["rect"].collidepoint(pos):
            if mode_group.is_paint_mode():
                if color_paint_mode_enabled:
                    sq["color"] = generate_same_shade_color(fg_color)
                else:
                    sq["color"] = fg_color
            break

def hue_wheel_click(mx, my, cx, cy, radius):
    dx = mx - cx
    dy = my - cy
    dist = math.sqrt(dx*dx + dy*dy)
    if dist <= radius:
        angle = math.atan2(dy, dx)
        hue = (angle + math.pi) / (2 * math.pi)
        return hsv_to_rgb(hue, 1, 1)
    return None

# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        mode_group.handle_event(event)
        auto_color_checkbox.handle_event(event)
        color_paint_checkbox.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_q:
                autoA30()
                if auto_color_enabled:
                    autoColorCycle()

            if event.key == K_w: autoSymmetryPainter()
            if event.key == K_e: autoSymmetryPainterReverse()
            if event.key == K_r: symmetryTopToBottom()
            if event.key == K_t: symmetryBottomToTop()
            if event.key == K_p:
                for sq in squares:
                    sq["color"] = (255,255,255)

            if event.key == K_b:
                autoBlur()

            if event.key == pygame.K_s:
                save_picture_only()
            if event.key == pygame.K_l:
                save_animation_gif_south()
            if event.key == pygame.K_k:
                save_animation_gif_east()
            if event.key == pygame.K_n:
                save_animation_gif_south_east()
            if event.key == pygame.K_m:
                save_animation_gif_north_east()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # FG spectrum click
            fg_spec = spectrum_square_click(mx, my, FG_SPEC_X, FG_SPEC_Y, FG_SPEC_W, FG_SPEC_H)
            if fg_spec:
                fg_color = fg_spec

            # BG spectrum click
            bg_spec = spectrum_square_click(mx, my, BG_SPEC_X, BG_SPEC_Y, BG_SPEC_W, BG_SPEC_H)
            if bg_spec:
                bg_color = bg_spec
            
            handle_square_click(event)


    screen.fill(bg_color)

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:
        handle_hover_paint(mouse_pos)

    # --- DRAW GRID ---
    for sq in squares:
        pygame.draw.rect(screen, sq["color"], sq["rect"])

    # --- DRAW UI ---
    draw_hue_wheel(screen, FG_SPEC_X, FG_SPEC_Y, FG_SPEC_W, FG_SPEC_H)
    draw_hue_wheel(screen, BG_SPEC_X, BG_SPEC_Y, BG_SPEC_W, BG_SPEC_H)

    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render("FG Spectrum", True, (230,230,230)), (FG_SPEC_X, FG_SPEC_Y - 30))
    screen.blit(font.render("BG Spectrum", True, (230,230,230)), (BG_SPEC_X, BG_SPEC_Y - 30))

    color_paint_checkbox.draw(screen)
    mode_group.draw(screen)
    auto_color_checkbox.draw(screen)

    pygame.display.flip()



