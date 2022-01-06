# Copyright (c) 2016-2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Jacks or Better engine"""

import collections
from .base import *


CAPTION = 'Jacks or Better'
BACKGROUND_COLOR = (0, 65, 15)

# Table of winnings
poker_winnings = collections.OrderedDict((
    ('Royal Flush',     [250, 500, 750, 1000, 4000]),
    ('Straight Flush',  [50,  100, 150, 200,  250]),
    ('Four of a Kind',  [25,  50,  75,  100,  125]),
    ('Full House',      [9,   18,  27,  36,   45]),
    ('Flush',           [6,   12,  18,  24,   30]),
    ('Straight',        [4,   8,   12,  16,   20]),
    ('Three of a Kind', [3,   6,   9,   12,   15]),
    ('Two Pairs',       [2,   4,   6,   8,    10]),
    ('Jacks or Better', [1,   2,   3,   4,    5])
))
combination_names = poker_winnings.keys()


class JacksOrBetter(RankOrBetter):
    """Class for 'Jacks or Better' engine"""

    def rank_or_better(self):
        """Check for Jacks or Better

        :return: 'Jacks or Better'
        :type: str
        """
        for rank in ['J', 'Q', 'K', 'A']:
            if self.card_ranks.count(rank) == 2:
                return 'Jacks or Better'
        return ''
