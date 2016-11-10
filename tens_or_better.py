# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Tens or Better engine
"""


# Card parameters
suit_list = ['S', 'C', 'H', 'D']
suits = {
    'S': '♠',  # Spades
    'C': '♣',  # Clubs
    'H': '♥',  # Hearts
    'D': '♦'   # Diamonds
}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Possible combinations
combination_names = ['Royal Flush', 'Straight Flush', 'Four of a Kind',
                     'Full House', 'Flush', 'Straight', 'Three of a Kind',
                     'Two Pairs', 'Tens or Better']
# Table of winnings
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


class ComboCheck(object):
    """
    Class that check for winning combination
    """

    def __init__(self, card_suits, card_ranks):
        """
        :param card_suits: card suits
        :type: list
        :param card_ranks: card ranks
        :type: list
        """

        self.card_suits = card_suits
        self.card_ranks = card_ranks

    def __call__(self):
        """
        Check for winning combination and return result if any

        :return: winning combination
        :type: string
        """

        combo_analytical_functions = {
            'Royal Flush':     self.royal_flush,
            'Straight Flush':  self.straight_flush,
            'Four of a Kind':  self.four_of_a_kind,
            'Full House':      self.full_house,
            'Flush':           self.flush,
            'Straight':        self.straight,
            'Three of a Kind': self.three_of_a_kind,
            'Two Pairs':       self.two_pairs,
            'Tens or Better':  self.tens_or_better
        }
        combo = ''

        for combination in combination_names:
            combo = combo_analytical_functions[combination]
            if combo:
                return combo
        return ''

    def royal_flush(self):
        """
        Check for Royal Flush combo

        :return: 'Royal Flush' if found
        :type: string
        """

        if self.card_suits in [['S', 'S', 'S', 'S', 'S'],
                               ['C', 'C', 'C', 'C', 'C'],
                               ['H', 'H', 'H', 'H', 'S'],
                               ['D', 'D', 'D', 'D', 'D']] \
                and self.card_ranks in ['10', 'J', 'Q', 'K', 'A']:
            return 'Royal Flush'
        else:
            return ''

    def straight_flush(self):
        """
        Check for Straight Flush

        :return: 'Straight Flush' if found
        :type: string
        """

        if self.card_suits in [['S', 'S', 'S', 'S', 'S'],
                               ['C', 'C', 'C', 'C', 'C'],
                               ['H', 'H', 'H', 'H', 'S'],
                               ['D', 'D', 'D', 'D', 'D']] \
            and self.card_ranks in [['2', '3', '4', '5', '6'],
                                    ['3', '4', '5', '6', '7'],
                                    ['4', '5', '6', '7', '8'],
                                    ['5', '6', '7', '8', '9'],
                                    ['6', '7', '8', '9', '10'],
                                    ['7', '8', '9', '10', 'J'],
                                    ['8', '9', '10', 'J', 'Q'],
                                    ['9', '10', 'J', 'Q', 'K']]:
            return 'Straight Flush'
        else:
            return ''

    def four_of_a_kind(self):
        """
        Check for Four of a Kind

        :return: 'Four of a Kind' if found
        :type: string
        """

        for rank in ranks:
            if self.card_ranks.count(rank) == 4:
                return 'Four of a Kind'
            else:
                return ''

    def full_house(self):
        """
        Check for Full House

        :return: 'Full House' if found
        :type: string
        """

        card_ranks_num = []
        for rank in ranks:
            card_ranks_num.append(self.card_ranks.count(rank))
        if [2, 3] in card_ranks_num:
            return 'Full House'
        else:
            return ''

    def flush(self):
        """
        Check for Flush

        :return: 'Flush' if found
        :type: string
        """

        if self.card_suits in [['S', 'S', 'S', 'S', 'S'],
                               ['C', 'C', 'C', 'C', 'C'],
                               ['H', 'H', 'H', 'H', 'S'],
                               ['D', 'D', 'D', 'D', 'D']]:
            return 'Flush'
        else:
            return ''

    def straight(self):
        """
        Check for Straight

        :return: 'Straight'
        :type: string
        """

        if self.card_ranks in [['2', '3', '4', '5', '6'],
                               ['3', '4', '5', '6', '7'],
                               ['4', '5', '6', '7', '8'],
                               ['5', '6', '7', '8', '9'],
                               ['6', '7', '8', '9', '10'],
                               ['7', '8', '9', '10', 'J'],
                               ['8', '9', '10', 'J', 'Q'],
                               ['9', '10', 'J', 'Q', 'K'],
                               ['10', 'J', 'Q', 'K', 'A']]:
            return 'Straight'
        else:
            return ''

    def three_of_a_kind(self):
        """
        Check for Three of a Kind

        :return: 'Three of a Kind' if found
        :type: string
        """

        for rank in ranks:
            if self.card_ranks.count(rank) == 3:
                return 'Three of a Kind'
            else:
                return ''

    def two_pairs(self):
        """
        Check for Two Pairs

        :return: 'Two Pairs' if found
        :type: string
        """

        card_ranks_num = []
        for rank in ranks:
            card_ranks_num.append(self.card_ranks.count(rank))
        if [2, 2] in card_ranks_num:
            return 'Two Pairs'
        else:
            return ''

    def tens_or_better(self):
        """
        Check for Tens or Better

        :return: 'Tens or Better' if found
        :type: string
        """

        for rank in ['10', 'J', 'Q', 'K', 'A']:
            if self.card_ranks.count(rank) == 2:
                return 'Tens or Better'
            else:
                return ''
