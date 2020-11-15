# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6

@author: Josh

Functions to read, clean and write csv files

"""


def read(file_name):
    """Reads data from a file
        Args:
            file_name (String): the name of the file to read from
        Raises:
            IOError: Error writing the file out
    """
    try:
        with open(file_name) as reader:
            try:
                columns = []
                for line in reader.readlines():
                    columns.append(line.strip())
                return columns
            except UnicodeDecodeError as e:
                print("Error parsing file in UTF-8 encoding", e)
    except IOError as e:
        print(f"Could not find specified file '{file_name}'", e)


def write(file_name, listings):
    """Writes data to a file

        Args:
            listings (list of lists of Strings): the list of table rows. Each row is a list of Strings
            file_name (String): the name of the file to write out
        Raises:
            IOError: Error writing the file out
    """
    try:
        with open(file_name, "w", newline="", encoding='utf-8') as csv_file:
            for row in listings:
                csv_file.write(str(row).replace(" ", "").replace("'", "").strip('[').strip(']') + '\n')
    except IOError as e:
        print(f"Could not find specified file '{file_name}'", e)


def load_dict(file_name):
    """Loads the csv file from storage into a data dict.

        This is the second step, before the data has been scrubbed. The returned dict contains the raw data
        with unwanted columns, null values, and potentially, unknown utf-8 characters.

        Args:
            file_name (String): the file to load from storage.
        Raises:
            IOError: an error occurred while trying to read file.
        Returns:
            table_data (dict): the data dictionary containing the raw csv values in a dataframe like manner.
    """
    try:
        with open(file_name, 'r', errors='replace', encoding='utf-8') as reader:
            headers = [x.strip() for x in reader.readline().strip().strip(" ").split(",")]
            values = [line.strip().split(',') for line in reader]
        table_data = {c: v for c, v in zip(headers, [*zip(*values)])}
        return table_data
    except IOError as e:
        print("Error trying to read file, ", e)


def save_dict(file_name, clean_table_data):
    """Write the dictionary of clean rows to file.

        This is the fifth step in the initial clean-up process.

        First, we convert the dict (k,v pairs of column name to column values) to a list of rows using zip()
        Second, we convert the list of column names to a string, replacing unwanted characters and writing to file.
        Third, we iteratively convert each row to a string, replacing replacing unwanted characters, and any special
        characters that could not be converted to utf-8 before writing to file.

        Within our dataset we are concerned with numerical values and therefore can remove special
        characters unknown within utf-8.

        Args:
            file_name (String): the name of te file to write out to.
            clean_table_data (dict): the cleaned table data in the form of dictionary.
                Each (k,v) pair are the column name and all column values.
            column_names (list): the list of column names of the rows to be written to file.
        Raises:
            IOError: error while writing data to file
    """
    rows = [list(col) for col in zip(*clean_table_data.values())]
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        csv_file.write(str(list(clean_table_data.keys())).replace("'", "").strip('[').strip(']') + '\n')
        for row in rows:
            csv_file.write(str(row).replace("�", "").replace("'", "").strip('[').strip(']') + '\n')


def load_rows(file_name):
    """Loads a csv file in utf-8 encoding as a list of rows, i.e. a list of lists.

        Args:
            file_name (String): the input file to read
        Raises:
            IOError: Error opening the file
            UnicodeDecodeError: Error parsing file in specified encoding

        Returns:
            rows: a list of raw rows, uncleaned.
        """
    try:
        with open(file_name, "r", errors='replace', encoding='utf-8') as table:
            print("Loading Data")
            rows = []
            try:
                for row in table:
                    new_row = []
                    for cell in row.strip().split(","):
                        new_row.append(cell)
                    rows.append(new_row)
                return rows
            except UnicodeDecodeError:
                print("Error parsing file in UTF-8 encoding")
    except IOError:
        print(f"Could not find specified file '{file_name}'")
        pass


def choose_columns(table_data):
    """Select the columns you want to keep and discard from the csv file

    1. Function will try to read if previously saved columns to keep are written to file.
    2. Prompts user to interactively select and preview column data.
    3. Prompts user to interactively select the columns to keep or discard.
    4. Prompts user tp confirm the chosen columns to keep.
    5. Prompts user to save the chosen columns to file to save time next time.

    Args:
        table_data (dict): the csv data in dict of column rows keyed by column name

    Returns:
        columns_to_keep (list):

    """
    print("Option to view and remove unwanted columns from dataset")
    unwanted_columns = []
    columns_to_keep = read("./data/wantedcolumns.csv")
    print()
    if columns_to_keep is None:
        print("Nothing saved")
    elif len(columns_to_keep) > 0:
        print("There are previously stored wanted columns")
        print(str(columns_to_keep).strip("[").strip("]"))
        use = ''
        while use not in ('n', 'y'):
            use = input("Do you want to use these? [Yy/Nn] ").strip().lower()
            if use == 'y':
                return columns_to_keep
            if use == 'n':
                continue

    print(f"There are {len(table_data.keys())} columns in table")
    for column, values in table_data.items():
        view = ''
        while view not in ('n', 'y'):
            view = input(f"View values for column '{column}'? [Yy/Nn]").strip().lower()
            if view == 'n':
                continue
            if view == 'y':
                print(f"There are {len(values)} rows in the column")
                try:
                    cells = int(input("How many rows would you like to see?"))
                    for value in values[:cells]:
                        print(value)
                except ValueError as e:
                    print(f"'{cells}' is not a valid number. Error raised:", e)

        keep = ''
        while keep not in ('n', 'y'):
            keep = input(f"Keep column '{column}'? [Yy/Nn]").strip().lower()
            if keep == 'y':
                continue
            if keep == 'n':
                unwanted_columns.append(column)
                continue
    columns_to_keep = [col for col in table_data.keys() if col not in unwanted_columns]
    unwanted = confirm_column_choice(columns_to_keep)
    unwanted_columns.extend(unwanted)
    columns_to_keep = [col for col in table_data.keys() if col not in unwanted_columns]
    save_columns(columns_to_keep)

    return columns_to_keep


def confirm_column_choice(columns):
    """Prompts user to confirm the select columns to keep, clean and save from the original csv file.

    Args:
        columns (list): the list of column names to keep

    Returns:
        unwanted (list): the amended columns to discard list

    """
    unwanted = []
    print("The selected columns to keep")
    for col in columns:
        print(col)
        remove = ''
        while remove not in ('n', 'y'):
            remove = input(f"Remove column '{col}'? [Yy/Nn]").strip().lower()
            if remove == 'y':
                unwanted.append(col)
                continue
            if remove == 'n':
                continue
    return unwanted


def save_columns(columns):
    """Prompts user to save the columns to keep to file for future use.

    If user selects 'yes' to prompt, the wanted columns are written to file.

    Args:
        columns (list): the list of columns to keep
    """
    save = ''
    while save not in ('n', 'y'):
        save = input(f"Save wanted columns for future reference? [Yy/Nn]").strip().lower()
        if save == 'y':
            write("./data/wantedcolumns.csv", columns)
            continue
        if save == 'n':
            continue


def remove_unwanted_columns(csv_file_dict, wanted_columns):
    """Remove the unwanted columns from the dataset

    Args:
        csv_file_dict: the csv file converted into a dictionary
        wanted_columns: the list of wanted columns to keep

    Returns:
        table_data: the dictionary of wanted columns

    """
    table_data = {k: v for k, v in csv_file_dict.items() if k in wanted_columns}
    return table_data


def find_largest_table(csv_files):
    """Find the the csv file with the largest dataset.

    Args:
        csv_files: all the csv_files for which we want to aggregate data from

    Returns:
         index: the index of the largest file from the input list of files
         master: the master file, or the file which has the largest dataset to check against all other csv files for matches.
    """
    master = csv_files[0]
    length = 0
    index = 0
    for i in range(len(csv_files)):
        csv = load_rows("./data/clean/" + csv_files[i])
        if len(csv) > length:
            master = csv_files[i]
            length = len(csv)
            index = i
    return index, master


