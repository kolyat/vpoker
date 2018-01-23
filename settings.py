# Copyright (c) 2016-2018 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Various game settings"""

#
# Graphical constants
#
FPS = 24
ANIMATION_SPEED = 0.4
# Table dimensions
COMBINATION_CELL_WIDTH = 180
WINNING_CELL_WIDTH = 80
CELL_HEIGHT = 30
BORDER_WIDTH = 2
# Card dimensions
ORIGIN_CARD_WIDTH = 720
ORIGIN_CARD_HEIGHT = 1080
K = 0.25
# CARD_BACKGROUND_WIDTH = 94
# CARD_BACKGROUND_HEIGHT = 140
CARD_WIDTH = int(ORIGIN_CARD_WIDTH * K)
CARD_HEIGHT = int(ORIGIN_CARD_HEIGHT * K)
CARD_BORDER = 10
CARD_BACKGROUND_WIDTH = CARD_WIDTH + CARD_BORDER
CARD_BACKGROUND_HEIGHT = CARD_HEIGHT + CARD_BORDER
# Surfaces dimensions
INDENTATION = 20
TABLE_SURFACE_X = TABLE_SURFACE_Y = 0
TABLE_HEIGHT = CELL_HEIGHT * 9
CARDS_SURFACE_X = TABLE_SURFACE_X
CARDS_SURFACE_Y = TABLE_HEIGHT + INDENTATION*2
DISTANCE_BETWEEN_CARDS = int(CARD_BACKGROUND_WIDTH/10)
# Screen dimensions
SCREEN_WIDTH = CARD_BACKGROUND_WIDTH*5 + DISTANCE_BETWEEN_CARDS*4 + \
               INDENTATION*2
TABLE_SURFACE_SIZE = (SCREEN_WIDTH, TABLE_HEIGHT + INDENTATION*2)
CARDS_SURFACE_SIZE = (SCREEN_WIDTH, CARD_BACKGROUND_HEIGHT + INDENTATION*2)
DISPLAY_MODE = (SCREEN_WIDTH, TABLE_SURFACE_SIZE[1] + CARDS_SURFACE_SIZE[1])
# Table coordinates
TABLE_X = SCREEN_WIDTH/2 - (COMBINATION_CELL_WIDTH + WINNING_CELL_WIDTH*5)/2
TABLE_Y = TABLE_SURFACE_Y + INDENTATION
# Colors
BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue
TABLE_BORDER_COLOR = FONT_COLOR = CARD_BACKGROUND_COLOR = (175, 175, 0)
TABLE_SELECTED_COLOR = (0, 100, 20)
CARD_ACTIVE_COLOR = (208, 113, 30)
CARD_FONT_COLOR = WIN_FONT_COLOR = (0, 0, 0)
WIN_COLOR = (200, 80, 30)
#
# Font paths and options
#
DATA_DIR = 'data'
FONT_NAME = r'fonts\LiberationSans-Regular.ttf'
FONT_SIZE = 16
ANTIALIASING = 0