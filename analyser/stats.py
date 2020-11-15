# -*- coding: utf-8 -*-
"""
Created on Tue Dec 6
@author: Josh

Functions to analyse the cleaned data.
"""
import sys

from reader import data_reader
from reader.validator import check_list_for_nums_and_size


def get_mean(nums_mean):
    """Function used to calculate the mean of a given list of numbers.

    :param nums_mean: a given list of numbers
    :raises ZeroDivisionError, TypeError
    :return mean: the mean of the given list of numbers
    """
    total_mean = 0
    if len(nums_mean) == 0:
        return 0
    try:
        for n in nums_mean:
            total_mean += n

        mean = float(total_mean) / len(nums_mean)
        return round(mean, 2)
    except (ZeroDivisionError, TypeError):
        print(f"We got an error in the list...{nums_mean}", sys.exc_info()[0], )


def get_median(nums_median):
    """  Calculate the median of a given list of numbers
    Args:
        nums_median: the list of given numbers
    Returns:
        None: if the input list is invalid
        median: the calculated median value
    """
    if check_list_for_nums_and_size(nums_median) is False:
        print(f"Median is : {None}")
        return None
    else:
        nums_median = sorted(nums_median)
        if len(nums_median) % 2 != 0:
            index = ((len(nums_median) - 1) / 2)
            median = nums_median[int(index)]

        else:
            middle_two = nums_median[int(((len(nums_median) / 2)) - 1)] + nums_median[int((len(nums_median) / 2))]
            median = middle_two / 2

        return median


def get_mode(nums_mode):
    """Calculates the mode, or most common value in a given list of numbers

    :param nums_mode: a given list of numbers
    :return None: if the input list is invalid
    :return mode: the mode of the given list of numbers
    """
    mode_element = ''
    mode = 0
    if check_list_for_nums_and_size(nums_mode) is False:
        return mode
    else:
        for element in nums_mode:
            if nums_mode.count(element) > mode:
                mode = nums_mode.count(element)
                mode_element = element

        return mode, mode_element


def get_standard_deviation(nums_std_dev):
    """Calculate the standard deviation of a given list of numbers

    :param nums_std_dev: the input list to calculate standard deviation of

    :return None: if the input list is invalid
    :return std_deviation: the calculated standard deviation of the input list
    """
    if check_list_for_nums_and_size(nums_std_dev) is False:
        return None
    else:
        summed_squares = 0
        mean = get_mean(nums_std_dev)
        for number_std in nums_std_dev:
            summed_squares += (number_std - mean) ** 2
        summed_squared_mean = summed_squares / len(nums_std_dev)
        std_deviation = summed_squared_mean ** 0.5
        return std_deviation


def calc_correlation(nums_corr_1, nums_corr_2):
    """Calculate the correlation between two given lists of numbers.

    :param nums_corr_1: the first input list of numbers
    :param nums_corr_2: the second input list of numbers
    :return None: if the input list is invalid, or if the two lists are not of equal length
    :return correlation: the calculated correlation between the two lists
    """
    if check_list_for_nums_and_size(nums_corr_1) is False and check_list_for_nums_and_size(nums_corr_2) is False:
        print("lists contains non-numeric value.")
        return None
    if len(nums_corr_1) != len(nums_corr_2):
        print("lists not of equal length.")
        return None
    else:
        mean_a = get_mean(nums_corr_1)
        mean_b = get_mean(nums_corr_2)

        subtracted_mean_a = [(x - mean_a) for x in nums_corr_1]
        subtracted_mean_b = [(x - mean_b) for x in nums_corr_2]

        sqrs_a = [(x ** 2) for x in subtracted_mean_a]
        sqrs_b = [(x ** 2) for x in subtracted_mean_b]

        a_times_b = [(a * b) for (a, b) in zip(subtracted_mean_a, subtracted_mean_b)]

        sum_sqrs_a = sum(sqrs_a)
        sum_sqrs_b = sum(sqrs_b)

        sum_a_times_b = sum(a_times_b)

        correlation = sum_a_times_b / ((sum_sqrs_a * sum_sqrs_b) ** 0.5)
        return correlation


def most_common_value(feature):
    """Finds the most common values for a feature with string data types.
    Args:
        feature (list): the list of rows for a given column

    Returns:
       most_common (dict): dictionary of number of most_common features keyed by feature value.
    """
    most_common = {}

    for row in feature:
        if row not in most_common.keys():
            most_common[row] = 1
        else:
            most_common[row] += 1

    return max(most_common, key=most_common.get)


def calc_feature_average(feature):
    """Given a dict with a feature and a list of its values, calculate the average of the fature.

    Args:
        feature (dict): the feature and its list of attributes. E.g. a column.

    Returns:
         feature (dict): the average of the feature keyed by the feature name
    """
    feature = dict({(k, round(sum(v) / len(v), 2)) for (k, v) in feature.items()})
    return feature


def sum_grouped_feature(feature):
    """Given a dict with a feature and a list of its values, calculate the average of the fature.

    Args:
        feature (dict): the feature and its list of attributes. E.g. a column.

    Returns:
         feature (dict): the average of the feature keyed by the feature name
    """
    feature = dict({(k, round(sum(v), 2)) for (k, v) in feature.items()})
    return feature


def sum_grouped_string_feature(feature):
    """Given a dict with a feature and a list of its values, calculate the average of the fature.

    Args:
        feature (dict): the feature and its list of attributes. E.g. a column.

    Returns:
         feature (dict): the average of the feature keyed by the feature name
    """
    feature = dict({(k, len(v)) for (k, v) in feature.items()})
    return feature


def group_by_rows(headers, rows, aggregate_column, group_by_column):
    """Groups values by a given feature and value
        1. retrieves the indices of the column to group and the column to group by
        2. iterates over the rows and groups the features
    Args:
        headers: the column names
        rows: the rows to group
        aggregate_column: column name of values to aggregate
        group_by_column: the column name to group values by 

    Returns:
        grouped_features (dict): dictionary of lists of values keyed by grouping feature

    """
    grouped_features = {}
    index_cols = data_reader.index_columns(headers)

    for row in rows:
        by_feature = row[index_cols.get(group_by_column)]
        group_value = row[index_cols.get(aggregate_column)]

        if by_feature not in grouped_features:
            grouped_features[by_feature] = [group_value]
        else:
            grouped_features.get(by_feature).append(group_value)

    return grouped_features
