"""
Project
"""

import wk_seven


# dealing with nulls...
# remove all rows where the data is 0 or null
# replace 0 with average of all data. 
# KeyError

def find_bad_data(file):
    with open(file, encoding="utf8") as reader:
        headers = [x for x in reader.readline().strip().split(",")]
        rows = [[x for x in line.strip().split(",")] for line in reader]

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
    if len(lengths) > 0:
        print("Removing rows with incorrect lengths")
        original = [row for row in original if row[0] not in lengths.keys()]
        print("Removed rows with incorrect lengths")
    print("Delete all data with '0' values from original set")
    original = [row for row in original if row[0] not in zeros.keys()]
    return [row for row in original if row[0] not in nulls.keys()]


def show_bad(show, bad_len_rows, bad_null_cell_rows, bad_zero_numeric_value, headers, rows):
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


def numeric_column(header, column):
    try:
        col = [int(x) for x in column]
        print(f"Successfully set column '{header}' as integer type.")
        return col
    except ValueError:
        try:
            col = [float(x) for x in column]
            print(f"Successfully set column '{header}' as float type.")
            return col
        except ValueError:
            pass
            return column


def set_average(clean_table, unclean_table):
    try:
        for header, column in unclean_table.items():
            if isinstance(unclean_table.get(header)[0], (float, int, complex)):
                print(f"Looks like column '{header}' has already been cleaned.")
                continue
            if not isinstance(clean_table.get(header)[0], (float, int, complex)):
                print(f"'{header}' doesn't look like a numeric column".capitalize())
                continue
            else:
                average = sum(clean_table.get(header)) / len(clean_table.get(header))
                if isinstance(clean_table.get(header)[0], float):
                    average
                else:
                    average = int(average)
            for i in range(len(column)):
                if len(column[i]) == 0:
                    column[i] = average
    except ValueError:
        print(f"Could not get average for {header}.")

def as_rows(file):
    """
        This method takes a csv file and converts it to a list of rows.
        This method is good for row look up when used in conjunction with a dictionary of same type.
        example:
            where (k,v) is (k,v) for all v in column in table.items():
                return rows where all v in rows
    """
    try:
        y = "0"
        with open(file, encoding="utf8") as reader:
            rows = [[y in x for x in line.strip().split(",")] for line in reader]
        return rows
    except FileNotFoundError:
        print('Cannot open the file')


def find_entry(rows, entry_id):
    for row in rows:
        for cell in row:
            if str(cell) == str(entry_id):
                return row


def as_dictionary(file_name):
    """
        This method takes a csv file and converts it to a dictionary of headers and columns.
        The keys correspond to the header names and values correspond to the columns in the form of lists.
    """
    try:
        with open(file_name, encoding="utf8") as reader:
            print("Creating Searchable Data")
            headers = [x for x in reader.readline().strip("\n").lower().split(",")]
            clean_rows = [[x for x in line.strip().split(",")] for line in reader]
            columns = [list(val) for val in zip(*clean_rows)]
            table = dict(zip(headers, columns))
            unclean_table = {k: numeric_column(k, v) for (k, v) in table.items()}

            clean_q = ''
            while clean_q not in ('y', 'n'):
                clean_q = input("Do you want to clean the data? (Yy/Nn): ")
                if clean_q == 'n':
                    continue
                elif clean_q == 'y':
                    clean_rows = find_bad_data(file_name)
                    print("Creating two dictionaries, one with zero values and one without")
                    columns_1 = [list(val) for val in zip(*clean_rows)]
                    table_1 = dict(zip(headers, columns_1))
                    clean_table = {k: numeric_column(k, v) for (k, v) in table_1.items()}
                    set_average(clean_table, unclean_table)

    except FileNotFoundError:
        print('Cannot open the file')


airbnb = as_dictionary("data/airbnb_cleaner_listings_2.csv")[0]
rtb = as_dictionary("data/rtb_cleaned_rent_deleted_rows_with_no_price_3.csv")[0]

quit = ''

print("\n\nOk, data sets are stored in memory. ")
while quit != 'y':

    view = ""
    while view not in ("y", "n"):
        view = input("\nView available columns for both sets? (Yy/Nn): ").lower()

    if view == 'y':
        print("Airbnb: ", airbnb.keys())
        print("Rent Tenancy board: ", rtb.keys())


    data_dict = {}
    data_choice = ""
    while data_choice not in ("airbnb", "rtb"):
        data_choice = input("\nWhich dataset would you like to get stats on? "
                            "\nAirbnb (airbnb) or Rent Tenancy Board (rtb)? "
                            "\nEnter (airbnb/rtb): ")

    if data_choice == "airbnb":
        data_dict = airbnb
    elif data_choice == "rtb":
        data_dict = rtb


    stat = ""
    while stat not in ("mode", "mean", "median", "standard deviation", "correlation", "all"):
        stat = input("\nWhat stat would you like to calculate? Mode, Mean, Median, Standard Deviation, Correlation, "
                     "or all? Enter one: ").strip().lower()

    confirm = ''
    feature = ''
    correlate = ''
    print(f"\nChoose feature from {data_choice} to get stats: \n", data_dict.keys())

    while confirm not in ('n', 'y') and feature not in data_dict.keys():
        if stat in ('correlation', 'all'):
            feature = input("Select data feature: ").strip().lower()
            correlate = input("Select data feature to correlate: ").strip().lower()
            if feature not in data_dict.keys():
                print(f"Sorry, try spell {feature} again.")
            if correlate not in data_dict.keys():
                print(f"Sorry, try spell {correlate} again.")
            confirm = input(f"You selected {feature} and {correlate}. Do you confirm your choice? (Yy/Nn): ")
        else:
            feature = input("Select data feature: ").strip().lower()
            column_view = input("Would you like to view the data? (Yy/Nn): ").lower()
            rows = len(data_dict.get(feature))
            lines = rows+1
            while column_view == 'y' and lines > rows:
                lines = int(input(f"Number of rows is {rows}. How many would you like to view: "))
                if lines < rows:
                    column_view == 'n'
                    for line in range(lines):
                        print(data_dict.get(feature)[line])
            confirm = input(f"You selected {feature}. Do you confirm your choice? (Yy/Nn): ")
            if feature not in str(data_dict.keys()):
                print("Sorry, try spell that again.")
            elif not isinstance(data_dict.get(feature)[0], (float, int, complex)):
                print(f"Try another data feature, {feature} isn't numeric.")



    if stat == 'mean':
        wk_seven.get_mean(data_dict.get(feature))
    elif stat == 'mean':
        wk_seven.get_mode(data_dict.get(feature))
    elif stat == 'median':
        wk_seven.get_median(data_dict.get(feature))
    elif stat == 'standard deviation':
        wk_seven.get_standard_deviation(data_dict.get(feature))
    elif stat == 'correlation':
        wk_seven.calc_correlation(data_dict.get(feature), data_dict.get(correlate))
    elif stat == 'all':
        wk_seven.get_mean(data_dict.get(feature))
        wk_seven.get_mode(data_dict.get(feature))
        wk_seven.get_median(data_dict.get(feature))
        wk_seven.get_standard_deviation(data_dict.get(feature))
        wk_seven.calc_correlation(data_dict.get(feature), data_dict.get(correlate))

    quit = ''
    while quit not in ('y', 'n'):
        quit = input("\nWould you like to end the program? (Yy/Nn): ").strip().lower()
