from pygame.locals import *
import pygame,os
import time
from sys import exit

SCREEN_SIZE = (1280,800)
pygame.init()


leng = len(os.listdir("pics/"))

for k in range(1, leng):
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    bg = pygame.image.load("pics/{}.jpg".format(k)).convert()
    screen.blit(bg,(0,0))
    pygame.display.update()
#    time.sleep(0.01)
