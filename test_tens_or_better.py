# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Unit tests for Tens or Better engine
"""

import unittest
import random
from tens_or_better import *


def generate_random_suits():
    """
    Generates random 5 suits

    :return: 5 random suits
    :type: list
    """

    my_suits = []
    random.seed(None)
    for i in range(5):
        my_suits += suit_list[random.randint(0, len(suit_list)-1)]
    return my_suits


def generate_random_ranks():
    """
    Generates random 5 ranks

    :return: 5 random ranks
    :type: list
    """

    my_ranks = []
    random.seed(None)
    for i in range(5):
        my_ranks += ranks[random.randint(0, len(ranks)-1)]
    return my_ranks


class TestComboCheck(unittest.TestCase):
    """Tests for class ComboCheck"""

    def setUp(self):
        self.ranks = tuple(ranks)

    def test_royal_flush(self):
        """Tests for Royal Flush combo"""

        # Perform positive tests
        self.assertEqual(ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                    ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(ComboCheck(['C', 'C', 'C', 'C', 'C'],
                                    ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(ComboCheck(['H', 'H', 'H', 'H', 'H'],
                                    ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(ComboCheck(['D', 'D', 'D', 'D', 'D'],
                                    ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        # Negative tests
        self.assertEqual(ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                    ['9', '10', 'J', 'Q', 'K']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['10', 'J', 'Q', 'K', 'A']), '')

    def test_straight_flush(self):
        """Tests for Straight Flush combo"""

        for i in range(0, len(ranks) - 5, 1):
            # Make an unshuffled hand with combo
            raw_test_hand = []
            raw_test_hand += ranks[i:i+4]
            # Shuffle hand
            random.seed(None)
            test_hand = []
            while raw_test_hand:
                test_hand += raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1))
            # Perform positive test
            self.assertEqual(ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                        test_hand), 'Straight Flush')
            self.assertEqual(ComboCheck(['C', 'C', 'C', 'C', 'C'],
                                        test_hand), 'Straight Flush')
            self.assertEqual(ComboCheck(['H', 'H', 'H', 'H', 'H'],
                                        test_hand), 'Straight Flush')
            self.assertEqual(ComboCheck(['D', 'D', 'D', 'D', 'D'],
                                        test_hand), 'Straight Flush')
        # Negative tests
        self.assertEqual(ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                    ['10', 'J', 'Q', 'K', 'A']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', '3', '4', '5', '6']), '')
        self.assertEqual(ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                    ['A', '2', '3', '4', '5']), '')

    def test_four_of_a_kind(self):
        """Tests for Four of a Kind combo"""

        for rank in ranks:
            # Select second rank
            random.seed(None)
            while True:
                second_rank = ranks[random.randint(0, len(ranks)-1)]
                if second_rank != rank:
                    break
            # Create unshuffled hand
            raw_test_hand = []
            raw_test_hand += rank*4 + second_rank
            # Shuffle hand
            test_hand = []
            while raw_test_hand:
                test_hand += raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1))
            # Perform positive test
            self.assertEqual(ComboCheck(generate_random_suits(),
                                        test_hand),
                             'Four of a Kind')
        # Negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', 'A', 'A', 'K', 'Q']), '')

    def test_full_house(self):
        """Tests for Full House combo"""

        first_rank = list(ranks)
        while len(first_rank) > 1:
            # Get first rank
            first_card = first_rank.pop(0)
            second_rank = first_rank
            while len(second_rank) > 0:
                # Get second rank
                second_card = second_rank.pop(0)
                # Create unshuffled hand
                random.seed(None)
                raw_test_hand1 = []
                raw_test_hand2 = []
                raw_test_hand1 += first_card*2 + second_card*3
                raw_test_hand2 += first_card*3 + second_card*2
                # Shuffle hand
                test_hand1 = []
                test_hand2 = []
                while raw_test_hand1 and raw_test_hand2:
                    test_hand1 += raw_test_hand1.pop(
                        random.randint(0, len(raw_test_hand1) - 1))
                    test_hand2 += raw_test_hand2.pop(
                        random.randint(0, len(raw_test_hand2) - 1))
                # Perform positive test
                self.assertEqual(ComboCheck(generate_random_suits(),
                                            test_hand1),
                                 'Full House')
                self.assertEqual(ComboCheck(generate_random_suits(),
                                            test_hand2),
                                 'Full House')
        # Perform negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', '2', '3', '3', 'A']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', 'A', 'A', '2', '3']), '')

    def test_flush(self):
        """Tests for Flush combo"""

        # Positive tests
        for suit in suit_list:
            self.assertEqual(ComboCheck(suit*5, generate_random_ranks()),
                             'Flush')
        # Negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    generate_random_ranks()), '')

    def test_straight(self):
        """Tests for Straight combo"""

        for i in range(0, len(ranks)-4, 1):
            # Make an unshuffled hand with combo
            raw_test_hand = []
            raw_test_hand += ranks[i:i+4]
            # Shuffle hand
            random.seed(None)
            test_hand = []
            while raw_test_hand:
                test_hand += raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1))
            # Perform positive test
            self.assertEqual(ComboCheck(generate_random_suits(),
                             test_hand), 'Straight')
        # Perform negative test
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', '2', '3', '4', '5']), '')

    def test_three_of_a_kind(self):
        """Tests for Three of a Kind combo"""

        for rank in ranks:
            # Prepare additional rank list to fill hand with two other ranks
            other_ranks = list(ranks)
            other_ranks.remove(rank)
            # Choose two other ranks that must differ from each other
            random.seed(None)
            another_rank_1 = other_ranks.pop(
                random.randint(0, len(other_ranks)-1))
            another_rank_2 = other_ranks.pop(
                random.randint(0, len(other_ranks)-1))
            # Make a hand
            raw_test_hand = []
            raw_test_hand += rank*3 + another_rank_1 + another_rank_2
            # Shuffle hand
            test_hand = []
            while raw_test_hand:
                test_hand += raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand)-1))
            # Perform positive test
            self.assertEqual(ComboCheck(generate_random_suits(),
                                        test_hand), 'Three of a Kind')
        # Perform negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', '3', '4', '5', '6']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', 'A', '4', '5', '6']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['K', 'K', '10', '10', 'J']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', 'Q', 'Q', 'J', 'J']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['10', '10', '10', '10', 'A']), '')

    def test_two_pairs(self):
        """Tests for Two Pairs combo"""

        first_rank = list(ranks)
        while len(first_rank) > 1:
            # Get first rank to make a pair
            first_card = first_rank.pop(0)
            second_rank = first_rank
            while len(second_rank) > 0:
                # Get second rank to make a pair
                second_card = second_rank.pop(0)
                # Create list of available ranks for last card
                other_ranks = ranks
                other_ranks.remove(first_card)
                other_ranks.remove(second_card)
                # Create unshuffled hand
                random.seed(None)
                raw_test_hand = []
                raw_test_hand += first_card*2 + second_card*2 + \
                    other_ranks[random.randint(0, len(other_ranks)-1)]
                # Shuffle hand
                test_hand = []
                while raw_test_hand:
                    test_hand += raw_test_hand.pop(
                        random.randint(0, len(raw_test_hand)-1))
                # Perform positive test
                self.assertEqual(ComboCheck(generate_random_suits(),
                                            test_hand),
                                 'Two Pairs')
        # Perform negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', '3', '4', '5', '6']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', 'A', '4', '5', '6']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['3', '3', '3', '10', 'J']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['3', '3', '3', '2', '2']), '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['4', '4', '4', '4', 'A']), '')

    def test_tens_or_better(self):
        """Tests for Tens or Better combo"""

        # Positive tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['A', '2', 'A', '3', '4']),
                         'Tens or Better')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['K', '2', '3', 'K', '4']),
                         'Tens or Better')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', '2', '3', '4', 'Q']),
                         'Tens or Better')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', 'J', '3', '4', 'J']),
                         'Tens or Better')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['2', '3', '10', '4', '10']),
                         'Tens or Better')
        # Negative tests
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['9', '9', 'Q', 'K', 'A']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', '8', '8', 'K', 'A']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', 'K', '7', '7', 'A']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', 'K', 'A', '6', '6']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', '5', 'K', '5', 'A']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['4', 'Q', 'K', 'A', '4']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['3', 'Q', 'K', '3', 'A']),
                         '')
        self.assertEqual(ComboCheck(generate_random_suits(),
                                    ['Q', '2', 'K', 'A', '2']),
                         '')


if __name__ == '__main__':
    unittest.main()
