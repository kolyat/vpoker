# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of vpoker
"""

import os
import random
import time
import pygame
from pygame.locals import *

from tens_or_better import *


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
TABLE_HEIGHT = CELL_HEIGHT * len(poker_winnings)
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
        :arg back: will show cards back if active (card is not defined)
        :type: bool
        :arg suit: card's suit
        :type: str
        :arg rank: card's rank
        :type: str
        :arg: held: if kept in hand
        :type: bool
        """
        if type(centerx) not in (int, float):
            self.centerx = 0
        elif centerx < 0:
            self.centerx = 0
        elif centerx > SCREEN_WIDTH:
            self.centerx = int(SCREEN_WIDTH)
        else:
            self.centerx = int(centerx)
        self.centery = int(CARD_BACKGROUND_HEIGHT/2)
        self.active = False
        self.back = True
        self.suit = ''
        self.rank = ''
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
        if self.back:
            raw_image = pygame.image.load(
                os.path.join(DATA_DIR, ''.join('BACK') + '.png'))
        else:
            raw_image = pygame.image.load(
                os.path.join(DATA_DIR, ''.join(
                    self.suit + self.rank) + '.png'))
        if raw_image:
            card_image = pygame.transform.scale(raw_image,
                                                (CARD_WIDTH, CARD_HEIGHT))
        else:
            print('Cannot load image: ',
                  os.path.join(DATA_DIR, (self.suit + self.rank + '.png')))
            print('Using text instead')
            if self.back:
                card_image = font.render('BACK', ANTIALIASING,
                                         CARD_FONT_COLOR)
            else:
                card_image = font.render(suits[self.suit] + self.rank,
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
        pygame.display.flip()

    def set_card(self, current_card):
        """
        Set card from playing deck

        :param current_card: card from deck
        :type: tuple

        :raises TypeError: if 'current_card' is not tuple
        :raises ValueError: if length of 'current_card' is not equal to 2
        :raises KeyError: if 'current_card' contains not valid suit/rank
        """

        if type(current_card) != tuple:
            raise TypeError
        if len(current_card) != 2:
            raise ValueError
        if current_card[0] not in suit_list:
            raise KeyError
        if current_card[1] not in ranks:
            raise KeyError
        self.suit = current_card[0]
        self.rank = current_card[1]
        self.set_back(False)

    def get_suit(self):
        """
        Get card's suit

        :return: card's suit
        :type: string
        """

        return self.suit

    def get_rank(self):
        """
        Get card's rank

        :return: card's rank
        :type: string
        """

        return self.rank

    def set_active(self, active=False):
        """
        Set state of a card: active or not

        :param: active: card's state
        :type: bool

        :raises TypeError: if 'active' is not bool
        """

        if type(active) != bool:
            raise TypeError
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

        :raises TypeError: if 'hold' is not boolean
        """

        if type(hold) != bool:
            raise TypeError
        self.held = hold

    def set_back(self, back=True):
        """
        Sets card back parameter

        :param back: back parameter
        :type: bool

        :raises TypeError: if 'back' is not bool
        """

        if type(back) != bool:
            raise TypeError
        self.back = back


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
        if name == win_combo:
            pygame.draw.rect(table_surface, WIN_COLOR,
                             combination_rect, 0)
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

            if coins == i and name == win_combo:
                pygame.draw.rect(table_surface, CARD_BACKGROUND_COLOR,
                                 winning_rect, 0)
            elif coins == i:
                pygame.draw.rect(table_surface, TABLE_SELECTED_COLOR,
                                 winning_rect, 0)
            elif name == win_combo:
                pygame.draw.rect(table_surface, WIN_COLOR,
                                 winning_rect, 0)
            else:
                pass
            pygame.draw.rect(table_surface, TABLE_BORDER_COLOR, winning_rect,
                             BORDER_WIDTH)
            # Print number of winning coins
            if coins == i and name == win_combo:
                font.set_bold(True)
                text = font.render(str(item), ANTIALIASING, WIN_FONT_COLOR)
            else:
                text = font.render(str(item), ANTIALIASING, FONT_COLOR)
            text_rect = text.get_rect()
            text_rect.centerx = winning_rect.centerx
            text_rect.centery = winning_rect.centery
            table_surface.blit(text, text_rect)
            font.set_bold(False)
            winning_rect.left += WINNING_CELL_WIDTH - 1
        combination_rect.top += CELL_HEIGHT - 1
    screen.blit(table_surface, (TABLE_SURFACE_X, TABLE_SURFACE_Y))
    pygame.display.flip()


def init_deck():
    """
    Initialize playing deck with 52 cards

    :return: deck with 52 cards
    :type: list of tuples
    """

    raw_deck = []
    for suit in suits:
        for rank in ranks:
            raw_card = list()
            raw_card.append(suit)
            raw_card.append(rank)
            raw_deck.append(tuple(raw_card))
    return raw_deck


def main():
    """Main function"""

    # Init variables
    clock = pygame.time.Clock()
    global coins
    global win_combo
    global cards_surface

    # Main game loop
    game_loop = True
    while game_loop:
        coins = 1
        win_combo = ''
        # Initialize playing deck
        deck = init_deck()
        # Initialize random generator with current system time
        random.seed(None)
        # Initialize cards
        cards = []
        for x in range(int(INDENTATION + CARD_BACKGROUND_WIDTH / 2),
                       (CARD_BACKGROUND_WIDTH + DISTANCE_BETWEEN_CARDS) * 5,
                       CARD_BACKGROUND_WIDTH + DISTANCE_BETWEEN_CARDS):
            cards.append(Card(x))

        # Draw surface for cards
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

        # Stage 2: hand out cards, wait for player to hold some cards
        active_card = 0
        for card in cards:
            random_card = deck.pop(random.randint(0, len(deck)-1))
            card.set_card(random_card)
            card.draw()
            time.sleep(ANIMATION_SPEED)
        cards[active_card].set_active(True)
        cards[active_card].draw()
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
        cards[active_card].set_active(False)
        cards[active_card].draw()

        # Stage 3: remove cards that were not held
        for card in cards:
            if not card.get_held():
                card.set_back(True)
                card.draw()
        time.sleep(ANIMATION_SPEED)

        # Stage 4: hand out new cards
        for card in cards:
            if not card.get_held():
                random_card = deck.pop(random.randint(0, len(deck)-1))
                card.set_card(random_card)
                card.draw()
                time.sleep(ANIMATION_SPEED)

        # Stage 5: check for winning combinations and show if any
        card_suits = list()
        card_ranks = list()
        for card in cards:
            card_suits.append(card.get_suit())
            card_ranks.append(card.get_rank())
        combo_check = ComboCheck()
        win_combo = combo_check(card_suits, card_ranks)
        if win_combo:
            draw_table()
        # Wait for player
        wait = True
        while wait:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        wait = False
                    if event.key == K_ESCAPE:
                        pygame.event.post(QUIT)
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)

# Initialize library and create main window
pygame.init()
screen = pygame.display.set_mode(DISPLAY_MODE)
pygame.display.set_caption('Video Poker - ' + CAPTION)
# Try to initialize game font
try:
    font = pygame.font.Font(os.path.join(DATA_DIR, FONT_NAME), FONT_SIZE)
except FileNotFoundError as sys_error:
    print('File not found: ', os.path.join(DATA_DIR, FONT_NAME))
    print(sys_error)
    font = pygame.font.SysFont('None', FONT_SIZE)
except pygame.error as error:
    print('Cannot load game font: ', os.path.join(DATA_DIR, FONT_NAME))
    print(error)
    print('Using system default font')
    font = pygame.font.SysFont('None', FONT_SIZE)
#
# Global variables
#
coins = 1  # Number of inserted coins
win_combo = ''
cards_surface = pygame.Surface(CARDS_SURFACE_SIZE)
# Start game
if __name__ == '__main__':
    main()
