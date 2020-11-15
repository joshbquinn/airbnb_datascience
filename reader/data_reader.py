# -*- coding: utf-8 -*-
"""
Created on Tue Dec  12

@author: Josh

Functions to read data to analyse

"""
from cleaner.generic_cleaner import make_numeric


def as_rows(file):
    """Takes a csv file and converts it to a list of rows.

    This method is good for row look up when used in conjunction with a dictionary of same type.
    example:
        where (k,v) is (k,v) for all v in column in table.items():
            return rows where all v in rows

    Args:
        file (String): the file location

    Returns:
        headers (list): the list of column names
        rows (list of lists): the rows of the csv file

    """
    try:
        y = "0"
        with open(file, encoding="utf8") as reader:
            headers = [x.strip() for x in reader.readline().strip().split(",")]
            rows = [[x.strip() for x in line.strip().split(",")] for line in reader]

            return headers, rows
    except FileNotFoundError:
        print('Cannot open the file')


def as_dictionary(file_name):
    """"Takes a csv file and converts it to a dictionary of headers and columns.

    The keys correspond to the header names and values correspond to the columns in the form of lists.

    Args:
        file_name (String): the csv file location

    Returns:
        headers (List): the column names
        unclean_table (dict): the column rows of the csv file keyed by column names

    Raises:
        FileNotFoundError
    """

    try:
        with open(file_name, encoding="utf8") as reader:
            print(f"Creating Searchable Data from file '{file_name}'")
            headers = [x.strip() for x in reader.readline().strip("\n").lower().split(",")]
            clean_rows = [[x.strip() for x in line.strip().split(",")] for line in reader]
            columns = [list(val) for val in zip(*clean_rows)]
            table = dict(zip(headers, columns))
            unclean_table = {k: make_numeric(k, v) for (k, v) in table.items()}

            return unclean_table

    except FileNotFoundError:
        print('Cannot open the file')


def transpose_to_rows(data_table):
    """Given a data table in the form of a dictionary structure with rows keyed by column,
        transpose the dictionary into a list of rows.

    Args:
        data_table: the dictionary object that stores the csv data.

    Returns:
        data_rows: the list of lists containing the rows of the csv dile.

    """
    data_rows = [list(row) for row in zip(*data_table.values())]
    return data_rows


def find_entry(rows, entry_id):
    """Given a list of rows and entry id, returns the row where entry id exists.

    Args:
        rows (List): the list of data rows
        entry_id (integer): the id of the row for which the user is searching for

    Returns:
        row (list): the row if found
    """
    for row in rows:
        if str(row[0]) == str(entry_id):
            return row


def get_ids(rows):
    """Given a list of rows return the IDs
    Args:
        rows: the rows of the csv data.

    Returns:
        ids: the list ids of the csv file.
    """
    ids = []
    for row in rows:
        ids.append(row[0])
    return ids


def index_columns(column_headers):
    """Create an index for the columns of a given list of rows.
    This helps with lookup.

    Args:
        column_headers: The headers of the csv file columns

    Returns:
        indexed_columns: a dictionary of indexes keyed by header name

    """
    indexed_columns = {}
    for index in range(len(column_headers)):
        indexed_columns[column_headers[index]] = index
    return indexed_columns


def get_headers(file_name):
    """Returns the column names from a csv file

    Args:
        file_name (String): the file location

    Returns:
        headers (list): the list of column names from the csv

    Raises:
        IOError: an error occurred while trying to read file.


    """
    try:
        with open(file_name, errors='replace', encoding="utf8") as reader:
            headers = [x.strip() for x in reader.readline().strip().strip(" ").split(",")]
            return headers
    except IOError as e:
        print("Error trying to read file, ", e)


def sort_keys(dataset):
    """Sort a dataset by key

    Args:
        dataset: the dictionary of values to sort

    Returns:
        dataset: the sorted dataset
    """

    return {key: dataset[key] for key in sorted(dataset.keys())}


def combine_data_if_key_contains(index, key, values, data, characters, new_key):
    """More Specific function to combine values from groups that share a common column name

    Args:
        index:
        key:
        values:
        data:
        characters:
        new_key:

    Returns:

    """
    if isinstance(characters, (list, tuple)):
        characters = [str(x) for x in characters]
    else:
        characters = str(characters)

    if characters in key:
        if index < 10:
            loc = new_key + '0' + characters
        else:
            loc = new_key + characters
        if loc not in data:
            data[loc] = [values]
        else:
            data.get(loc).append(values)
    return data
