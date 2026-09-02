from PIL import Image
import pygame
from pygame.locals import *
import sys
import time
import datetime
import random

pygame.init()
screen = pygame.display.set_mode((1450, 1000), 0, 32)
pygame.display.set_caption("Writers Jumbler 50 Art - Q,W,E,R,T,P=Erase,B=blur,S=save, M,N,L,K")

# ---------------------------------------------------------
# Globals
# ---------------------------------------------------------
fg_color = (0,0,0)
bg_color = (0,0,0)
squares = []
auto_color_enabled = False
color_paint_mode_enabled = False
q_press_count = 0

GRID_ROWS = 50
GRID_COLS = 50
GRID_SPACING = 20
GRID_START_X = 405
GRID_START_Y = 20
GRID_SIZE = 15
SAVE_SIZE = GRID_ROWS * GRID_SPACING  # 1000

# ---------------------------------------------------------
# Filename helper
# ---------------------------------------------------------
def make_timestamp_filename(ext):
    word = "WritersJumbler_50_Art_"
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S-%p")
    return f"{word}{timestamp}.{ext}"

# ---------------------------------------------------------
# Grid builder
# ---------------------------------------------------------
def build_grid(rows=GRID_ROWS, cols=GRID_COLS):
    squares.clear()
    for col in range(cols):
        for row in range(rows):
            x = GRID_START_X + col * GRID_SPACING
            y = GRID_START_Y + row * GRID_SPACING
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
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
# Symmetry + autoA50
# ---------------------------------------------------------
def autoSymmetryPainter():
    cols = GRID_COLS
    rows = GRID_ROWS
    for row in range(rows):
        for col in range(cols//2):
            left = row + col*rows
            right = row + (cols-col-1)*rows
            squares[right]["color"] = squares[left]["color"]

def autoSymmetryPainterReverse():
    cols = GRID_COLS
    rows = GRID_ROWS
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
def autoA50():
    for offset in range(0, GRID_ROWS*GRID_COLS, GRID_ROWS):
        n = random.randint(1, GRID_ROWS)
        idx = n + offset
        if idx < len(squares):
            squares[idx]["color"] = fg_color

# ---------------------------------------------------------
# Auto Color Cycle
# ---------------------------------------------------------
def generate_same_shade_color(base_color):
    r,g,b = base_color
    delta = random.randint(-45,45)
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
    rows = GRID_ROWS
    cols = GRID_COLS
    original = [sq["color"] for sq in squares]

    def get_color(r,c):
        return original[r + c*rows]

    for c in range(cols):
        for r in range(rows):
            neighbors = []
            for dc in (1,0,-1):
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
    surf = pygame.Surface((SAVE_SIZE,SAVE_SIZE))
    for sq in squares:
        shifted = sq["rect"].move(-GRID_START_X,-GRID_START_Y)
        pygame.draw.rect(surf,sq["color"],shifted)
    filename = make_timestamp_filename("png")
    pygame.image.save(surf,filename)
    print("Saved:",filename)

# ---------------------------------------------------------
# Save GIF (picture only)
# ---------------------------------------------------------
def gif_frame():
    surf = pygame.Surface((SAVE_SIZE,SAVE_SIZE))
    for sq in squares:
        shifted = sq["rect"].move(-GRID_START_X,-GRID_START_Y)
        pygame.draw.rect(surf,sq["color"],shifted)
    return surface_to_image(surf)

def save_animation_gif_south():
    frames=[]
    for _ in range(GRID_ROWS):
        marquee_south(GRID_ROWS,GRID_COLS)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_east():
    frames=[]
    for _ in range(GRID_COLS):
        marquee_east(GRID_ROWS,GRID_COLS)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_south_east():
    frames=[]
    for _ in range(GRID_ROWS):
        marquee_east(GRID_ROWS,GRID_COLS)
        marquee_south(GRID_ROWS,GRID_COLS)
        frames.append(gif_frame())
    filename = make_timestamp_filename("gif")
    frames[0].save(filename,save_all=True,append_images=frames[1:],duration=80,loop=0)
    print("Saved:",filename)

def save_animation_gif_north_east():
    frames=[]
    for _ in range(GRID_ROWS):
        marquee_east(GRID_ROWS,GRID_COLS)
        marquee_north(GRID_ROWS,GRID_COLS)
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
# Color Paint Mode Checkbox
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
def on_fg_change(new_color):
    global fg_color
    fg_color=new_color

def on_bg_change(new_color):
    global bg_color
    bg_color=new_color

fg_group = SliderGroup(50,40,"FG",on_fg_change)
bg_group = SliderGroup(50,180,"BG",on_bg_change)
mode_group = CheckboxGroup()

# ---------------------------------------------------------
# Auto Color Cycle Checkbox
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

# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fg_group.handle_event(event)
        bg_group.handle_event(event)
        mode_group.handle_event(event)
        auto_color_checkbox.handle_event(event)
        color_paint_checkbox.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_q:
                autoA50()
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
            handle_square_click(event)

    screen.fill(bg_color)

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:
        handle_hover_paint(mouse_pos)

    for sq in squares:
        pygame.draw.rect(screen,sq["color"],sq["rect"])

    color_paint_checkbox.draw(screen)
    fg_group.draw(screen)
    bg_group.draw(screen)
    mode_group.draw(screen)
    auto_color_checkbox.draw(screen)

    pygame.display.update()
