# Copyright (c) 2016-2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Base engine for various poker types"""

# Card parameters
suits = {
    'S': '♠',  # Spades
    'C': '♣',  # Clubs
    'H': '♥',  # Hearts
    'D': '♦'   # Diamonds
}
suit_list = suits.keys()
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')


class BaseEngine:
    """Base class for game engines
    """
    suits_flush = [['S']*5, ['C']*5, ['H']*5, ['D']*5]

    def __call__(self, card_suits, card_ranks):
        """Entry point with necessary checks, should be overridden with
        super().__call__(card_suits, card_ranks)

        :param card_suits: card suits
        :type card_suits: list
        :param card_ranks: card ranks
        :type card_ranks: list

        :raise: TypeError: card_suit/card_rank is not a list
        :raise: ValueError: number of elements in a list is not equal to 5
        :raise: KeyError: current suit/rank does not exist
        """
        # Check for correct type
        if type(card_suits) != list:
            raise TypeError('Card suits must be a list')
        if type(card_ranks) != list:
            raise TypeError('Card ranks must be a list')
        # Check for list length
        if len(card_suits) != 5:
            raise ValueError('Number of elements in a list of card suits must'
                             'be equal to 5')
        if len(card_ranks) != 5:
            raise ValueError('Number of elements in a list of card ranks must'
                             'be equal to 5')
        # Check values in list
        for e in card_suits:
            if e not in suit_list:
                raise KeyError('Unknown card suit: ', e)
        for e in card_ranks:
            if e not in ranks:
                raise KeyError('Unknown card rank: ', e)


class RankOrBetter(BaseEngine):
    """Abstract class that checks for winning combination in such poker type as
    'any rank or better' (e.g., 'Tens or Better')
    Method rank_or_better() is abstract and should be reimplemented
    """
    ranks_straight = [set(ranks[i:i+5]) for i in range(9)]

    def __init__(self):
        self.analytical_sequence = (
            self.royal_flush,
            self.straight_flush,
            self.four_of_a_kind,
            self.full_house,
            self.flush,
            self.straight,
            self.three_of_a_kind,
            self.two_pairs,
            self.rank_or_better
        )

    def __call__(self, card_suits, card_ranks):
        """Check for winning combination and return result if any

        :return: winning combination
        :type: str
        """
        super().__call__(card_suits, card_ranks)
        self.card_suits = card_suits
        self.card_ranks = card_ranks
        for fun in self.analytical_sequence:
            result = fun()
            if result:
                return result
        return ''

    def royal_flush(self):
        """Check for Royal Flush

        :return: 'Royal Flush'
        :type: str
        """
        if self.card_suits in self.suits_flush \
                and set(self.card_ranks) == {'10', 'J', 'Q', 'K', 'A'}:
            return 'Royal Flush'
        else:
            return ''

    def straight_flush(self):
        """Check for Straight Flush

        :return: 'Straight Flush'
        :type: str
        """
        if self.card_suits in self.suits_flush \
                and set(self.card_ranks) in self.ranks_straight:
            return 'Straight Flush'
        else:
            return ''

    def four_of_a_kind(self):
        """Check for Four of a Kind

        :return: 'Four of a Kind'
        :type: str
        """
        for rank in ranks:
            if self.card_ranks.count(rank) == 4:
                return 'Four of a Kind'
        return ''

    def full_house(self):
        """Check for Full House

        :return: 'Full House'
        :type: str
        """
        card_ranks_num = []
        for rank in ranks:
            card_ranks_num.append(self.card_ranks.count(rank))
        if {2, 3}.issubset(set(card_ranks_num)):
            return 'Full House'
        else:
            return ''

    def flush(self):
        """Check for Flush

        :return: 'Flush'
        :type: str
        """
        if self.card_suits in self.suits_flush:
            return 'Flush'
        else:
            return ''

    def straight(self):
        """Check for Straight

        :return: 'Straight'
        :type: str
        """
        if set(self.card_ranks) in self.ranks_straight:
            return 'Straight'
        else:
            return ''

    def three_of_a_kind(self):
        """Check for Three of a Kind

        :return: 'Three of a Kind'
        :type: str
        """
        for rank in ranks:
            if self.card_ranks.count(rank) == 3:
                return 'Three of a Kind'
        return ''

    def two_pairs(self):
        """Check for Two Pairs

        :return: 'Two Pairs'
        :type: str
        """
        card_ranks_num = []
        for rank in ranks:
            card_ranks_num.append(self.card_ranks.count(rank))
        card_ranks_num.sort()
        if card_ranks_num[-1] == 2 and card_ranks_num[-2] == 2:
            return 'Two Pairs'
        else:
            return ''

    def rank_or_better(self):
        """This method should be reimplemented and must return name of winning
        combo for pair of cards with the same rank
        """
        raise NotImplementedError('Method should be implemented')
