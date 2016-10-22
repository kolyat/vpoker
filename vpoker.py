# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import os
import pygame
from pygame.locals import *


combination_names = ['Royal Flush', 'Straight Flush', 'Four of a Kind',
                     'Full House', 'Flush', 'Straight', 'Three of a Kind',
                     'Two Pairs', 'Tens or Better']
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
TABLE_SURFACE_X = TABLE_SURFACE_Y = 0
TABLE_X = TABLE_Y = 20
TABLE_HEIGHT = CELL_HEIGHT * len(poker_winnings)
TABLE_SURFACE_SIZE = (SCREEN_WIDTH, TABLE_HEIGHT + 40)
CARDS_HEIGHT = 200
CARDS_SURFACE_SIZE = (SCREEN_WIDTH, CARDS_HEIGHT + 40)

DISPLAY_MODE = (SCREEN_WIDTH, TABLE_SURFACE_SIZE[1] + CARDS_SURFACE_SIZE[1])

BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue
TABLE_BORDER_COLOR = FONT_COLOR = (155, 155, 0)


# File paths
DATA_DIR = 'data'
FONT_NAME = 'arial.ttf'
FONT_SIZE = 16
ANTIALIASING = 1


# Initialize library and create main window
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY_MODE)
pygame.display.set_caption('Video Poker - Tens or Better')

# Try to initialize game font
try:
    font = pygame.font.Font(os.path.join(DATA_DIR, FONT_NAME), FONT_SIZE)
except pygame.error as error:
    print('Cannot load game font: ', os.path.join(DATA_DIR, FONT_NAME))
    print(error)
    print('Using system default font')
    font = pygame.font.SysFont('None', FONT_SIZE)

# Draw surface for winning combinations table
table_surface = pygame.Surface(TABLE_SURFACE_SIZE)
table_surface.fill(BACKGROUND_COLOR)
table_surface = table_surface.convert()

# Draw cell for winning combination's name
combination_rect = pygame.Rect(TABLE_X, TABLE_Y, COMBINATION_CELL_WIDTH,
                               CELL_HEIGHT)
for name in combination_names:
    pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, combination_rect,
                     BORDER_WIDTH)
    # Print combination's name
    text = font.render(name, ANTIALIASING, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.centerx = combination_rect.centerx
    text_rect.centery = combination_rect.centery
    table_surface.blit(text, text_rect)
    # Draw cells for amount of winning coins of current combination
    winning_rect = pygame.Rect(TABLE_X + COMBINATION_CELL_WIDTH - 1,
                               combination_rect.top, WINNING_CELL_WIDTH,
                               CELL_HEIGHT)
    for c in poker_winnings[name]:
        pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, winning_rect,
                         BORDER_WIDTH)
        # Print number of winning coins
        text = font.render(str(c), ANTIALIASING, FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.centerx = winning_rect.centerx
        text_rect.centery = winning_rect.centery
        winning_rect.left += WINNING_CELL_WIDTH - 1
        table_surface.blit(text, text_rect)
    combination_rect.top += CELL_HEIGHT - 1
screen.blit(table_surface, (TABLE_SURFACE_X, TABLE_SURFACE_Y))

# Main event loop
mainloop = True
while mainloop:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
    pygame.display.flip()

pygame.quit()
