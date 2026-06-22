import pygame
from pygame.locals import *
from random import *
from sys import exit
import sys
import datetime

pygame.init()
screen = pygame.display.set_mode((640, 640), 0, 32)

def dotArtwork():
    word = "DOTartwork_Rndm_"
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
    zT = word + d + ".py"
    file = open(zT, "w")
    file.write('import pygame' + '\n')
    file.write('from pygame.locals import *' + '\n')
    file.write('pygame.init()' + '\n')
    file.write('screen = pygame.display.set_mode((640, 640), 0, 32)' + '\n')
    y = int(randint(0, 64) * 10)
    crcl_color = (int(255),int(255),int(255))
    circle_radius = int(2)
    file.write('crcl_color = (int(255),int(255),int(255))' + '\n')
    file.write('circle_radius = int(2)' + '\n')
    plot0 = (0, y)
    
    pygame.draw.circle(screen, crcl_color, plot0, circle_radius)

    plot1 = (640, y)
    pygame.draw.circle(screen, crcl_color, plot1, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot0) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot1) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot1 = (10, y)
    
    pygame.draw.circle(screen, crcl_color, plot1, circle_radius)

    plot2 = (630, y)
    pygame.draw.circle(screen, crcl_color, plot2, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot1) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot2) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot2 = (20, y)
    
    pygame.draw.circle(screen, crcl_color, plot2, circle_radius)

    plot3 = (620, y)
    pygame.draw.circle(screen, crcl_color, plot3, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot2) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot3) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot3 = (30, y)
    
    pygame.draw.circle(screen, crcl_color, plot3, circle_radius)

    plot4 = (610, y)
    pygame.draw.circle(screen, crcl_color, plot4, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot3) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot4) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot4 = (40, y)
    
    pygame.draw.circle(screen, crcl_color, plot4, circle_radius)

    plot5 = (600, y)
    pygame.draw.circle(screen, crcl_color, plot5, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot4) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot5) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot5 = (50, y)
    
    pygame.draw.circle(screen, crcl_color, plot5, circle_radius)

    plot6 = (590, y)
    pygame.draw.circle(screen, crcl_color, plot6, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot5) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot6) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot6 = (60, y)
    
    pygame.draw.circle(screen, crcl_color, plot6, circle_radius)

    plot7 = (580, y)
    pygame.draw.circle(screen, crcl_color, plot7, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot6) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot7) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot7 = (70, y)
    
    pygame.draw.circle(screen, crcl_color, plot7, circle_radius)

    plot8 = (570, y)
    pygame.draw.circle(screen, crcl_color, plot8, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot7) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot8) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot8 = (80, y)
    
    pygame.draw.circle(screen, crcl_color, plot8, circle_radius)

    plot9 = (560, y)
    pygame.draw.circle(screen, crcl_color, plot9, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot8) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot9) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot9 = (90, y)
    
    pygame.draw.circle(screen, crcl_color, plot9, circle_radius)

    plot10 = (550, y)
    pygame.draw.circle(screen, crcl_color, plot10, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot9) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot10) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot10 = (100, y)
    
    pygame.draw.circle(screen, crcl_color, plot10, circle_radius)

    plot11 = (540, y)
    pygame.draw.circle(screen, crcl_color, plot11, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot10) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot11) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot11 = (110, y)
    
    pygame.draw.circle(screen, crcl_color, plot11, circle_radius)

    plot12 = (530, y)
    pygame.draw.circle(screen, crcl_color, plot12, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot11) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot12) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot12 = (120, y)
    
    pygame.draw.circle(screen, crcl_color, plot12, circle_radius)

    plot13 = (520, y)
    pygame.draw.circle(screen, crcl_color, plot13, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot12) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot13) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot13 = (130, y)
    
    pygame.draw.circle(screen, crcl_color, plot13, circle_radius)

    plot14 = (510, y)
    pygame.draw.circle(screen, crcl_color, plot14, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot13) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot14) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot14 = (140, y)
    
    pygame.draw.circle(screen, crcl_color, plot14, circle_radius)

    plot15 = (500, y)
    pygame.draw.circle(screen, crcl_color, plot15, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot14) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot15) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot15 = (150, y)
    
    pygame.draw.circle(screen, crcl_color, plot15, circle_radius)

    plot16 = (490, y)
    pygame.draw.circle(screen, crcl_color, plot16, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot15) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot16) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot16 = (160, y)
    
    pygame.draw.circle(screen, crcl_color, plot16, circle_radius)

    plot17 = (480, y)
    pygame.draw.circle(screen, crcl_color, plot17, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot16) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot17) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot17 = (170, y)
    
    pygame.draw.circle(screen, crcl_color, plot17, circle_radius)

    plot18 = (470, y)
    pygame.draw.circle(screen, crcl_color, plot18, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot17) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot18) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot18 = (180, y)
    
    pygame.draw.circle(screen, crcl_color, plot18, circle_radius)

    plot19 = (460, y)
    pygame.draw.circle(screen, crcl_color, plot19, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot18) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot19) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot19 = (190, y)
    
    pygame.draw.circle(screen, crcl_color, plot19, circle_radius)

    plot20 = (450, y)
    pygame.draw.circle(screen, crcl_color, plot20, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot19) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot20) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot20 = (200, y)
    
    pygame.draw.circle(screen, crcl_color, plot20, circle_radius)

    plot21 = (440, y)
    pygame.draw.circle(screen, crcl_color, plot21, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot20) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot21) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot21 = (210, y)
    
    pygame.draw.circle(screen, crcl_color, plot21, circle_radius)

    plot22 = (430, y)
    pygame.draw.circle(screen, crcl_color, plot22, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot21) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot22) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot22 = (220, y)
    
    pygame.draw.circle(screen, crcl_color, plot22, circle_radius)

    plot23 = (420, y)
    pygame.draw.circle(screen, crcl_color, plot23, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot22) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot23) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot23 = (230, y)
    
    pygame.draw.circle(screen, crcl_color, plot23, circle_radius)

    plot24 = (410, y)
    pygame.draw.circle(screen, crcl_color, plot24, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot23) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot24) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot24 = (240, y)
    
    pygame.draw.circle(screen, crcl_color, plot24, circle_radius)

    plot25 = (400, y)
    pygame.draw.circle(screen, crcl_color, plot25, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot24) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot25) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot25 = (250, y)
    
    pygame.draw.circle(screen, crcl_color, plot25, circle_radius)

    plot26 = (390, y)
    pygame.draw.circle(screen, crcl_color, plot26, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot25) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot26) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot26 = (260, y)
    
    pygame.draw.circle(screen, crcl_color, plot26, circle_radius)

    plot27 = (380, y)
    pygame.draw.circle(screen, crcl_color, plot27, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot26) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot27) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot27 = (270, y)
    
    pygame.draw.circle(screen, crcl_color, plot27, circle_radius)

    plot28 = (370, y)
    pygame.draw.circle(screen, crcl_color, plot28, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot27) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot28) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot28 = (280, y)
    
    pygame.draw.circle(screen, crcl_color, plot28, circle_radius)

    plot29 = (360, y)
    pygame.draw.circle(screen, crcl_color, plot29, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot28) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot29) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot29 = (290, y)
    
    pygame.draw.circle(screen, crcl_color, plot29, circle_radius)

    plot30 = (350, y)
    pygame.draw.circle(screen, crcl_color, plot30, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot29) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot30) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot30 = (300, y)
    
    pygame.draw.circle(screen, crcl_color, plot30, circle_radius)

    plot31 = (340, y)
    pygame.draw.circle(screen, crcl_color, plot31, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot30) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot31) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot31 = (310, y)
    
    pygame.draw.circle(screen, crcl_color, plot31, circle_radius)

    plot32 = (330, y)
    pygame.draw.circle(screen, crcl_color, plot32, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot31) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot32) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot32 = (320, y)
    
    pygame.draw.circle(screen, crcl_color, plot32, circle_radius)

    plot33 = (320, y)
    pygame.draw.circle(screen, crcl_color, plot33, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot32) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot33) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot33 = (330, y)
    
    pygame.draw.circle(screen, crcl_color, plot33, circle_radius)

    plot34 = (310, y)
    pygame.draw.circle(screen, crcl_color, plot34, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot33) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot34) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot34 = (340, y)
    
    pygame.draw.circle(screen, crcl_color, plot34, circle_radius)

    plot35 = (300, y)
    pygame.draw.circle(screen, crcl_color, plot35, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot34) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot35) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot35 = (350, y)
    
    pygame.draw.circle(screen, crcl_color, plot35, circle_radius)

    plot36 = (290, y)
    pygame.draw.circle(screen, crcl_color, plot36, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot35) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot36) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot36 = (360, y)
    
    pygame.draw.circle(screen, crcl_color, plot36, circle_radius)

    plot37 = (280, y)
    pygame.draw.circle(screen, crcl_color, plot37, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot36) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot37) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot37 = (370, y)
    
    pygame.draw.circle(screen, crcl_color, plot37, circle_radius)

    plot38 = (270, y)
    pygame.draw.circle(screen, crcl_color, plot38, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot37) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot38) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot38 = (380, y)
    
    pygame.draw.circle(screen, crcl_color, plot38, circle_radius)

    plot39 = (260, y)
    pygame.draw.circle(screen, crcl_color, plot39, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot38) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot39) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot39 = (390, y)
    
    pygame.draw.circle(screen, crcl_color, plot39, circle_radius)

    plot40 = (250, y)
    pygame.draw.circle(screen, crcl_color, plot40, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot39) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot40) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot40 = (400, y)
    
    pygame.draw.circle(screen, crcl_color, plot40, circle_radius)

    plot41 = (240, y)
    pygame.draw.circle(screen, crcl_color, plot41, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot40) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot41) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot41 = (410, y)
    
    pygame.draw.circle(screen, crcl_color, plot41, circle_radius)

    plot42 = (230, y)
    pygame.draw.circle(screen, crcl_color, plot42, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot41) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot42) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot42 = (420, y)
    
    pygame.draw.circle(screen, crcl_color, plot42, circle_radius)

    plot43 = (220, y)
    pygame.draw.circle(screen, crcl_color, plot43, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot42) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot43) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot43 = (430, y)
    
    pygame.draw.circle(screen, crcl_color, plot43, circle_radius)

    plot44 = (210, y)
    pygame.draw.circle(screen, crcl_color, plot44, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot43) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot44) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot44 = (440, y)
    
    pygame.draw.circle(screen, crcl_color, plot44, circle_radius)

    plot45 = (200, y)
    pygame.draw.circle(screen, crcl_color, plot45, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot44) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot45) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot45 = (450, y)
    
    pygame.draw.circle(screen, crcl_color, plot45, circle_radius)

    plot46 = (190, y)
    pygame.draw.circle(screen, crcl_color, plot46, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot45) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot46) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot46 = (460, y)
    
    pygame.draw.circle(screen, crcl_color, plot46, circle_radius)

    plot47 = (180, y)
    pygame.draw.circle(screen, crcl_color, plot47, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot46) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot47) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot47 = (470, y)
    
    pygame.draw.circle(screen, crcl_color, plot47, circle_radius)

    plot48 = (170, y)
    pygame.draw.circle(screen, crcl_color, plot48, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot47) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot48) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot48 = (480, y)
    
    pygame.draw.circle(screen, crcl_color, plot48, circle_radius)

    plot49 = (160, y)
    pygame.draw.circle(screen, crcl_color, plot49, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot48) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot49) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot49 = (490, y)
    
    pygame.draw.circle(screen, crcl_color, plot49, circle_radius)

    plot50 = (150, y)
    pygame.draw.circle(screen, crcl_color, plot50, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot49) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot50) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot50 = (500, y)
    
    pygame.draw.circle(screen, crcl_color, plot50, circle_radius)

    plot51 = (140, y)
    pygame.draw.circle(screen, crcl_color, plot51, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot50) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot51) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot51 = (510, y)
    
    pygame.draw.circle(screen, crcl_color, plot51, circle_radius)

    plot52 = (130, y)
    pygame.draw.circle(screen, crcl_color, plot52, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot51) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot52) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot52 = (520, y)
    
    pygame.draw.circle(screen, crcl_color, plot52, circle_radius)

    plot53 = (120, y)
    pygame.draw.circle(screen, crcl_color, plot53, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot52) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot53) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot53 = (530, y)
    
    pygame.draw.circle(screen, crcl_color, plot53, circle_radius)

    plot54 = (110, y)
    pygame.draw.circle(screen, crcl_color, plot54, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot53) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot54) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot54 = (540, y)
    
    pygame.draw.circle(screen, crcl_color, plot54, circle_radius)

    plot55 = (100, y)
    pygame.draw.circle(screen, crcl_color, plot55, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot54) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot55) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot55 = (550, y)
    
    pygame.draw.circle(screen, crcl_color, plot55, circle_radius)

    plot56 = (90, y)
    pygame.draw.circle(screen, crcl_color, plot56, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot55) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot56) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot56 = (560, y)
    
    pygame.draw.circle(screen, crcl_color, plot56, circle_radius)

    plot57 = (80, y)
    pygame.draw.circle(screen, crcl_color, plot57, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot56) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot57) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot57 = (570, y)
    
    pygame.draw.circle(screen, crcl_color, plot57, circle_radius)

    plot58 = (70, y)
    pygame.draw.circle(screen, crcl_color, plot58, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot57) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot58) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot58 = (580, y)
    
    pygame.draw.circle(screen, crcl_color, plot58, circle_radius)

    plot59 = (60, y)
    pygame.draw.circle(screen, crcl_color, plot59, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot58) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot59) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot59 = (590, y)
    
    pygame.draw.circle(screen, crcl_color, plot59, circle_radius)

    plot60 = (50, y)
    pygame.draw.circle(screen, crcl_color, plot60, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot59) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot60) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot60 = (600, y)
    
    pygame.draw.circle(screen, crcl_color, plot60, circle_radius)

    plot61 = (40, y)
    pygame.draw.circle(screen, crcl_color, plot61, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot60) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot61) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot61 = (610, y)
    
    pygame.draw.circle(screen, crcl_color, plot61, circle_radius)

    plot62 = (30, y)
    pygame.draw.circle(screen, crcl_color, plot62, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot61) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot62) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot62 = (620, y)
    
    pygame.draw.circle(screen, crcl_color, plot62, circle_radius)

    plot63 = (20, y)
    pygame.draw.circle(screen, crcl_color, plot63, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot62) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot63) + ', circle_radius)' + '\n')


    y = int(randint(0, 64) * 10)
    
    plot63 = (630, y)
    
    pygame.draw.circle(screen, crcl_color, plot63, circle_radius)

    plot64 = (10, y)
    pygame.draw.circle(screen, crcl_color, plot64, circle_radius)
    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot63) + ', circle_radius)' + '\n')

    file.write('pygame.draw.circle(screen, crcl_color, ' + str(plot64) + ', circle_radius)' + '\n')
    file.write('pygame.display.update()' + '\n')
    file.close()
    return

def saveAsBMP():
    word = "DOTartwork_Rndm_"
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
    zQ = word + ".html"
    getImage = screen
    pygame.image.save(getImage, zS)
    file2 = open(zQ, "a")
    file2.write('<p>' + zS + '</p></br>' + '\n')
    file2.write('<img src="' + zS + '">' + '\n')
    file2.close()
    return

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_q:
                screen.fill((0,0,0))
                dotArtwork()
                saveAsBMP()
                
    pygame.display.update()

