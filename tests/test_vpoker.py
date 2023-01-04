# Copyright (c) 2016-2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Unit tests for main module"""

import unittest
import ddt
from tests import tools

from vpoker import CARD_BACKGROUND_HEIGHT, SCREEN_WIDTH
from vpoker import Card, init_deck


@ddt.ddt
class TestCard(unittest.TestCase):
    """Card class testing"""

    @classmethod
    def setUpClass(cls):
        cls.sample_card = ('S', '10')

    def setUp(self):
        self.card = Card(1)

    def test_init_positive(self):
        """Positive test for constructor
        """
        self.assertEqual(1, self.card.centerx)
        self.assertEqual(int(CARD_BACKGROUND_HEIGHT/2), self.card.centery)
        self.assertEqual(False, self.card.active)
        self.assertEqual(True, self.card.back)
        self.assertEqual('', self.card.suit)
        self.assertEqual('', self.card.rank)
        self.assertEqual(False, self.card.held)

    @ddt.data(*tools.prepare_test_data(
        ('negative_int', -1, 0),
        ('zero', 0, 0),
        ('float', 10.5, 10),
        ('screen_width_minus_1', SCREEN_WIDTH - 1, SCREEN_WIDTH - 1),
        ('screen_width', SCREEN_WIDTH, SCREEN_WIDTH),
        ('screen_width_plus_1', SCREEN_WIDTH + 1, SCREEN_WIDTH),
        ('none', None, 0),
        ('wrong_type', '123', 0)
    ))
    @ddt.unpack
    def test_init_negative(self, x, expected):
        """Negative test for constructor: x = {0}, expected = {1}
        """
        card = Card(x)
        self.assertEqual(expected, card.centerx)

    def test_set_card_positive(self):
        """Positive test for set_card()
        """
        self.card.set_card(self.sample_card)
        self.assertEqual(self.sample_card[0], self.card.suit)
        self.assertEqual(self.sample_card[1], self.card.rank)
        self.assertEqual(False, self.card.back)

    @ddt.data(*tools.prepare_test_data(
        ('wrong_type', 1, TypeError),
        ('wrong_length', (1, 2, 3), ValueError),
        ('wrong_suit', ('A', '10'), KeyError),
        ('wrong_rank', ('S', '1'), KeyError),
        ('wrong_suit_rank', ('X', '11'), KeyError)
    ))
    @ddt.unpack
    def test_set_card_negative(self, crd, expected):
        """Negative test for set_card(): card - {0}, expected - {1}
        """
        self.assertRaises(expected, self.card.set_card, crd)

    def test_get_suit(self):
        """Test get_suit()
        """
        self.card.set_card(self.sample_card)
        self.assertEqual(self.sample_card[0], self.card.suit)

    def test_get_rank(self):
        """Test get_rank()
        """
        self.card.set_card(self.sample_card)
        self.assertEqual(self.sample_card[1], self.card.rank)

    def test_set_active_positive(self):
        """Positive test for set_active()
        """
        self.card.set_active(True)
        self.assertEqual(True, self.card.active)
        self.card.set_active()
        self.assertEqual(False, self.card.active)

    def test_set_active_negative(self):
        """Negative test for set_active()
        """
        self.assertRaises(TypeError, self.card.set_active, 3)

    def test_get_held(self):
        """Test for get_held()
        """
        self.card.held = False
        self.assertEqual(False, self.card.get_held())

    def test_set_held_positive(self):
        """Positive test for set_held()
        """
        self.card.set_held(True)
        self.assertEqual(True, self.card.held)
        self.card.set_held()
        self.assertEqual(False, self.card.held)

    def test_set_held_negative(self):
        """Negative test for set_held()
        """
        self.assertRaises(TypeError, self.card.set_held, 3)

    def test_set_back_positive(self):
        """Positive test for set_back()
        """
        self.card.set_back()
        self.assertEqual(True, self.card.back)
        self.card.set_back(False)
        self.assertEqual(False, self.card.back)

    def test_set_back_negative(self):
        """Negative test for set_back()
        """
        self.assertRaises(TypeError, self.card.set_back, 3)


class TestInitDeck(unittest.TestCase):
    """init_deck() testing"""

    @classmethod
    def setUpClass(cls):
        cls.standard_deck = (
            ('S', '2'),  ('C', '2'),  ('H', '2'),  ('D', '2'),
            ('S', '3'),  ('C', '3'),  ('H', '3'),  ('D', '3'),
            ('S', '4'),  ('C', '4'),  ('H', '4'),  ('D', '4'),
            ('S', '5'),  ('C', '5'),  ('H', '5'),  ('D', '5'),
            ('S', '6'),  ('C', '6'),  ('H', '6'),  ('D', '6'),
            ('S', '7'),  ('C', '7'),  ('H', '7'),  ('D', '7'),
            ('S', '8'),  ('C', '8'),  ('H', '8'),  ('D', '8'),
            ('S', '9'),  ('C', '9'),  ('H', '9'),  ('D', '9'),
            ('S', '10'), ('C', '10'), ('H', '10'), ('D', '10'),
            ('S', 'J'),  ('C', 'J'),  ('H', 'J'),  ('D', 'J'),
            ('S', 'Q'),  ('C', 'Q'),  ('H', 'Q'),  ('D', 'Q'),
            ('S', 'K'),  ('C', 'K'),  ('H', 'K'),  ('D', 'K'),
            ('S', 'A'),  ('C', 'A'),  ('H', 'A'),  ('D', 'A'),
        )

    def test_init_deck(self):
        """Check if standard test deck and generated deck are equal
        """
        self.assertEqual(len(self.standard_deck), len(init_deck()))
        self.assertEqual(set(self.standard_deck), set(init_deck()))


if __name__ == '__main__':
    unittest.main()
