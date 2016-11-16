# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Unit tests for main module
"""


import unittest

from vpoker import CARD_BACKGROUND_HEIGHT
from vpoker import SCREEN_WIDTH

from vpoker import Card


class TestCard(unittest.TestCase):
    """Tests for Card class"""

    def test_init(self):
        """Tests for main class constructor"""

        # Positive test
        card = Card(1)
        self.assertEqual(card.centerx, 1)
        self.assertEqual(card.centery, int(CARD_BACKGROUND_HEIGHT/2))
        self.assertEqual(card.active, False)
        self.assertEqual(card.back, True)
        self.assertEqual(card.suit, '')
        self.assertEqual(card.rank, '')
        self.assertEqual(card.held, False)

        # Negative scenarios
        card = Card(-1)
        self.assertEqual(card.centerx, 0)
        card = Card(0)
        self.assertEqual(card.centerx, 0)
        card = Card(10.5)
        self.assertEqual(card.centerx, int(10.5))
        card = Card(SCREEN_WIDTH-1)
        self.assertEqual(card.centerx, SCREEN_WIDTH-1)
        card = Card(SCREEN_WIDTH)
        self.assertEqual(card.centerx, SCREEN_WIDTH)
        card = Card(SCREEN_WIDTH+1)
        self.assertEqual(card.centerx, SCREEN_WIDTH)
        card = Card()
        self.assertEqual(card.centerx, 0)
        card = Card('123')
        self.assertEqual(card.centerx, 0)

    def test_set_card(self):
        """Test for set_card() method"""

        card = Card()
        # Positive test
        card.set_card(('S', '10'))
        self.assertEqual(card.suit, 'S')
        self.assertEqual(card.rank, '10')
        self.assertEqual(card.back, False)

        # Negative tests
        self.assertRaises(TypeError, card.set_card, {'2', '3'})
        self.assertRaises(ValueError, card.set_card, ('S', '1', '0'))
        self.assertRaises(KeyError, card.set_card, ('A', '10'))
        self.assertRaises(KeyError, card.set_card, ('S', '1'))
        self.assertRaises(KeyError, card.set_card, ('X', 'V'))

if __name__ == '__main__':
    unittest.main()
