# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import os
import pygame
from pygame.locals import *


suits = {
    'S': '♠',  # Spades
    'C': '♣',  # Clubs
    'H': '♥',  # Hearts
    'D': '♦'   # Diamonds
}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

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

INDENTATION = 20
COMBINATION_CELL_WIDTH = 200
WINNING_CELL_WIDTH = 80
CELL_HEIGHT = 30
BORDER_WIDTH = 2
TABLE_SURFACE_X = TABLE_SURFACE_Y = 0
TABLE_X = TABLE_Y = INDENTATION
TABLE_HEIGHT = CELL_HEIGHT * len(poker_winnings)
TABLE_SURFACE_SIZE = (SCREEN_WIDTH, TABLE_HEIGHT + INDENTATION*2)
CARD_BACKGROUND_WIDTH = 94
CARD_BACKGROUND_HEIGHT = 140
CARD_WIDTH = 86
CARD_HEIGHT = 130
CARDS_SURFACE_X = TABLE_SURFACE_X
CARDS_SURFACE_Y = TABLE_SURFACE_SIZE[1]
CARDS_SURFACE_SIZE = (SCREEN_WIDTH, CARD_BACKGROUND_HEIGHT + INDENTATION*2)

DISPLAY_MODE = (SCREEN_WIDTH, TABLE_SURFACE_SIZE[1] + CARDS_SURFACE_SIZE[1])

BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue
TABLE_BORDER_COLOR = FONT_COLOR = CARD_BACKGROUND_COLOR = (155, 155, 0)
CARD_ACTIVE_COLOR = (208, 113, 30)
CARD_FONT_COLOR = (0, 0, 0)


# File paths
DATA_DIR = 'data'
FONT_NAME = 'arial.ttf'
FONT_SIZE = 16
ANTIALIASING = 1


class Card(object):
    """Represents playing card"""

    def __init__(self, centerx=0):
        self.centerx = centerx
        self.centery = int(CARD_BACKGROUND_HEIGHT/2)
        self.background_rect = pygame.Rect(
            centerx - int(CARD_BACKGROUND_WIDTH/2),
            self.centery - int(CARD_BACKGROUND_HEIGHT/2),
            CARD_BACKGROUND_WIDTH, CARD_BACKGROUND_HEIGHT)
        self.active = False
        self.card = 'BACK'
        self.held = False

    def draw(self):
        """Draw card with background and text"""

        # Draw card's background
        if self.active:
            pygame.draw.rect(cards_surface, CARD_ACTIVE_COLOR,
                             self.background_rect, 0)
        else:
            pygame.draw.rect(cards_surface, CARD_BACKGROUND_COLOR,
                             self.background_rect, 0)

        # Try to load card's image
        raw_image = pygame.image.load(os.path.join(DATA_DIR,
                                                   (str(self.card) + '.png')))
        if raw_image:
            card_image = pygame.transform.scale(raw_image,
                                                (CARD_WIDTH, CARD_HEIGHT))
        else:
            print('Cannot load image: ',
                  os.path.join(DATA_DIR, (str(self.card) + '.png')))
            print('Using text instead')
            if self.card == 'BACK':
                card_image = font.render('BACK', ANTIALIASING,
                                         CARD_FONT_COLOR)
            else:
                card_image = font.render((suits[self.card[0]] + self.card[1]),
                                         ANTIALIASING, CARD_FONT_COLOR)
        # Draw image
        card_rect = card_image.get_rect()
        card_rect.centerx = self.centerx
        card_rect.centery = self.centery
        cards_surface.blit(card_image, (card_rect.left, card_rect.top))
        screen.blit(cards_surface, (CARDS_SURFACE_X, CARDS_SURFACE_Y))

        # Draw status text
        if self.held:
            status = font.render('HELD', ANTIALIASING, FONT_COLOR)
        else:
            status = font.render('HELD', ANTIALIASING, BACKGROUND_COLOR)
        status_rect = status.get_rect()
        status_rect.centerx = self.centerx
        status_rect.centery = self.centery + int(CARD_BACKGROUND_HEIGHT/2) +\
            int(status_rect.height/2) + int(INDENTATION/2)
        cards_surface.blit(status, (status_rect.left, status_rect.top))


def init_deck():
    """
    Initialize playing deck

    :return: deck with 52 playing cards
    :type: list
    """

    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(tuple(suit + rank))
    return deck

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

# Draw surface for cards
cards_surface = pygame.Surface(CARDS_SURFACE_SIZE)
cards_surface.fill(BACKGROUND_COLOR)
cards_surface = cards_surface.convert()

# Initialize cards
cards = []
for x in range(int(INDENTATION + CARD_BACKGROUND_WIDTH/2),
               (CARD_BACKGROUND_WIDTH + INDENTATION + 11)*5,
               CARD_BACKGROUND_WIDTH + INDENTATION + 11):
    cards.append(Card(x))

# Draw cards
for card in cards:
    card.draw()

# Main event loop
mainloop = True
while mainloop:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
    pygame.display.flip()

pygame.quit()
