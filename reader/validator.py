# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12

@author: Josh

Functions to validate or invalidate data while cleaning.
"""


def check_list_for_nums_and_size(nums_list):
    """Check if a given list's elements are all numbers

    :param nums_list: the list of elements to validate
    :return is_numeric_list: the result of whether the list contains all numerical values or not
    """
    if len(nums_list) < 1:
        print("List has zero values")
        return False
    boolean_list = [type(x) == int or type(x) == float for x in nums_list]
    is_numeric_list = all(boolean_list)
    if is_numeric_list is False:
        print("List contains non-numeric values.")
    return is_numeric_list


def is_numeric(header, table):
    """
    Checks if the rows in a column can be converted to numerical values and finds and prints the invalid rows.
    :param header: the column name to retrieve the column to check
    :param table: the table of data

    """
    column = table.get(header)
    ids = table.get("id")
    ids_column = zip(ids, column)
    print("\nChecking for valid numeric rows in", header)
    invalid_ints = []
    invalid_floats = []

    for id, row in ids_column:
        try:
            int(row)
        except ValueError:
            invalid_ints.append((id, row))
        try:
            float(row)
        except ValueError:
            invalid_floats.append((id, row))

    if len(invalid_ints) > 0 and len(invalid_floats) > 0:
        if len(invalid_ints) < len(invalid_floats):
            print(f"{len(invalid_ints)}/{len(ids)} invalid rows: ")
            print("Invalid integer rows:")
            for row in invalid_ints:
                print(row)
        else:
            print(f"{len(invalid_floats)}/{len(ids)} invalid rows: ")
            print("Invalid float rows:")
            for row in invalid_floats:
                print(row)
    else:
        print("All values numeric")


def is_selected_numeric(wanted_columns, table):
    """Check if the values wanted to aggregate are numeric

    Args:
        wanted_columns: the list of columns selected by user
        table: the actual data created from the original csv file

    Returns:
        True or False depending if the wanted columns are numeric
    """
    booleans = []
    for column in wanted_columns:
        values = table.get(column)
        booleans.append(check_list_for_nums_and_size(values))

    return all(booleans)


def validate_column(wanted_columns, table):
    """
    Validate selected columns for data manipulation by checking if they exist in the data table converted from csv file

    Args:
        wanted_columns: the list of columns selected by user
        table: the actual data created from the original csv file

    Returns:
        True or False depending if the wanted columns exist in the actual data set
    """
    for column in wanted_columns:
        if column not in table.keys():
            print(f"Column {column} wasn't found in the table ")
            return False

    return True
