# Copyright (c) 2016-2019 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Tools for data driven testing"""

import random
from engine.base import suit_list, ranks


class DataList(list):
    """Custom list with __name__ attribute, which is added by
    prepare_test_data()
    """
    pass


def prepare_test_data(*test_data):
    """Generator to prepare data for DDT

    :param test_data: tuples with name of the test, input value and expected
                      output value

    :return: named list with input value and expected output value
    """
    for td in test_data:
        _test_name, _input, _expected = td
        data_list = DataList([_input, _expected])
        setattr(data_list, '__name__', _test_name)
        yield data_list


def generate_random_suits():
    """Generates 5 random suits

    :return: 5 random suits
    :type: list
    """
    random.seed(None)
    return [suit_list[random.randint(0, len(suit_list)-1)] for _ in range(5)]


def generate_random_ranks():
    """Generates 5 random ranks

    :return: 5 random ranks
    :type: list
    """
    random.seed(None)
    return [ranks[random.randint(0, len(ranks)-1)] for _ in range(5)]


def generate_different_suits():
    """Create hand with 4 suits from list and 1 random

    :return: 5 suits
    :type: list
    """
    _suits = list(suit_list)
    random.seed(None)
    _suits.append(suit_list[random.randint(0, len(suit_list)-1)])
    return _suits


def generate_different_ranks():
    """Create hand with 'even' ranks

    :return: 5 ranks
    :type: list
    """
    return ['2', '4', '6', '8', '10']


def shuffle(unshuffled):
    """Shuffle items

    :param unshuffled: list with items (suits or ranks)

    :return: list with shuffled items
    """
    random.seed(None)
    _unshuffled = list(unshuffled)
    shuffled = list()
    while _unshuffled:
        shuffled.append(_unshuffled.pop(random.randint(0, len(_unshuffled)-1)))
    return shuffled
