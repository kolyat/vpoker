# Copyright (c) 2016-2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Unit tests for game engines:
- Tens or Better
- Jacks or Better
"""

import random
import itertools
import unittest
import ddt
from tests import tools

from engine.base import suit_list, ranks, RankOrBetter
from engine.tens_or_better import TensOrBetter
from engine.jacks_or_better import JacksOrBetter


class RankOrBetterUnderTesting(RankOrBetter):
    """For testing purposes with empty rank_or_better() method"""
    def rank_or_better(self):
        pass


def data_straight_flush():
    """Prepare data for Straight Flush
    """
    _test_ranks = [tools.shuffle(ranks[i:i+5]) for i in range(len(ranks)-5)]
    return [('{}_{}'.format(s*5, ''.join(r)), [s]*5, r)
            for s in suit_list for r in _test_ranks]


def data_four_of_a_kind():
    """Prepare data for Four of a Kind
    """
    random.seed(None)
    _test_data = list()
    for rank in ranks:
        second_rank = rank
        while second_rank == rank:
            second_rank = ranks[random.randint(0, len(ranks)-1)]
        _test_ranks = tools.shuffle([rank]*4 + [second_rank])
        _test_suits = tools.generate_random_suits()
        _test_data.append(
            ('{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
             _test_suits, _test_ranks)
        )
    return _test_data


def data_full_house():
    """Prepare data for Full House
    """
    pairs, triples = list(), list()
    for r in ranks:
        pairs.append([r]*2)
        triples.append([r]*3)
    raw = [(i[0]+i[1]) for i in itertools.product(pairs, triples)]
    raw = filter(lambda x: len(set(x)) > 1, raw)
    raw = [(tools.generate_different_suits(), r)
           for r in map(tools.shuffle, raw)]
    return [('{}_{}'.format(''.join(s), ''.join(r)), s, r) for s, r in raw]


def data_straight():
    """Prepare data for Straight
    """
    _test_data = [
        (tools.generate_different_suits(), tools.shuffle(ranks[i:i+5]))
        for i in range(len(ranks)-4)
    ]
    return [('{}_{}'.format(''.join(s), ''.join(r)), s, r)
            for s, r in _test_data]


def data_three_of_a_kind():
    """Prepare data for Three of a Kind
    """
    random.seed(None)
    _test_data = list()
    for rank in ranks:
        _test_ranks = [rank]*3
        while len(_test_ranks) < 5:
            another_rank = ranks[random.randint(0, len(ranks)-1)]
            if another_rank not in _test_ranks:
                _test_ranks.append(another_rank)
        _test_ranks = tools.shuffle(_test_ranks)
        _test_suits = tools.generate_different_suits()
        _test_data.append(
            ('{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
             _test_suits, _test_ranks)
        )
    return _test_data


def data_two_pairs():
    """Prepare data for Two Pairs
    """
    pairs = [[r]*2 for r in ranks]
    raw = [i[0]+i[1] for i in itertools.product(pairs, pairs)]
    raw = list(filter(lambda x: len(set(x)) > 1, raw))
    for i in range(len(raw)):
        while len(raw[i]) < 5:
            r = ranks[random.randint(0, len(ranks)-1)]
            if r not in raw[i]:
                raw[i].append(r)
    raw = [(tools.generate_different_suits(), r)
           for r in map(tools.shuffle, raw)]
    return [('{}_{}'.format(''.join(s), ''.join(r)), s, r) for s, r in raw]


@ddt.ddt
class TestRankOrBetter(unittest.TestCase):
    """Tests for RankOrBetter"""

    @classmethod
    def setUpClass(cls):
        cls.rank_or_better = RankOrBetterUnderTesting()

    def test_royal_flush(self):
        """Test Royal Flush
        """
        self.assertEqual(
            'Royal Flush',
            self.rank_or_better(['S']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Royal Flush',
            self.rank_or_better(['C']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Royal Flush',
            self.rank_or_better(['H']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Royal Flush',
            self.rank_or_better(['D']*5, ['Q', 'K', 'A', 'J', '10'])
        )

    @ddt.data(*tools.prepare_test_data(*data_straight_flush()))
    @ddt.unpack
    def test_straight_flush(self, test_suites, test_ranks):
        """Test Straight Flush: suits - {0}, ranks - {1}
        """
        self.assertEqual('Straight Flush',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_four_of_a_kind()))
    @ddt.unpack
    def test_four_of_a_kind(self, test_suites, test_ranks):
        """Test Four of a Kind: suits - {0}, ranks - {1}
        """
        self.assertEqual('Four of a Kind',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_full_house()))
    @ddt.unpack
    def test_full_house(self, test_suites, test_ranks):
        """Test Full House: suits - {0}, ranks - {1}
        """
        self.assertEqual('Full House',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(
        ('spades', ['S']*5, tools.generate_different_ranks()),
        ('clubs', ['C']*5, tools.generate_different_ranks()),
        ('hearts', ['H']*5, tools.generate_different_ranks()),
        ('diamonds', ['D']*5, tools.generate_different_ranks()),
    ))
    @ddt.unpack
    def test_flush(self, test_suites, test_ranks):
        """Test Flush: suits - {0}, ranks - {1}
        """
        self.assertEqual('Flush',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_straight()))
    @ddt.unpack
    def test_straight(self, test_suites, test_ranks):
        """Test Straight: suits - {0}, ranks - {1}
        """
        self.assertEqual('Straight',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_three_of_a_kind()))
    @ddt.unpack
    def test_three_of_a_kind(self, test_suites, test_ranks):
        """Test Three of a Kind: suits - {0}, ranks - {1}
        """
        self.assertEqual('Three of a Kind',
                         self.rank_or_better(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_two_pairs()))
    @ddt.unpack
    def test_two_pairs(self, test_suites, test_ranks):
        """Test Two Pairs: suits - {0}, ranks - {1}
        """
        self.assertEqual('Two Pairs',
                         self.rank_or_better(test_suites, test_ranks))


class TestTensOrBetter(unittest.TestCase):
    """Tests for TensOrBetter"""

    @classmethod
    def setUpClass(cls):
        cls.tens_or_better = TensOrBetter()

    def test_tens_or_better_positive(self):
        """Positive tests for Tens or Better
        """
        self.assertEqual(
            'Tens or Better',
            self.tens_or_better(tools.generate_different_suits(),
                                ['A', '2', 'A', '3', '4'])
        )
        self.assertEqual(
            'Tens or Better',
            self.tens_or_better(tools.generate_different_suits(),
                                ['K', '2', '3', 'K', '4'])
        )
        self.assertEqual(
            'Tens or Better',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', '2', '3', '4', 'Q'])
        )
        self.assertEqual(
            'Tens or Better',
            self.tens_or_better(tools.generate_different_suits(),
                                ['2', 'J', '3', '4', 'J'])
        )
        self.assertEqual(
            'Tens or Better',
            self.tens_or_better(tools.generate_different_suits(),
                                ['2', '3', '10', '4', '10'])
        )

    def test_tens_or_better_negative(self):
        """Negative tests for Tens or Better
        """
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['9', '9', 'Q', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', '8', '8', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', 'K', '7', '7', 'A'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', 'K', 'A', '6', '6'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', '5', 'K', '5', 'A'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['4', 'Q', 'K', 'A', '4'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['3', 'Q', 'K', '3', 'A'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                ['Q', '2', 'K', 'A', '2'])
        )
        self.assertEqual(
            '',
            self.tens_or_better(tools.generate_different_suits(),
                                tools.generate_different_ranks())
        )

    def test_negative(self):
        """Negative scenarios
        """
        # Invalid type
        self.assertRaises(TypeError, self.tens_or_better,
                          3, tools.generate_random_ranks())
        self.assertRaises(TypeError, self.tens_or_better,
                          tools.generate_random_suits(), 3)
        self.assertRaises(TypeError, self.tens_or_better, 3, 3)
        # Invalid length of list
        self.assertRaises(ValueError, self.tens_or_better,
                          [1, 2, 3, 4, 5, 6], tools.generate_random_ranks())
        self.assertRaises(ValueError, self.tens_or_better,
                          tools.generate_random_suits(), [1, 2, 3, 4, 5, 6])
        self.assertRaises(ValueError, self.tens_or_better,
                          [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6])
        # Incorrect values
        self.assertRaises(
            KeyError, self.tens_or_better,
            ['A', 'B', 'C', 'D', 'E'], tools.generate_random_ranks()
        )
        self.assertRaises(
            KeyError, self.tens_or_better,
            tools.generate_random_suits(), ['1', '11', 'C', 'B', 'X']
        )
        self.assertRaises(
            KeyError, self.tens_or_better,
            ['A', 'B', 'C', 'D', 'E'], ['1', '2', 'C', 'B', 'X']
        )


class TestJacksOrBetter(unittest.TestCase):
    """Tests for JacksOrBetter"""

    @classmethod
    def setUpClass(cls):
        cls.jacks_or_better = JacksOrBetter()

    def test_jacks_or_better_positive(self):
        """Positive tests for Jacks or Better
        """
        self.assertEqual(
            'Jacks or Better',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['A', '2', 'A', '3', '4'])
        )
        self.assertEqual(
            'Jacks or Better',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['K', '2', '3', 'K', '4'])
        )
        self.assertEqual(
            'Jacks or Better',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', '2', '3', '4', 'Q'])
        )
        self.assertEqual(
            'Jacks or Better',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['2', 'J', '3', '4', 'J'])
        )

    def test_jacks_or_better_negative(self):
        """Negative tests for Jacks or Better
        """
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['2', '3', '10', '4', '10'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['9', '9', 'Q', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', '8', '8', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', 'K', '7', '7', 'A'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', 'K', 'A', '6', '6'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', '5', 'K', '5', 'A'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['4', 'Q', 'K', 'A', '4'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['3', 'Q', 'K', '3', 'A'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 ['Q', '2', 'K', 'A', '2'])
        )
        self.assertEqual(
            '',
            self.jacks_or_better(tools.generate_different_suits(),
                                 tools.generate_different_ranks())
        )


if __name__ == '__main__':
    unittest.main()
