# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import pygame
from pygame.locals import *


DISPLAY_MODE = (640, 480)
FPS = 24
BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue

# Initialize library and create main window
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY_MODE)
pygame.display.set_caption('Video Poker - Tens or Better')
# Draw background
background = pygame.Surface(screen.get_size())
background.fill(BACKGROUND_COLOR)
background = background.convert()
screen.blit(background, (0, 0))
# Main event loop
mainloop = True
while mainloop:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
    pygame.display.flip()

pygame.quit()
