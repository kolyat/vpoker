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
        my_suits += suit_list[random.randint(0, len(suit_list) - 1)]
    return my_suits


class TestComboCheck(unittest.TestCase):
    """Tests for class ComboCheck"""

    def test_two_pairs(self):
        """Tests for Two Pairs combo"""

        first_rank = ranks
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
                for i in range(5):
                    test_hand += raw_test_hand.pop(
                        random.randint(0, len(raw_test_hand)-1))
                # Perform positive test
                self.assertEqual(ComboCheck(generate_random_suits(),
                                            test_hand),
                                 'Two Pairs')
        # Perform negative test
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
