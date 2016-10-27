# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main unit of vpoker
"""

import os
import random
import time
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
ANIMATION_SPEED = 0.4

BACKGROUND_COLOR = (0, 65, 15)  # (0, 25, 50) - dark blue
TABLE_BORDER_COLOR = FONT_COLOR = CARD_BACKGROUND_COLOR = (175, 175, 0)
TABLE_SELECTED_COLOR = (0, 100, 20)
CARD_ACTIVE_COLOR = (208, 113, 30)
CARD_FONT_COLOR = (0, 0, 0)


# File paths
DATA_DIR = 'data'
FONT_NAME = 'arial.ttf'
FONT_SIZE = 16
ANTIALIASING = 0


class Card(object):
    """Represents playing card"""

    def __init__(self, centerx=0):
        """
        Class Card constructor

        :param centerx: x-coordinate of card's center, default = 0
        :type: int
        :arg centery: y-coordinate of card's center
        :type: int
        :arg active: currently selected card
        :type: bool
        :arg card: represents playing card or it's back
        :type: str ('BACK')
        :type: tuple
        :arg: held: if kept in hand
        """
        self.centerx = centerx
        self.centery = int(CARD_BACKGROUND_HEIGHT/2)
        self.active = False
        self.card = 'BACK'
        self.held = False

    def draw(self):
        """Draw card with background and text"""

        # Draw card's background
        background_rect = pygame.Rect(
            self.centerx - int(CARD_BACKGROUND_WIDTH/2),
            self.centery - int(CARD_BACKGROUND_HEIGHT/2),
            CARD_BACKGROUND_WIDTH, CARD_BACKGROUND_HEIGHT)
        if self.active:
            pygame.draw.rect(cards_surface, CARD_ACTIVE_COLOR,
                             background_rect, 0)
        else:
            pygame.draw.rect(cards_surface, CARD_BACKGROUND_COLOR,
                             background_rect, 0)

        # Try to load card's image
        raw_image = pygame.image.load(
            os.path.join(DATA_DIR, ''.join(self.card) + '.png'))
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

    def set_card(self, current_card):
        """
        Set card from playing deck

        :param current_card: card from deck
        :type: str ('BACK')
        :type: tuple
        """

        self.card = current_card

    def set_active(self, active=False):
        """
        Set state of a card: active or not

        :param: active: card's state
        :type: bool
        """

        self.active = active

    def get_held(self):
        """
        Get 'held' status

        :return: 'held' status
        :type: bool
        """

        return self.held

    def set_held(self, hold=False):
        """
        Set status 'held'

        :param hold: 'held' status
        :type: bool
        """

        self.held = hold


def draw_table():
    """
    Draw table with winning combinations
    """

    # Draw surface for winning combinations table
    table_surface = pygame.Surface(TABLE_SURFACE_SIZE)
    table_surface.fill(BACKGROUND_COLOR)
    # table_surface = table_surface.convert()

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
        for i, item in enumerate(poker_winnings[name], start=1):
            if coins == i:
                pygame.draw.rect(table_surface, TABLE_SELECTED_COLOR,
                                 winning_rect, 0)
            pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, winning_rect,
                             BORDER_WIDTH)
            # Print number of winning coins
            text = font.render(str(item), ANTIALIASING, FONT_COLOR)
            text_rect = text.get_rect()
            text_rect.centerx = winning_rect.centerx
            text_rect.centery = winning_rect.centery
            winning_rect.left += WINNING_CELL_WIDTH - 1
            table_surface.blit(text, text_rect)
        combination_rect.top += CELL_HEIGHT - 1
    screen.blit(table_surface, (TABLE_SURFACE_X, TABLE_SURFACE_Y))


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

# Main game loop
game_loop = True
while game_loop:
    coins = 1  # Number of inserted coins
    # Initialize playing deck
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(tuple(suit + rank))
    # Initialize random generator with current system time
    random.seed(None)
    # Initialize cards
    cards = []
    for x in range(int(INDENTATION + CARD_BACKGROUND_WIDTH / 2),
                   (CARD_BACKGROUND_WIDTH + INDENTATION + 11) * 5,
                   CARD_BACKGROUND_WIDTH + INDENTATION + 11):
        cards.append(Card(x))

    # Draw surface for cards
    cards_surface = pygame.Surface(CARDS_SURFACE_SIZE)
    cards_surface.fill(BACKGROUND_COLOR)
    # cards_surface = cards_surface.convert()

    # Stage 1: insert coins to select amount of winning
    draw_table()
    for card in cards:
        card.draw()
    wait = True
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if coins < 5:
                        coins += 1
                if event.key == K_DOWN:
                    if coins > 1:
                        coins -= 1
                if event.key == K_RETURN:
                    wait = False
                draw_table()
            if event.type == QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

    # Stage 2: hand out cards, wait for player to hold some cards
    active_card = 0
    cards[active_card].set_active(True)
    for card in cards:
        random_card = deck.pop(random.randint(0, len(deck)-1))
        card.set_card(random_card)
        card.draw()
        pygame.display.flip()
        time.sleep(ANIMATION_SPEED)
    wait = True
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if active_card > 0:
                        cards[active_card].set_active(False)
                        active_card -= 1
                        cards[active_card].set_active(True)
                if event.key == K_RIGHT:
                    if active_card < 4:
                        cards[active_card].set_active(False)
                        active_card += 1
                        cards[active_card].set_active(True)
                if event.key == K_SPACE:
                    if cards[active_card].get_held():
                        cards[active_card].set_held(False)
                    else:
                        cards[active_card].set_held(True)
                if event.key == K_RETURN:
                    wait = False
                for card in cards:
                    card.draw()
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            pygame.display.flip()
    cards[active_card].set_active(False)

    # Stage 3: remove cards that were not held
    for card in cards:
        if not card.get_held():
            card.set_card('BACK')
        card.draw()
    pygame.display.flip()
    time.sleep(ANIMATION_SPEED)

    # Stage 4: hand out new cards
    for card in cards:
        if not card.get_held():
            random_card = deck.pop(random.randint(0, len(deck)-1))
            card.set_card(random_card)
        card.draw()
        pygame.display.flip()
        time.sleep(ANIMATION_SPEED)

    # Stage 5
