# Copyright (c) 2016-2018 Kirill 'Kolyat' Kiselnikov
# This file is the part of vpoker, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Tools for data driven testing"""


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
