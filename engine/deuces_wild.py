# Copyright (c) 2016-2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Deuces Wild engine"""

import collections
from .base import suits, suit_list, ranks, BaseEngine


CAPTION = 'Deuces Wild'
BACKGROUND_COLOR = (50, 0, 10)

# Table of winnings
poker_winnings = collections.OrderedDict((
    ('Natural Royal Flush', [250, 500, 750, 1000, 4000]),
    ('Four Deuces',         [200, 400, 600, 800,  1000]),
    ('Deuces Royal Flush',  [25,  50,  75,  100,  125]),
    ('Five of a Kind',      [16,  32,  48,  64,   80]),
    ('Straight Flush',      [13,  26,  39,  52,   65]),
    ('Four of a Kind',      [4,   8,   12,  16,   20]),
    ('Full House',          [3,   6,   9,   12,   15]),
    ('Flush',               [2,   4,   6,   8,    10]),
    ('Straight',            [2,   4,   6,   8,    10]),
    ('Three of a Kind',     [1,   2,   3,   4,    5])
))
combination_names = poker_winnings.keys()


class DeucesWild(BaseEngine):
    """Deuces Wild game engine
    """
    ranks_straight = [set(ranks[i:i+5]) for i in range(1, 9)]

    def __init__(self):
        self.analytical_sequence = (
            self.natural_royal_flush,
            self.four_deuces,
            self.deuces_royal_flush,
            self.five_of_a_kind,
            self.straight_flush,
            self.four_of_a_kind,
            self.full_house,
            self.flush,
            self.straight,
            self.three_of_a_kind
        )

    def __call__(self, card_suits, card_ranks):
        """Check for winning combination and return result if any, deuces are
        counted and removed from hand

        :return: winning combination
        :type: str
        """
        super().__call__(card_suits, card_ranks)
        self.deuces = 0
        self.card_suits = []
        self.card_ranks = []
        for i, rank in enumerate(card_ranks):
            if rank != '2':
                self.card_suits.append(card_suits[i])
                self.card_ranks.append(rank)
            else:
                self.deuces += 1
        for fun in self.analytical_sequence:
            result = fun()
            if result:
                return result
        return ''

    def natural_royal_flush(self):
        """Check for Natural Royal Flush

        :return: 'Natural Royal Flush'
        :type: str
        """
        if self.deuces == 0 and self.card_suits in self.suits_flush \
                and set(self.card_ranks) == {'10', 'J', 'Q', 'K', 'A'}:
            return 'Natural Royal Flush'
        else:
            return ''

    def four_deuces(self):
        """Check for Four Deuces

        :return: 'Four Deuces'
        :type: str
        """
        if self.deuces == 4:
            return 'Four Deuces'
        else:
            return ''

    def deuces_royal_flush(self):
        """Check for Deuces Royal Flush

        :return: 'Deuces Royal Flush'
        :type: str
        """
        for suit in self.suits_flush:
            if self.deuces > 0 and set(self.card_suits) == set(suit) \
                    and set(self.card_ranks).issubset(
                        {'10', 'J', 'Q', 'K', 'A'}):
                return 'Deuces Royal Flush'
        return ''

    def five_of_a_kind(self):
        """Check for Five of a Kind

        :return: 'Five of a Kind'
        :type: str
        """
        for rank in ranks:
            if self.card_ranks.count(rank) + self.deuces == 5:
                return 'Five of a Kind'
        return ''

    def straight_flush(self):
        """Check for Straight Flush

        :return: 'Straight Flush'
        :type: str
        """
        ranks_straight = \
            self.ranks_straight[:len(self.ranks_straight)-self.deuces-1]
        for suit in self.suits_flush:
            for rank in ranks_straight:
                if set(self.card_suits) == set(suit) \
                        and set(self.card_ranks).issubset(rank):
                    return 'Straight Flush'
        return ''

    def four_of_a_kind(self):
        """Check for Four of a Kind

        :return: 'Four of a Kind'
        :type: str
        """
        for rank in ranks:
            if self.card_ranks.count(rank) + self.deuces == 4:
                return 'Four of a Kind'
        return ''

    def full_house(self):
        """Check for Full House

        :return: 'Full House'
        :type: str
        """
        card_ranks_num = [self.card_ranks.count(rank) for rank in ranks]
        card_ranks_set = set(card_ranks_num) - {0}
        for s, d in [({1, 2}, 2), ({2, 2}, 1), ({2, 3}, 0)]:
            if card_ranks_set == s and self.deuces == d:
                return 'Full House'
        return ''

    def flush(self):
        """Check for Flush

        :return: 'Flush'
        :type: str
        """
        for suit in self.suits_flush:
            if set(self.card_suits) == set(suit):
                return 'Flush'
        return ''

    def straight(self):
        """Check for Straight

        :return: 'Straight'
        :type: str
        """
        for rank in self.ranks_straight:
            if (set(self.card_ranks).issubset(rank)
                and len(self.card_ranks) == len(set(self.card_ranks))
                and self.deuces > 0) or \
                    (set(self.card_ranks) in self.ranks_straight
                     and self.deuces == 0):
                return 'Straight'
        return ''

    def three_of_a_kind(self):
        """Check for Three of a Kind

        :return: 'Three of a Kind'
        :type: str
        """
        for rank in ranks:
            if self.card_ranks.count(rank) + self.deuces == 3:
                return 'Three of a Kind'
        return ''
