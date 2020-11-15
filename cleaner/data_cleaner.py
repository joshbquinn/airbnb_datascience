# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6

@author: Josh

Functions to clean and manipulate datasets

"""

import re

import cleaner
from cleaner.generic_cleaner import make_numeric
from reader.data_reader import as_rows, get_ids, get_headers
from reader.validator import is_numeric, validate_column, is_selected_numeric


def aggregate_columns(table):
    """Aggregate and average common columns into single column.

    Example: aggregate and average monthly cost values into quarterly, bi-annual, or annual values.

    Args:
         table: the converted csv into a table of data in the form of dictionary structure
    Returns
        table: the restructured table of data in the form of dictionary structure
    """
    go = ''
    while go not in ('y', 'n'):
        go = input("Do you want to combine data? [Yy/Nn]")
        if go == 'y':
            print("The available columns: ", list(table.keys()))
            wanted = input("Enter the columns to combine separated by space: ").lower().split(" ")
            if not validate_column(wanted, table):
                pass
            if not is_selected_numeric(wanted, table):
                print("Those columns are not all numeric.")
                pass
            else:
                columns = []
                for column, rows in table.items():
                    if column in wanted:
                        columns.append(rows)

                combined = average(columns)

                for column in wanted:
                    table.pop(column)

                confirm = ''
                while confirm not in ('y', 'n'):
                    column_name = input("Enter name for these combined columns: ")
                    confirm = input(f"You've chosen {column_name}. Are you sure? [Yy/Nn] ").strip().lower()
                    if confirm == 'y':
                        table[column_name] = list(combined)
                        continue
                    elif confirm == 'n':
                        confirm = ''
        if go == 'n':
            return table
        go = ''

    return table


def average(columns):
    """Sums columns together and for each row calculates the average of all cells from that row.

    :param columns: the columns to aggregate together and get and average for
    :return: the aggregated column
    """
    try:
        combined = [round(sum(tup) / len(tup), 2) for tup in zip(*columns)]
        return combined
    except ValueError as e:
        print("Error combining and averaging the data.", e)
        pass


def fix_numerics(table):
    """
    The driver function which calls other fixing numeric functions.
    Allows user to iteratively select columns to try and covert into numerical type columns.

    :param table: the data dictionary containing the csv data
    :return table: the data dictionary containing the original or updated columns
    """
    go = ''
    while go not in ('y', 'n'):
        go = input("Do you want to fix numeric data? [Yy/Nn]")
        if go == 'y':
            print("The available columns: ", list(table.keys()))
            wanted = []
            for column, rows in table.items():
                if type(rows[0]) == int or type(rows[0]) == float:
                    continue
                col = ''
                while col not in ('y', 'n'):
                    col = input(f"Make {column} numeric? [Yy/Nn]").lower().strip()
                    if col == 'y':
                        wanted.append(column)
                        continue
                    if col == 'n':
                        continue

            for column in wanted:
                rows = table.get(column)
                is_numeric(column, table)
                fix_invalid_numeric(rows)
                table[column] = make_numeric(column, rows)
        if go == 'n':
            return table
        go = ''

    return table


def fix_invalid_numeric(column):
    """
    Fix the invalid rows of a numeric column to be able to convert all rows to numerical type.
    :param column: the column of rows in the form of a list
    :return column: the column with fixed rows in the form of a list
    """
    for i in range(len(column)):
        if type(column[i]) == int or type(column[i]) == float:
            print(f"{(column[i])} is already numeric")
            continue
        if len(column[i]) == 0:
            column[i] = '0'
        if not re.match('[0-9.]', column[i]):
            column[i] = re.sub('[^0-9.]', '', column[i])
    return column


def append_price_column(master_dataset, csv_datasets, indexed_cols):
    """Appends the column price to the master file

    *NB, the method is tightly coupled to the 'price' column. Better would be to add an argument containing a list of
    the columns to append. This would generalize the method.

    Args:

        master_dataset: the dataset chosen to check other files against. If there is an entry match by ID, then we
                     append the price column onto the master dataset.

        csv_datasets: the list of other csv datasets we want to check for matching entries to append onto master dataset

        indexed_cols: the indices of columns, common for all datasets, keyed by column name. This is used to retrive the
                      correct column values between datasets.

    Returns:
        master_dataset: the list of rows with the appended price column.



    """
    count = 2
    id_index = indexed_cols.get("id")
    price_index = indexed_cols.get("price")
    for file in csv_datasets:
        print(f"Appending price column from file {file[0]} to master file")
        ids = get_ids(file[1])
        for master_row in master_dataset:
            if master_row[id_index] not in ids:
                master_row.append(0)
                continue
            for row in file[1]:
                if master_row[id_index] == "id":
                    master_row.append(row[price_index] + "_" + file[0].replace(".csv", "").replace("listings", ""))
                    break
                if master_row[id_index] == row[id_index]:
                    master_row.append(row[price_index])
                    break
        count += 1
    return master_dataset


def find_poor_data(file):
    """Finds the bad data in a given dataset. Namely the rows with incorrect number of cells,
    the cells with null values, and the cells with zero numeric value.

    It first reads the file into rows.
    It then iterates through the rows of the csv file, and creates dictionaries containing the rows with bad data
    keyed by the row ID.
    It calls the show bad data function to show user all poor data found.
    It then removes those rows from the dataset and returns the dataset with no poor data.

    *NB to make more generic we could use the {data_reader.index_columns()} and prompt user to select particular columns
    to include in this data cleanup. It may be ok for Some rows to contain zero, or may it be ok for some rows to be null.

    Args:
        file: the path to the file to search for bad data in.

    Returns:
        calls handle_bad_data which returns the rows with the rows containing bad data removed.
    """

    headers, rows = as_rows(file)

    bad_len_rows = {}
    bad_null_cell_rows = {}
    bad_zero_numeric_value = {}

    print("\nSearching for null values, zero values and rows with incorrect number of cells.")

    for row in rows:
        if len(row) != len(headers):
            bad_len_rows[row[0]] = row[1:]
        for cell in row:
            if len(cell) == 0:
                bad_null_cell_rows[row[0]] = row[1:]
            if cell.strip() in {'0.0', '0', '0.00', '00.00', '00'}:
                bad_zero_numeric_value[row[0]] = row[1:]

    show = input("Do you want to see bad data found?  (Yy / Nn): ").strip().lower()
    show_bad(show, bad_len_rows, bad_null_cell_rows, bad_zero_numeric_value, headers, rows)

    return handle_bad_data(bad_len_rows, bad_zero_numeric_value, bad_null_cell_rows, rows)


def handle_bad_data(lengths, zeros, nulls, original):
    """ Removes the rows containing data with nulls, zeros and with number of cells.

    Args:
        lengths: dictionary of rows with incorrect lengths keyed by row ID
        zeros: dictionary of rows with zero values keyed by row ID
        nulls: dictionary of rows with null values keyed by row ID
        original: the original uncleaned dataset

    Returns:
        the cleaned dataset with rows containing data with nulls, zeros and with number of cells removed.

    """
    if len(lengths) > 0:
        print("Removing rows with incorrect lengths")
        original = [row for row in original if row[0] not in lengths.keys()]
        print("Removed rows with incorrect lengths")
    print("Delete all data with '0' values from original set")
    original = [row for row in original if row[0] not in zeros.keys()]
    return [row for row in original if row[0] not in nulls.keys()]


def show_bad(show, bad_len_rows, bad_null_cell_rows, bad_zero_numeric_value, headers, rows):
    """Shows the bad data found.

    *NB to improve usability of this function it would be better to print the bad data out to a file to debug.

    Args:
        show: user input to select whether to show or not.
        bad_len_rows: dictionary of rows with incorrect lengths keyed by row ID
        bad_null_cell_rows: dictionary of rows with zero values keyed by row ID
        bad_zero_numeric_value: dictionary of rows with null values keyed by row ID
        headers: the column names of the dataset
        rows: the rows of the dataset
    """
    while show != 'y' or show != 'n':
        if show == 'y':
            print("Rows with missing columns: ")
            for id, row in bad_len_rows.items():
                print(id, row)

            print("\nRows with null column cells: ")
            for id, row in bad_null_cell_rows.items():
                print(id, row)

            print("\nRows with cells containing zero: ")
            for id, row in bad_zero_numeric_value.items():
                print(id, row)
            show = 'n'
        elif show == 'n':
            print("\n SUMMARY \n")
            count_bad_row_len = sum(len(row) < len(headers) for row in rows)
            count_null_cells = sum(sum(len(cell) <= 0 for cell in row) for row in rows)
            count_cells_with_zero_val = sum(sum(cell in {'0', '0.00', '00.00', '00'} for cell in row) for row in rows)
            print(f"\nNumber of rows with missing columns: {count_bad_row_len}. Number of rows: {len(bad_len_rows)}.")
            print(
                f"Number of cells with zero value: {count_cells_with_zero_val}. Number of rows: {len(bad_zero_numeric_value)}.")
            print(f"Number of cells with null values: {count_null_cells}. Number of rows: {len(bad_null_cell_rows)}.")
            return
        else:
            show = input("Do you want to see bad data? (Yy / Nn: ").strip().lower()


def scrub_table(file_name, headers):
    """
    This function calls the find bad data functions, cleans up the rows, tries to convert the rows to numberic
    and converts the rows into a dictionary object.

    Args:
        file_name: the file path of the csv file
        headers: the column names to
    Returns:

    """
    clean_q = ''
    while clean_q not in ('y', 'n'):
        clean_q = input("Do you want to scrub the data? (Yy/Nn): ")
        if clean_q == 'n':
            continue
        elif clean_q == 'y':
            clean_rows = find_poor_data(file_name)
            print("Creating dictionary without any null cells or cells with zero value.")
            converted_columns = [list(val) for val in zip(*clean_rows)]
            table_dataset = dict(zip(headers, converted_columns))
            clean_table = {k: cleaner.generic_cleaner.make_numeric(k, v) for (k, v) in table_dataset.items()}
            return clean_table


def set_average(clean_table, unclean_table):
    """
    Provides two of the same datasets, one without any zeros, and one with zeros. Function calculates the average values of
    numerical columns of the clean_table, the dataset without any zeros, and then sets any column with zero in the unclean_table
    with that average.

    We use this clean_table because:
    1. in order to convert a list to numerical values it cannot contain nulls, and we need numerical values to get an average, and
    2. zeros will greatly skew an average so we want a dataset without zeros

    *NB the method is over-engineered and can be done in simpler ways using list comprehension I think
    nums = [float(x) for x in nums if type(float(x)) == True]

    Args:
        clean_table: datasets without any zeros
        unclean_table: dataset with zeros
    Returns:
        unclean_table: the dictionary of csv values now with the average set.

    """
    try:
        for header, column in unclean_table.items():
            if header not in clean_table.keys():
                continue
            data_sample = clean_table.get(header)[0]
            if not isinstance(data_sample, (float, int, complex)):
                print(f"'{header}' doesn't look like a numeric column".capitalize())
                continue
            else:
                average = sum(clean_table.get(header)) / len(clean_table.get(header))
                if isinstance(clean_table.get(header)[0], float):
                    average = round(average, 2)
                else:
                    average = int(average)
            count = 0
            for i in range(len(column)):
                if column[i] == 0:
                    column[i] = average
                    count +=1
            print(f"Converted {count}/{len(column)} '{header}' rows with 0 value to the '{header}' average of {average}")

        return unclean_table
    except ValueError as e:
        print(f"Could not get average for {header}.")


def do_clean(file, unclean_table):
    """Calls the scrub_table function and does all the initial data cleaning.

    Args:
        file: the file to read the csv dataset from
        unclean_table: the table containing zeros.

    Returns:
        cleaned_table the table
    """
    headers = get_headers(file)
    scrubbed_table = scrub_table(file, headers)
    if scrubbed_table is None:
        print("Return the uncleaned table for analysis")
        return unclean_table
    else:
        cleaned_table = set_average(scrubbed_table, unclean_table)
        return cleaned_table
