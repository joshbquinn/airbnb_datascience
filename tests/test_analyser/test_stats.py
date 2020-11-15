# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12

@author: Josh

Test stats.py functions.
"""

from analyser import stats


def test_check_list_for_nums_and_size():
    # Positive test case
    list_true = [1, 2, 3, 45, 6]
    expected = True
    actual_true = stats.check_list_for_nums_and_size(list_true)
    assert expected == actual_true, "Should be True"

    # Negative test case
    list_false = [1, 2, 3, "5"]
    expected = False
    actual_false = stats.check_list_for_nums_and_size(list_false)
    assert expected is actual_false, "Should be False"

    # Negative test case
    list_null = []
    expected = False
    actual_false = stats.check_list_for_nums_and_size(list_null)
    assert expected is actual_false, "Should be False"


def test_get_median():
    # Positive tests
    odd_nums = [1, 2, 3]
    odd_median = stats.get_median(odd_nums)
    assert odd_median == 2, "Given odd list of numbers, should return number at the middle index"

    even_nums = [1, 2, 3, 4]
    even_median = stats.get_median(even_nums)
    assert even_median == 2.5, "Given even list of numbers, should return the result of centre two values added and divided by 2"

    # Negative Tests
    odd_nums = []
    odd_median = stats.get_median(odd_nums)
    assert odd_median is None, "Should invalidate the given empty input and return None"

    odd_nums = ["1", "2", "3"]
    odd_median = stats.get_median(odd_nums)
    assert odd_median is None, "Should invalidate the given input Strings and return None"

    string_list = ['hi', 'there']
    string_median = stats.get_median(string_list)
    assert string_median is None, "Should invalidate the given input Strings and return None"


def test_get_mean():
    assert stats.get_mean([1, 2, 3]) == 2, "Should be 2"


def test_get_mode():
    expected = 2
    input = [1, 2, 2, 3]
    actual, element = stats.get_mode(input)
    assert expected == actual, f"Given {input}, function should return {expected}"


def test_get_standard_deviation():
    expected = 1.4142135623730951
    input = [1, 2, 3, 4, 5]
    actual = stats.get_standard_deviation(input)
    assert expected == actual, f"Given {input}, function should return {expected}"


def test_calc_correlation():
    expected = -0.3
    input_1 = [1, 3, 2, 5, 4]
    input_2 = [9, 10, 7, 8, 6]
    actual = stats.calc_correlation(input_1, input_2)
    assert expected == actual, f"Given {input_1} and {input_2}, function should return {expected}"


def test_calc_string_mode():
    expected = "hi"
    input = ["you", "me", "him", "him", "her", "hi", "hi", "hi"]
    actual = stats.most_common_value(input)
    assert actual == expected, f"Given {input} , function should return {expected}"

