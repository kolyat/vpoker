# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import pygame
from pygame.locals import *


DISPLAY_MODE = (640, 480)
BACKGROUND_COLOR = (11, 111, 0)


# Initialize library and create main window
pygame.init()
screen = pygame.display.set_mode(DISPLAY_MODE)
pygame.display.set_caption('Video Poker - Tens or Better')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BACKGROUND_COLOR)
