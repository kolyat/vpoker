# Copyright (c) 2016-2019 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Tens or Better engine"""

import collections
from .base import *


CAPTION = 'Tens or Better'
BACKGROUND_COLOR = (0, 25, 50)

# Table of winnings
poker_winnings = collections.OrderedDict((
    ('Royal Flush',     [500, 1000, 2000, 3000, 4000]),
    ('Straight Flush',  [50,  100,  150,  200,  250]),
    ('Four of a Kind',  [25,  50,   75,   100,  125]),
    ('Full House',      [6,   12,   18,   24,   30]),
    ('Flush',           [5,   10,   15,   20,   25]),
    ('Straight',        [4,   8,    12,   16,   20]),
    ('Three of a Kind', [3,   6,    9,    12,   15]),
    ('Two Pairs',       [2,   4,    6,    8,    10]),
    ('Tens or Better',  [1,   2,    3,    4,    5])
))
combination_names = poker_winnings.keys()


class TensOrBetter(RankOrBetter):
    """Class for 'Tens or Better' engine"""

    def rank_or_better(self):
        """Check for Tens or Better

        :return: 'Tens or Better'
        :type: str
        """
        for rank in ['10', 'J', 'Q', 'K', 'A']:
            if self.card_ranks.count(rank) == 2:
                return 'Tens or Better'
        return ''
