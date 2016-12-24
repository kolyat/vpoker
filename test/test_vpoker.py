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
from vpoker import init_deck


class TestCard(unittest.TestCase):
    """Tests for Card class"""

    def setUp(self):
        self.sample_card = ('S', '10')

    def tearDown(self):
        del self.sample_card

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
        card.set_card(self.sample_card)
        self.assertEqual(card.suit, self.sample_card[0])
        self.assertEqual(card.rank, self.sample_card[1])
        self.assertEqual(card.back, False)

        # Negative tests
        self.assertRaises(TypeError, card.set_card, {'2', '3'})
        self.assertRaises(ValueError, card.set_card, ('S', '1', '0'))
        self.assertRaises(KeyError, card.set_card, ('A', '10'))
        self.assertRaises(KeyError, card.set_card, ('S', '1'))
        self.assertRaises(KeyError, card.set_card, ('X', 'V'))

    def test_get_suit(self):
        """Test for get_suit() method"""

        card = Card()
        card.set_card(self.sample_card)
        self.assertEqual(card.get_suit(), self.sample_card[0])

    def test_get_rank(self):
        """Test for get_rank() method"""

        card = Card()
        card.set_card(self.sample_card)
        self.assertEqual(card.get_rank(), self.sample_card[1])

    def test_set_active(self):
        """Test for set_active() method"""

        card = Card()
        # Positive tests
        card.set_active(True)
        self.assertEqual(card.active, True)
        card.set_active()
        self.assertEqual(card.active, False)

        # Negative test
        self.assertRaises(TypeError, card.set_active, 3)

    def test_get_held(self):
        """Test for get_held() method"""

        card = Card()
        self.assertEqual(card.get_held(), False)

    def test_set_held(self):
        """Test for set_held() method"""

        card = Card()
        # Positive tests
        card.set_held(True)
        self.assertEqual(card.held, True)
        card.set_held()
        self.assertEqual(card.held, False)

        # Negative test
        self.assertRaises(TypeError, card.set_held, 3)

    def test_set_back(self):
        """Test for set_back() method"""

        card = Card()
        # Positive tests
        card.set_back()
        self.assertEqual(card.back, True)
        card.set_back(False)
        self.assertEqual(card.back, False)

        # Negative test
        self.assertRaises(TypeError, card.set_back, 3)


class TestInitDeck(unittest.TestCase):
    """Tests for init_deck() function"""

    def setUp(self):
        self.standard_deck = {
            ('S', '2'), ('C', '2'), ('H', '2'), ('D', '2'),
            ('S', '3'), ('C', '3'), ('H', '3'), ('D', '3'),
            ('S', '4'), ('C', '4'), ('H', '4'), ('D', '4'),
            ('S', '5'), ('C', '5'), ('H', '5'), ('D', '5'),
            ('S', '6'), ('C', '6'), ('H', '6'), ('D', '6'),
            ('S', '7'), ('C', '7'), ('H', '7'), ('D', '7'),
            ('S', '8'), ('C', '8'), ('H', '8'), ('D', '8'),
            ('S', '9'), ('C', '9'), ('H', '9'), ('D', '9'),
            ('S', '10'), ('C', '10'), ('H', '10'), ('D', '10'),
            ('S', 'J'), ('C', 'J'), ('H', 'J'), ('D', 'J'),
            ('S', 'Q'), ('C', 'Q'), ('H', 'Q'), ('D', 'Q'),
            ('S', 'K'), ('C', 'K'), ('H', 'K'), ('D', 'K'),
            ('S', 'A'), ('C', 'A'), ('H', 'A'), ('D', 'A'),
        }

    def tearDown(self):
        del self.standard_deck

    def test_init_deck(self):
        """Check if standard test deck and generated deck are equal"""

        self.assertEqual(set(init_deck()), self.standard_deck)

if __name__ == '__main__':
    unittest.main()
