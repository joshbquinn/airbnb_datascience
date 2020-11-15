# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6

@author: Josh

Function used generically to convert string numbers to int or float types.
Separated this function to prevent circular dependencies.

"""


def make_numeric(header, column):
    """
    Convert String numeric column values into numeric data types

    :param header: the column name
    :param column: the column rows to try convert into numerical values
    :return: the column, either transformed or in its original state
    """
    try:
        col = [int(x) for x in column]
        print(f"Successfully set '{header}' as integer type.")
        return col
    except ValueError:
        try:
            col = [round(float(x), 2) for x in column]
            print(f"Successfully set '{header}' as float type.")
            return col
        except ValueError:
            pass
            return column