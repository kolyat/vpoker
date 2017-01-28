# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
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

    my_suits = list()
    random.seed(None)
    for i in range(5):
        my_suits.append(suit_list[random.randint(0, len(suit_list)-1)])
    return my_suits


def generate_random_ranks():
    """
    Generates random 5 ranks

    :return: 5 random ranks
    :type: list
    """

    my_ranks = list()
    random.seed(None)
    for i in range(5):
        my_ranks.append(ranks[random.randint(0, len(ranks)-1)])
    return my_ranks


def generate_different_suits():
    """
    Create hand with 4 suits from list and 1 random

    :return: 5 suits
    :type: liat
    """

    my_suits = list()
    for s in suit_list:
        my_suits.append(s)
    random.seed(None)
    my_suits.append(suit_list[random.randint(0, len(suit_list)-1)])
    return my_suits


def generate_different_ranks():
    """
    Create hand with 'even' ranks

    :return: 5 ranks
    :type: list
    """

    return ['2', '4', '6', '8', '10']


class TestComboCheck(unittest.TestCase):
    """Tests for class ComboCheck"""

    def setUp(self):
        self.ranks = ranks
        self.ComboCheck = ComboCheck()

    def tearDown(self):
        del self.ranks
        del self.ComboCheck

    def test_royal_flush(self):
        """Tests for Royal Flush combo"""

        self.assertEqual(self.ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                         ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(self.ComboCheck(['C', 'C', 'C', 'C', 'C'],
                                         ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(self.ComboCheck(['H', 'H', 'H', 'H', 'H'],
                                         ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')
        self.assertEqual(self.ComboCheck(['D', 'D', 'D', 'D', 'D'],
                                         ['Q', 'K', 'A', 'J', '10']),
                         'Royal Flush')

    def test_straight_flush(self):
        """Tests for Straight Flush combo"""

        for i in range(0, len(self.ranks) - 5, 1):
            # Make an unshuffled hand with combo
            raw_test_hand = []
            raw_test_hand += self.ranks[i:i+5]
            # Shuffle hand
            random.seed(None)
            test_hand = []
            while raw_test_hand:
                test_hand.append(raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1)))
            # Perform tests
            self.assertEqual(self.ComboCheck(['S', 'S', 'S', 'S', 'S'],
                                             test_hand), 'Straight Flush')
            self.assertEqual(self.ComboCheck(['C', 'C', 'C', 'C', 'C'],
                                             test_hand), 'Straight Flush')
            self.assertEqual(self.ComboCheck(['H', 'H', 'H', 'H', 'H'],
                                             test_hand), 'Straight Flush')
            self.assertEqual(self.ComboCheck(['D', 'D', 'D', 'D', 'D'],
                                             test_hand), 'Straight Flush')

    def test_four_of_a_kind(self):
        """Tests for Four of a Kind combo"""

        for rank in self.ranks:
            # Select second rank
            random.seed(None)
            second_rank = []
            while True:
                second_rank = self.ranks[random.randint(0, len(self.ranks)-1)]
                if second_rank != rank:
                    break
            # Create unshuffled hand
            raw_test_hand = list()
            for i in range(4):
                raw_test_hand.append(rank)
            raw_test_hand.append(second_rank)
            # Shuffle hand
            test_hand = []
            while raw_test_hand:
                test_hand.append(raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1)))
            # Perform test
            self.assertEqual(self.ComboCheck(generate_different_suits(),
                                             test_hand),
                             'Four of a Kind')

    def test_full_house(self):
        """Tests for Full House combo"""

        first_rank = list(self.ranks)
        while len(first_rank) > 1:
            # Get first rank
            first_card = first_rank.pop(0)
            second_rank = first_rank
            while len(second_rank) > 0:
                # Get second rank
                second_card = second_rank.pop(0)
                # Create unshuffled hand
                random.seed(None)
                raw_test_hand1 = list()
                raw_test_hand2 = list()
                for i in range(3):
                    raw_test_hand1.append(first_card)
                    raw_test_hand2.append(second_card)
                for i in range(2):
                    raw_test_hand1.append(second_card)
                    raw_test_hand2.append(first_card)
                # Shuffle hand
                test_hand1 = list()
                test_hand2 = list()
                while raw_test_hand1 and raw_test_hand2:
                    test_hand1.append(raw_test_hand1.pop(
                        random.randint(0, len(raw_test_hand1) - 1)))
                    test_hand2.append(raw_test_hand2.pop(
                        random.randint(0, len(raw_test_hand2) - 1)))
                # Perform tests
                self.assertEqual(self.ComboCheck(generate_different_suits(),
                                                 test_hand1),
                                 'Full House')
                self.assertEqual(self.ComboCheck(generate_different_suits(),
                                                 test_hand2),
                                 'Full House')

    def test_flush(self):
        """Tests for Flush combo"""

        for suit in suit_list:
            my_suit = list()
            for i in range(5):
                my_suit.append(suit)
            self.assertEqual(self.ComboCheck(
                my_suit, generate_different_ranks()), 'Flush')

    def test_straight(self):
        """Tests for Straight combo"""

        for i in range(0, len(self.ranks)-4, 1):
            # Make an unshuffled hand with combo
            raw_test_hand = list(self.ranks[i:i+5])
            # Shuffle hand
            random.seed(None)
            test_hand = []
            while raw_test_hand:
                test_hand.append(raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand) - 1)))
            # Perform test
            self.assertEqual(self.ComboCheck(generate_different_suits(),
                                             test_hand), 'Straight')

    def test_three_of_a_kind(self):
        """Tests for Three of a Kind combo"""

        for rank in self.ranks:
            # Prepare additional rank list to fill hand with two other ranks
            other_ranks = list(self.ranks)
            other_ranks.remove(rank)
            # Choose two other ranks that must differ from each other
            random.seed(None)
            another_rank_1 = other_ranks.pop(
                random.randint(0, len(other_ranks)-1))
            another_rank_2 = other_ranks.pop(
                random.randint(0, len(other_ranks)-1))
            # Make a hand
            raw_test_hand = list()
            for i in range(3):
                raw_test_hand.append(rank)
            raw_test_hand.append(another_rank_1)
            raw_test_hand.append(another_rank_2)
            # Shuffle hand
            test_hand = list()
            while raw_test_hand:
                test_hand.append(raw_test_hand.pop(
                    random.randint(0, len(raw_test_hand)-1)))
            # Perform test
            self.assertEqual(self.ComboCheck(generate_different_suits(),
                                             test_hand), 'Three of a Kind')

    def test_two_pairs(self):
        """Tests for Two Pairs combo"""

        first_rank = list(self.ranks)
        while len(first_rank) > 1:
            # Get first rank to make a pair
            first_card = first_rank.pop(0)
            second_rank = first_rank
            while len(second_rank) > 0:
                # Get second rank to make a pair
                second_card = second_rank.pop(0)
                # Create list of available ranks for last card
                other_ranks = list(self.ranks)
                other_ranks.remove(first_card)
                other_ranks.remove(second_card)
                # Create unshuffled hand
                random.seed(None)
                raw_test_hand = list()
                for i in range(2):
                    raw_test_hand.append(first_card)
                    raw_test_hand.append(second_card)
                raw_test_hand.append(
                    other_ranks[random.randint(0, len(other_ranks)-1)])
                # Shuffle hand
                test_hand = list()
                while raw_test_hand:
                    test_hand.append(raw_test_hand.pop(
                        random.randint(0, len(raw_test_hand)-1)))
                # Perform test
                self.assertEqual(self.ComboCheck(generate_different_suits(),
                                                 test_hand),
                                 'Two Pairs')

    def test_tens_or_better(self):
        """Tests for Tens or Better combo"""

        # Positive tests
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['A', '2', 'A', '3', '4']),
                         'Tens or Better')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['K', '2', '3', 'K', '4']),
                         'Tens or Better')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', '2', '3', '4', 'Q']),
                         'Tens or Better')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['2', 'J', '3', '4', 'J']),
                         'Tens or Better')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['2', '3', '10', '4', '10']),
                         'Tens or Better')
        # Negative tests
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['9', '9', 'Q', 'K', 'A']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', '8', '8', 'K', 'A']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', 'K', '7', '7', 'A']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', 'K', 'A', '6', '6']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', '5', 'K', '5', 'A']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['4', 'Q', 'K', 'A', '4']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['3', 'Q', 'K', '3', 'A']),
                         '')
        self.assertEqual(self.ComboCheck(generate_different_suits(),
                                         ['Q', '2', 'K', 'A', '2']),
                         '')

    def test_negative(self):
        """Negative scenarios"""

        # Invalid type
        self.assertRaises(TypeError, self.ComboCheck,
                          3, generate_random_ranks())
        self.assertRaises(TypeError, self.ComboCheck,
                          generate_random_suits(), 3)
        self.assertRaises(TypeError, self.ComboCheck,
                          3, 3)

        # Invalid length of list
        self.assertRaises(ValueError, self.ComboCheck,
                          [1, 2, 3, 4, 5, 6], generate_random_ranks())
        self.assertRaises(ValueError, self.ComboCheck,
                          generate_random_suits(), [1, 2, 3, 4, 5, 6])
        self.assertRaises(ValueError, self.ComboCheck,
                          [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6])

        # Incorrect values
        self.assertRaises(KeyError, self.ComboCheck,
                          ['A', 'B', 'C', 'D', 'E'], generate_random_ranks())
        self.assertRaises(KeyError, self.ComboCheck,
                          generate_random_suits(), ['1', '11', 'C', 'B', 'X'])
        self.assertRaises(KeyError, self.ComboCheck,
                          ['A', 'B', 'C', 'D', 'E'], ['1', '2', 'C', 'B', 'X'])

if __name__ == '__main__':
    unittest.main()
