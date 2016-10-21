# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import pygame
from pygame.locals import *


# 'Tens or Better' winning combinations
poker_winnings = {
    'Royal Flush':     [500, 1000, 2000, 3000, 4000],
    'Straight Flush':  [50,  100,  150,  200,  250],
    'Four of a Kind':  [25,  50,   75,   100,  125],
    'Full House':      [6,   12,   18,   24,   30],
    'Flush':           [5,   10,   15,   20,   25],
    'Straight':        [4,   8,    12,   16,   20],
    'Three of a Kind': [3,   6,    9,    12,   15],
    'Two Pairs':       [2,   4,    6,    8,    10],
    'Tens or Better':  [1,   2,    3,    4,    5]
}


# Graphical constants
SCREEN_WIDTH = 640
FPS = 24

COMBINATION_CELL_WIDTH = 200
WINNING_CELL_WIDTH = 80
CELL_HEIGHT = 30
BORDER_WIDTH = 2
TABLE_X = TABLE_Y = 20
TABLE_HEIGHT = CELL_HEIGHT * len(poker_winnings)
TABLE_SURFACE_SIZE = (SCREEN_WIDTH, TABLE_HEIGHT + 40)
CARDS_HEIGHT = 200
CARDS_SURFACE_SIZE = (SCREEN_WIDTH, CARDS_HEIGHT + 40)

DISPLAY_MODE = (SCREEN_WIDTH, TABLE_SURFACE_SIZE[1] + CARDS_SURFACE_SIZE[1])

BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue
TABLE_BORDER_COLOR = (155, 155, 0)


# Initialize library and create main window
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY_MODE)
pygame.display.set_caption('Video Poker - Tens or Better')

# Draw surface for winning combinations table
table_surface = pygame.Surface(TABLE_SURFACE_SIZE)
table_surface.fill(BACKGROUND_COLOR)
table_surface = table_surface.convert()

# Draw cell for winning combination's name
combination_rect = pygame.Rect(TABLE_X, TABLE_Y, COMBINATION_CELL_WIDTH,
                               CELL_HEIGHT)
for c in poker_winnings:
    pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, combination_rect,
                     BORDER_WIDTH)
    # Draw cells for amount of winning coins of current combination
    winning_rect = pygame.Rect(TABLE_X + COMBINATION_CELL_WIDTH - 1,
                               combination_rect.top, WINNING_CELL_WIDTH,
                               CELL_HEIGHT)
    for w in range(5):
        pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, winning_rect,
                         BORDER_WIDTH)
        winning_rect.left += WINNING_CELL_WIDTH - 1
    combination_rect.top += CELL_HEIGHT - 1
screen.blit(table_surface, (0, 0))

# Main event loop
mainloop = True
while mainloop:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
    pygame.display.flip()

pygame.quit()
