# Copyright (c) 2016-2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Unit tests for Deuces Wild game engine"""

import random
import itertools
import unittest
import ddt
from tests import tools

from engine.base import suit_list, ranks
from engine.deuces_wild import DeucesWild

suit_list = list(suit_list)
ranks_no_deuce = list(ranks)
ranks_no_deuce.remove('2')


def data_deuces_royal_flush():
    """Prepare data for Deuces Royal Flush
    """
    for suit in suit_list:
        for deuces in (1, 2, 3):
            _test_suits = suit_list[0:deuces] + [suit]*(5-deuces)
            for _ranks in itertools.combinations(
                    ['10', 'J', 'Q', 'K', 'A'], 5-deuces):
                _test_ranks = ['2']*deuces + list(_ranks)
                yield (
                    '{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                    _test_suits, _test_ranks
                )


def data_five_of_a_kind():
    """Prepare data for Five of a Kind
    """
    for deuces in (1, 2, 3):
        for rank in ranks_no_deuce:
            _test_suits = suit_list[0:deuces] + \
                          tools.generate_different_suits()[0:5-deuces]
            _test_ranks = ['2']*deuces + [rank]*(5-deuces)
            yield (
                '{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                _test_suits, _test_ranks
            )


def data_straight_flush():
    """Prepare data for Straight Flush
    """
    for suit in suit_list:
        for deuces in (0, 1, 2, 3):
            _test_suits = suit_list[0:deuces] + [suit]*(5-deuces)
            straight_ranks = [ranks_no_deuce[i:i+5]
                              for i in range(len(ranks_no_deuce)-5-deuces)]
            for straight in straight_ranks:
                for _ranks in itertools.combinations(straight, 5-deuces):
                    _test_ranks = ['2']*deuces + list(_ranks)
                    yield (
                        '{}_{}'.format(''.join(_test_suits),
                                       ''.join(_test_ranks)),
                        _test_suits, _test_ranks
                    )


def data_four_of_a_kind():
    """Prepare data for Four of a Kind
    """
    random.seed(None)
    for deuces in (0, 1, 2, 3):
        for rank in ranks_no_deuce:
            second_rank = rank
            while second_rank == rank:
                second_rank = ranks_no_deuce[
                    random.randint(0, len(ranks_no_deuce)-1)]
            _test_ranks = ['2']*deuces + [rank]*(4-deuces) + [second_rank]
            _test_suits = tools.generate_different_suits()
            yield (
                ('{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                 _test_suits, _test_ranks)
            )


def data_full_house():
    """Prepare data for Full House
    """
    rank_pairs = itertools.combinations(ranks_no_deuce, 2)
    for deuces in (0, 1):
        for rank1, rank2 in rank_pairs:
            pair_combos = itertools.combinations_with_replacement(
                [rank1, rank2], 5-deuces)
            pair_combos = filter(
                lambda x: x.count(rank1) > 1 and x.count(rank2) > 1,
                pair_combos
            )
            for pair_combo in pair_combos:
                _test_ranks = list(pair_combo) + ['2']*deuces
                _test_suits = tools.generate_different_suits()
                yield (
                    ('_'.join((''.join(_test_suits), ''.join(_test_ranks))),
                     _test_suits, _test_ranks)
                )


def data_flush():
    """Prepare data for Flush
    """
    for suit in suit_list:
        for deuces in (0, 1, 2):
            _test_suits = suit_list[0:deuces] + [suit]*(5-deuces)
            _test_ranks = ['2']*deuces + \
                list(tools.generate_different_ranks()[:5-deuces])
            yield (
                '{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                _test_suits, _test_ranks
            )


def data_straight():
    """Prepare data for Straight
    """
    for deuces in (0, 1, 2):
        _test_suits = tools.generate_different_suits()
        straight_ranks = [ranks_no_deuce[i:i+5]
                          for i in range(len(ranks_no_deuce)-5-deuces)]
        for straight in straight_ranks:
            for _ranks in itertools.combinations(straight, 5-deuces):
                _test_ranks = ['2']*deuces + list(_ranks)
                yield (
                    '{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                    _test_suits, _test_ranks
                )


def data_three_of_a_kind():
    """Prepare data for Three of a Kind
    """
    random.seed(None)
    for deuces in (0, 1, 2):
        for rank in ranks_no_deuce:
            _test_ranks = ['2']*deuces + [rank]*(3-deuces)
            while len(_test_ranks) < 5:
                another_rank = ranks_no_deuce[
                    random.randint(0, len(ranks_no_deuce)-1)]
                if abs(ranks_no_deuce.index(rank) -
                       ranks_no_deuce.index(another_rank)) > deuces+1 \
                        and another_rank not in _test_ranks:
                    _test_ranks += [another_rank]
            _test_suits = tools.generate_different_suits()
            yield (
                '{}_{}'.format(''.join(_test_suits), ''.join(_test_ranks)),
                _test_suits, _test_ranks
            )


def data_two_pairs():
    """Prepare data for Two Pairs
    """
    pairs = [[r]*2 for r in ranks_no_deuce]
    raw = [i[0]+i[1] for i in itertools.product(pairs, pairs)]
    raw = list(filter(lambda x: len(set(x)) > 1, raw))
    for i in range(len(raw)):
        while len(raw[i]) < 5:
            r = ranks_no_deuce[random.randint(0, len(ranks_no_deuce)-1)]
            if r not in raw[i]:
                raw[i].append(r)
    raw = [(tools.generate_different_suits(), r)
           for r in map(tools.shuffle, raw)]
    return [('{}_{}'.format(''.join(s), ''.join(r)), s, r) for s, r in raw]


@ddt.ddt
class TestDeucesWild(unittest.TestCase):
    """Tests for DeucesWild"""

    @classmethod
    def setUpClass(cls):
        cls.deuces_wild = DeucesWild()

    def test_natural_royal_flush(self):
        """Test Natural Royal Flush
        """
        self.assertEqual(
            'Natural Royal Flush',
            self.deuces_wild(['S']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Natural Royal Flush',
            self.deuces_wild(['C']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Natural Royal Flush',
            self.deuces_wild(['H']*5, ['Q', 'K', 'A', 'J', '10'])
        )
        self.assertEqual(
            'Natural Royal Flush',
            self.deuces_wild(['D']*5, ['Q', 'K', 'A', 'J', '10'])
        )

    def test_four_deuces(self):
        """Test Four Deuces
        """
        self.assertEqual(
            'Four Deuces',
            self.deuces_wild(tools.generate_different_suits(),
                             ['2', '2', '2', '2', 'A'])
        )

    @ddt.data(*tools.prepare_test_data(*data_deuces_royal_flush()))
    @ddt.unpack
    def test_deuces_royal_flush(self, test_suites, test_ranks):
        """Test Deuces Royal Flush: suits - {0}, ranks - {1}
        """
        self.assertEqual('Deuces Royal Flush',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_five_of_a_kind()))
    @ddt.unpack
    def test_five_of_a_kind(self, test_suites, test_ranks):
        """Test Five of a Kind: suits - {0}, ranks - {1}
        """
        self.assertEqual('Five of a Kind',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_straight_flush()))
    @ddt.unpack
    def test_straight_flush(self, test_suites, test_ranks):
        """Test Straight Flush: suits - {0}, ranks - {1}
        """
        self.assertEqual('Straight Flush',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_four_of_a_kind()))
    @ddt.unpack
    def test_four_of_a_kind(self, test_suites, test_ranks):
        """Test Four of a Kind: suits - {0}, ranks - {1}
        """
        self.assertEqual('Four of a Kind',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_full_house()))
    @ddt.unpack
    def test_full_house(self, test_suites, test_ranks):
        """Test Full House: suits - {0}, ranks - {1}
        """
        self.assertEqual('Full House',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_flush()))
    @ddt.unpack
    def test_flush(self, test_suites, test_ranks):
        """Test Flush: suits - {0}, ranks - {1}
        """
        self.assertEqual('Flush',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_straight()))
    @ddt.unpack
    def test_straight(self, test_suites, test_ranks):
        """Test Straight: suits - {0}, ranks - {1}
        """
        self.assertEqual('Straight',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_three_of_a_kind()))
    @ddt.unpack
    def test_three_of_a_kind(self, test_suites, test_ranks):
        """Test Three of a Kind: suits - {0}, ranks - {1}
        """
        self.assertEqual('Three of a Kind',
                         self.deuces_wild(test_suites, test_ranks))

    @ddt.data(*tools.prepare_test_data(*data_two_pairs()))
    @ddt.unpack
    def test_two_pairs_negative(self, test_suites, test_ranks):
        """Test Two Pairs (negative test): suits - {0}, ranks - {1}
        """
        self.assertEqual('', self.deuces_wild(test_suites, test_ranks))

    def test_pair_negative(self):
        """Test Rank or Better (pair) (negative test)
        """
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['A', '10', 'A', '3', '4'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['K', '10', '3', 'K', '4'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', '10', '3', '4', 'Q'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['10', 'J', '3', '4', 'J'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['A', '3', '10', '4', '10'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['9', '9', 'Q', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', '8', '8', 'K', 'A'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', 'K', '7', '7', 'A'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', 'K', 'A', '6', '6'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', '5', 'K', '5', 'A'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['4', 'Q', 'K', 'A', '4'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['3', 'Q', 'K', '3', 'A'])
        )
        self.assertEqual(
            '',
            self.deuces_wild(tools.generate_different_suits(),
                             ['Q', '3', 'K', 'A', '7'])
        )

    def test_negative(self):
        """Negative scenarios
        """
        # Invalid type
        self.assertRaises(TypeError, self.deuces_wild,
                          3, tools.generate_random_ranks())
        self.assertRaises(TypeError, self.deuces_wild,
                          tools.generate_random_suits(), 3)
        self.assertRaises(TypeError, self.deuces_wild, 3, 3)
        # Invalid length of list
        self.assertRaises(ValueError, self.deuces_wild,
                          [1, 2, 3, 4, 5, 6], tools.generate_random_ranks())
        self.assertRaises(ValueError, self.deuces_wild,
                          tools.generate_random_suits(), [1, 2, 3, 4, 5, 6])
        self.assertRaises(ValueError, self.deuces_wild,
                          [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6])
        # Incorrect values
        self.assertRaises(
            KeyError, self.deuces_wild,
            ['A', 'B', 'C', 'D', 'E'], tools.generate_random_ranks()
        )
        self.assertRaises(
            KeyError, self.deuces_wild,
            tools.generate_random_suits(), ['1', '11', 'C', 'B', 'X']
        )
        self.assertRaises(
            KeyError, self.deuces_wild,
            ['A', 'B', 'C', 'D', 'E'], ['1', '2', 'C', 'B', 'X']
        )


if __name__ == '__main__':
    unittest.main()
