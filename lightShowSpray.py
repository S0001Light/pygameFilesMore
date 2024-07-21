import pygame
from pygame.locals import *
from random import *
from sys import exit
import sys
import math

pygame.init()
screen = pygame.display.set_mode((640, 640), RESIZABLE, 32)

def lineLightShow():
    
    x = int(randint(0, 32) * 10.)
    y = int(randint(0, 32) * 10.)
    x1 = int(randint(0, 32) * 10.)
    y1 = int(randint(0, 32) * 10.)
    x2 = int(randint(0, 32) * 10.)
    y2 = int(randint(0, 32) * 10.)
    x3 = int(randint(0, 32) * 10.)
    y3 = int(randint(0, 32) * 10.)
    x4 = int(randint(0, 32) * 10.)
    y4 = int(randint(0, 32) * 10.)
    
    rct_color = (int(255),int(255),int(255))
    pointSet3 = (640, x)
    pointSet4 = (0, x)
    pointSet5 = x * 640
    pointSet6 = y * 640
    pointSet7 = pointSet5 / 500
    pointSet8 = pointSet6 / 500
    pointSet51 = x1 * 640
    pointSet61 = y1 * 640
    pointSet72 = pointSet51 / 500
    pointSet82 = pointSet61 / 500
    pointSet53 = x2 * 640
    pointSet63 = y2 * 640
    pointSet74 = pointSet53 / 500
    pointSet84 = pointSet63 / 500
    pointSet55 = x3 * 640
    pointSet65 = y3 * 640
    pointSet76 = pointSet55 / 500
    pointSet86 = pointSet65 / 500
    pointSet57 = x4 * 640
    pointSet67 = y4 * 640
    pointSet78 = pointSet57 / 500
    pointSet88 = pointSet67 / 500
    print(pointSet5)
    print(pointSet6)
    print(pointSet7)
    print(pointSet8)
    print(pointSet51)
    print(pointSet61)
    print(pointSet72)
    print(pointSet82)
    print(pointSet53)
    print(pointSet63)
    print(pointSet74)
    print(pointSet84)
    print(pointSet55)
    print(pointSet65)
    print(pointSet76)
    print(pointSet86)
    print(pointSet57)
    print(pointSet67)
    print(pointSet78)
    print(pointSet88)
    pointSet9 = (0, pointSet7)
    pointSet10= (0, pointSet8)
    pointSet11 = (pointSet7, 640)
    pointSet12 = (pointSet8, 640)
    pointSet9a = (0, pointSet72)
    pointSet10a= (0, pointSet82)
    pointSet11a = (pointSet72, 0)
    pointSet12a = (pointSet82, 0)
    pointSet9b = (640, pointSet74)
    pointSet10b = (640, pointSet84)
    pointSet11b = (pointSet74, 640)
    pointSet12b = (pointSet84, 640)
    pointSet9c = (0, pointSet76)
    pointSet10c= (0, pointSet86)
    pointSet11c = (pointSet76, 0)
    pointSet12c = (pointSet86, 0)
    pointSet9d = (640, pointSet78)
    pointSet10d = (640, pointSet88)
    pointSet11d = (pointSet78, 640)
    pointSet12d = (pointSet88, 640)
    
    pygame.draw.line(screen, rct_color, (pointSet9), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10),1)
    pygame.draw.line(screen, rct_color, (pointSet11), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9a), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10a),1)
    pygame.draw.line(screen, rct_color, (pointSet11a), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12a),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9b), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10b),1)
    pygame.draw.line(screen, rct_color, (pointSet11b), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12b),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9c), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10c),1)
    pygame.draw.line(screen, rct_color, (pointSet11c), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12c),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9d), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10d),1)
    pygame.draw.line(screen, rct_color, (pointSet11d), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12d),1)
def lineLightShow2():
    
    x = int(randint(0, 32) * 10.)
    y = int(randint(0, 32) * 10.)
    x1 = int(randint(0, 32) * 10.)
    y1 = int(randint(0, 32) * 10.)
    x2 = int(randint(0, 32) * 10.)
    y2 = int(randint(0, 32) * 10.)
    x3 = int(randint(0, 32) * 10.)
    y3 = int(randint(0, 32) * 10.)
    x4 = int(randint(0, 32) * 10.)
    y4 = int(randint(0, 32) * 10.)
    
    rct_color = (int(255),int(255),int(255))
    pointSet3 = (640/2, x)
    pointSet4 = (320/2, x)
    pointSet5 = x * 640
    pointSet6 = y * 640
    pointSet7 = pointSet5 / 500
    pointSet8 = pointSet6 / 500
    pointSet51 = x1 * 640
    pointSet61 = y1 * 640
    pointSet72 = pointSet51 / 500
    pointSet82 = pointSet61 / 500
    pointSet53 = x2 * 640
    pointSet63 = y2 * 640
    pointSet74 = pointSet53 / 500
    pointSet84 = pointSet63 / 500
    pointSet55 = x3 * 640
    pointSet65 = y3 * 640
    pointSet76 = pointSet55 / 500
    pointSet86 = pointSet65 / 500
    pointSet57 = x4 * 640
    pointSet67 = y4 * 640
    pointSet78 = pointSet57 / 500
    pointSet88 = pointSet67 / 500
    print(pointSet5)
    print(pointSet6)
    print(pointSet7)
    print(pointSet8)
    print(pointSet51)
    print(pointSet61)
    print(pointSet72)
    print(pointSet82)
    print(pointSet53)
    print(pointSet63)
    print(pointSet74)
    print(pointSet84)
    print(pointSet55)
    print(pointSet65)
    print(pointSet76)
    print(pointSet86)
    print(pointSet57)
    print(pointSet67)
    print(pointSet78)
    print(pointSet88)
    pointSet9 = (0, pointSet7)
    pointSet10= (0, pointSet8)
    pointSet11 = (pointSet7, 640)
    pointSet12 = (pointSet8, 640)
    pointSet9a = (0, pointSet72)
    pointSet10a= (0, pointSet82)
    pointSet11a = (pointSet72, 640)
    pointSet12a = (pointSet82, 640)
    pointSet9b = (0, pointSet74)
    pointSet10b = (0, pointSet84)
    pointSet11b = (pointSet74, 640)
    pointSet12b = (pointSet84, 640)
    pointSet9c = (0, pointSet76)
    pointSet10c= (0, pointSet86)
    pointSet11c = (pointSet76, 640)
    pointSet12c = (pointSet86, 640)
    pointSet9d = (0, pointSet78)
    pointSet10d = (0, pointSet88)
    pointSet11d = (pointSet78, 640)
    pointSet12d = (pointSet88, 640)
    
    pygame.draw.line(screen, rct_color, (pointSet9), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10),1)
    pygame.draw.line(screen, rct_color, (pointSet11), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9a), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10a),1)
    pygame.draw.line(screen, rct_color, (pointSet11a), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12a),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9b), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10b),1)
    pygame.draw.line(screen, rct_color, (pointSet11b), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12b),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9c), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10c),1)
    pygame.draw.line(screen, rct_color, (pointSet11c), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12c),1)
    
    pygame.draw.line(screen, rct_color, (pointSet9d), (pointSet4),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet10d),1)
    pygame.draw.line(screen, rct_color, (pointSet11d), (pointSet3),1)
    pygame.draw.line(screen, rct_color, (pointSet4), (pointSet12d),1)
    
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_u:
                screen.fill((0,0,0))
                lineLightShow()
                lineLightShow2()
    pygame.display.update()
