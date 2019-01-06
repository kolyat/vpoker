# Copyright (c) 2016-2019 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Main module of vpoker"""

import sys
import os
import random
import time
import collections
import logging
import sqlite3
import pygame
from pygame.locals import *
from settings import *


class Dbase:
    player = 'player'
    creds = None

    def __init__(self, f):
        self.conn = sqlite3.connect(f)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('SELECT creds FROM players WHERE player=?',
                                (self.player,))
            self.creds = self.cursor.fetchone()[0]
        except sqlite3.OperationalError:
            self.cursor.execute(
                'CREATE TABLE players'
                ' (player TEXT NOT NULL UNIQUE, creds BIGINT)'
            )

    def get_creds(self):
        return self.creds

    def set_creds(self, c):
        self.creds = c

    def decrease_creds(self):
        self.set_creds(self.get_creds() - 1)

    def increase_creds(self):
        self.set_creds(self.get_creds() + 1)

    def update_creds(self):
        self.cursor.execute(
            'INSERT OR REPLACE INTO players (player, creds) VALUES (?, ?)',
            (self.player, self.creds)
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class Card:
    """Represents playing card"""

    def __init__(self, centerx=0):
        """Class Card constructor

        :param centerx: x-coordinate of card's center, default = 0
        :type centerx: int
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
        # If card is now selected
        self.active = False
        # Show card's back when card is not defined
        self.back = True
        self.suit = ''
        self.rank = ''
        # If stays on hand
        self.held = False

    def draw(self):
        """Draw card with background and text
        """
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
            try:
                raw_image = pygame.image.load(
                    os.path.join(DATA_DIR, ''.join('BACK') + '.png'))
            except pygame.error:
                logging.error('Cannot load image: %s',
                              os.path.join(DATA_DIR, ''.join('BACK') + '.png'))
                raw_image = None
        else:
            try:
                raw_image = pygame.image.load(
                    os.path.join(DATA_DIR, ''.join(
                        self.suit + self.rank) + '.png'))
            except pygame.error:
                logging.error(
                    'Cannot load image: %s',
                    os.path.join(DATA_DIR, (self.suit + self.rank + '.png'))
                )
                raw_image = None
        if raw_image:
            card_image = pygame.transform.scale(raw_image,
                                                (CARD_WIDTH, CARD_HEIGHT))
        else:
            logging.error('Using text instead of image')
            if self.back:
                card_image = card_font.render('BACK', ANTIALIASING,
                                              CARD_FONT_COLOR)
            else:
                card_image = card_font.render(suits[self.suit] + self.rank,
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
        """Set card from playing deck

        :param current_card: card from deck
        :type current_card: tuple

        :raise TypeError: 'current_card' is not tuple
        :raise ValueError: length of 'current_card' is not equal to 2
        :raise KeyError: 'current_card' contains not valid suit/rank
        """
        if type(current_card) != tuple:
            raise TypeError
        if len(current_card) != 2:
            raise ValueError
        if current_card[0] not in suit_list:
            raise KeyError
        if current_card[1] not in ranks:
            raise KeyError
        self.suit, self.rank = current_card
        self.set_back(False)

    def get_suit(self):
        """Get card's suit

        :return: card's suit
        :type: str
        """
        return self.suit

    def get_rank(self):
        """Get card's rank

        :return: card's rank
        :type: str
        """
        return self.rank

    def set_active(self, active=False):
        """Set state of a card: active or inactive

        :param: active: card's state
        :type active: bool

        :raise TypeError: 'active' is not bool
        """
        if type(active) != bool:
            raise TypeError
        self.active = active

    def get_held(self):
        """Get 'held' status

        :return: 'held' status
        :type: bool
        """
        return self.held

    def set_held(self, hold=False):
        """Set status 'held'

        :param hold: 'held' status
        :type hold: bool

        :raise TypeError: 'hold' is not boolean
        """
        if type(hold) != bool:
            raise TypeError
        self.held = hold

    def set_back(self, back=True):
        """Set card's back parameter

        :param back: back parameter
        :type back: bool

        :raise TypeError: 'back' is not bool
        """
        if type(back) != bool:
            raise TypeError
        self.back = back


def draw_table():
    """Draw table with winning combinations and show available creds
    """
    global dbase
    global table_surface
    # Draw surface for winning combinations table
    table_surface.fill(BACKGROUND_COLOR)
    # table_surface = table_surface.convert()
    # Print available creds
    text = font.render('Creds: {}'.format(dbase.get_creds()),
                       ANTIALIASING, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.centerx = INDENTATION + int(text.get_width()/2)
    text_rect.centery = CREDS_Y
    table_surface.blit(text, text_rect)
    # Draw cell for winning combination's name
    combination_rect = pygame.Rect(TABLE_X, TABLE_Y, COMBINATION_CELL_WIDTH,
                                   CELL_HEIGHT)
    for name in combination_names:
        if name == win_combo:
            pygame.draw.rect(table_surface, WIN_COLOR, combination_rect, 0)
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


def show_message():
    """Show message if no creds left
    """
    global table_surface
    text = font.render('No creds left', ANTIALIASING, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.centerx = INDENTATION + int(text.get_width()/2)
    text_rect.centery = MESSAGE_Y
    table_surface.blit(text, text_rect)
    screen.blit(table_surface, (TABLE_SURFACE_X, TABLE_SURFACE_Y))
    pygame.display.flip()


def init_deck():
    """Initialize playing deck with 52 cards

    :return: deck with 52 cards
    :type: list of tuples
    """
    return [(suit, rank) for suit in suits for rank in ranks]


def game():
    """Main game function
    """
    # Init variables
    clock = pygame.time.Clock()
    global dbase
    global coins
    global win_combo
    global cards_surface
    # Main game loop
    while True:
        coins = 0
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
        #
        # Stage 1: insert coins to select amount of winning
        #
        draw_table()
        for card in cards:
            card.draw()
        if dbase.get_creds() < 1:
            show_message()
            while True:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        pygame.quit()
                        exit(0)
        wait = True
        while wait:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if coins < 5 and dbase.get_creds() > 0:
                            coins += 1
                            dbase.decrease_creds()
                    if event.key == K_DOWN:
                        if coins > 0:
                            coins -= 1
                            dbase.increase_creds()
                    if event.key == K_RETURN:
                        wait = False
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                    draw_table()
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)
        #
        # Stage 2: hand out cards, wait for player to hold some cards
        #
        dbase.update_creds()
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
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                for card in cards:
                    card.draw()
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)
        cards[active_card].set_active(False)
        cards[active_card].draw()
        #
        # Stage 3: remove cards that were not held
        #
        for card in cards:
            if not card.get_held():
                card.set_back(True)
                card.draw()
        time.sleep(ANIMATION_SPEED)
        #
        # Stage 4: hand out new cards
        #
        for card in cards:
            if not card.get_held():
                random_card = deck.pop(random.randint(0, len(deck)-1))
                card.set_card(random_card)
                card.draw()
                time.sleep(ANIMATION_SPEED)
        #
        # Stage 5: check for winning combinations and show if any
        #
        card_suits = []
        card_ranks = []
        for card in cards:
            card_suits.append(card.get_suit())
            card_ranks.append(card.get_rank())
        win_combo = combo_check(card_suits, card_ranks)
        if win_combo:
            dbase.set_creds(
                dbase.get_creds() + poker_winnings[win_combo][coins-1])
            dbase.update_creds()
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
                        pygame.event.post(pygame.event.Event(QUIT))
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)


def menu():
    """Main menu

    :return: game and poker types
    :type: str
    """

    def clrscr():
        """Clear screen and show title
        """
        if sys.platform.startswith('linux') or \
                sys.platform.startswith('darwin'):
            os.system('clear')
        if sys.platform.startswith('win'):
            os.system('cls')
        print()
        print('======')
        print('vpoker')
        print('======')
        print()
        print()

    global dbase
    if type(dbase.creds) == int:
        game_types = collections.OrderedDict((
            ('1', 'Continue game'),
            ('2', 'New game'),
            ('0', 'Exit')
        ))
        item = ''
        while item not in game_types.keys():
            clrscr()
            for k, v in game_types.items():
                print(' - '.join((k, v)))
            print()
            item = input('> ', )
        game_type = game_types[item]
        if game_type == 'Exit':
            return game_type, 'Exit'
    else:
        game_type = 'New game'

    poker_types = collections.OrderedDict((
        ('1', 'Tens or Better'),
        ('2', 'Jacks or Better'),
        ('0', 'Exit')
    ))
    item = ''
    while item not in poker_types.keys():
        clrscr()
        print('Select video poker type')
        print()
        for k, v in poker_types.items():
            print(' - '.join((k, v)))
        print()
        item = input('> ', )
    poker_type = poker_types[item]
    return game_type, poker_type


# For testing purposes
if __name__ == 'vpoker':
    suits = {
        'S': '♠',
        'C': '♣',
        'H': '♥',
        'D': '♦'
    }
    suit_list = suits.keys()
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

if __name__ == '__main__':
    # Init logger
    logging.basicConfig(
        filename='vpoker.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.ERROR
    )
    dbase = Dbase(DB_FILE)
    # Call main menu
    game_t, poker_t = menu()
    # Initialize poker engine
    if poker_t == 'Tens or Better':
        from engine.tens_or_better import *
        combo_check = TensOrBetter()
    elif poker_t == 'Jacks or Better':
        from engine.jacks_or_better import *
        combo_check = JacksOrBetter()
    else:
        exit(0)
    # Initialize player
    if game_t == 'Continue game':
        pass
    elif game_t == 'New game':
        dbase.set_creds(INITIAL_CREDS)
        dbase.update_creds()
    else:
        exit(0)
    # Constant reinit
    TABLE_HEIGHT = CELL_HEIGHT * len(poker_winnings)
    # Initialize library and create main window
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_MODE)
    pygame.display.set_caption('Video Poker - ' + CAPTION)
    # Try to initialize game font
    try:
        font = pygame.font.Font(os.path.join(DATA_DIR, FONT_NAME), FONT_SIZE)
        card_font = pygame.font.Font(os.path.join(DATA_DIR, FONT_NAME),
                                     FONT_SIZE * 2)
    except OSError as sys_error:
        logging.error('File not found: %s', os.path.join(DATA_DIR, FONT_NAME))
        font = pygame.font.SysFont('None', FONT_SIZE)
        card_font = pygame.font.SysFont('None', FONT_SIZE * 2)
    #
    # Global variables
    #
    coins = 0  # Number of inserted coins
    win_combo = ''
    table_surface = pygame.Surface(TABLE_SURFACE_SIZE)
    cards_surface = pygame.Surface(CARDS_SURFACE_SIZE)
    # Start game
    game()
