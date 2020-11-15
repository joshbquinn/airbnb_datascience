# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6

@author: Josh

Python script to run the csv_cleaner functions.
This script is the first step to clean the csv files.

"""
import os
from cleaner import csv_cleaner, data_cleaner
from reader import data_reader

clean_dir = "./data/clean/"
unclean_dir = "./data/unclean/"
csv_files = os.listdir(unclean_dir)
initial_table = csv_cleaner.load_dict(unclean_dir + csv_files[0])
wanted_columns = csv_cleaner.choose_columns(initial_table)
total_columns_num = len(initial_table.keys())

print("\nInitial cleanup - cleaning individual csv files before aggregating.")
print(f"There are {len(csv_files)} csv files to combine each with {total_columns_num} columns.")
print(f"Loading all csv files, removing {total_columns_num - len(wanted_columns)} columns from each, "
      f"removing unknown characters '�', and writing back to file.\n")

for largest_file in csv_files:
    read_path = unclean_dir + largest_file
    write_path = clean_dir + largest_file

    print(f"1. Uncleaned csv file loaded from '{read_path}'")
    uncleaned_csv_dict = csv_cleaner.load_dict(read_path)

    print("2. Unwanted columns removed")
    clean_csv_dict = csv_cleaner.remove_unwanted_columns(uncleaned_csv_dict, wanted_columns)

    print(f"3. Selected csv data written to new csv file '{write_path}'.")
    print("4. Printing the cleaned dictionary to new csv file.")
    csv_cleaner.save_dict(write_path, clean_csv_dict)
    print("5. Finished writing cleaned dictionary to file\n")

print("6. All refined csv data written to files\n")

print("7. Loading the largest clean airbnb listings csv file to compare the other airbnb listings against."
      "\nWe can append prices for each month over two years from all the csv's into this 'master' csv, where ids Match."
      "\nIf a master ID is not in any other CSV file, we append a ZERO for that month, denoting that it "
      "was not listed that month.")

index, largest_file = csv_cleaner.find_largest_table(csv_files)
print("The file with most rows is ", largest_file)
master_list = csv_cleaner.load_rows(clean_dir + largest_file)
csv_files.pop(index)

print("\n8. Loading all the clean csv files into a list of rows. Removing any rows where the length is incorrect.")
combined_tables = []
for name in csv_files:
    print()
    table = csv_cleaner.load_rows(clean_dir + name)
    print("Checking", name)
    rows_before = len(table)
    table = [row for row in table if len(row) == len(wanted_columns)]
    rows_after = len(table)
    print(f"{rows_before - rows_after} rows with incorrect number of columns removed.", )
    combined_tables.append((name, table))

print("\n9. Compare the Master CSV file against all the others. "
      "\nAppend a new column to master for the year.month price."
      "\nIterate through each csv file. Iterate through each master ROW. "
      "\nIf the master ROW's ID is not in the csv file we're comparing against. Append a zero for that month."
      "\n ")
indexed_columns = data_reader.index_columns(wanted_columns)
master_list[0][indexed_columns.get("price")] = "price_" + largest_file.replace(".csv", "").replace("listings", "")
clean_csv_dict = data_cleaner.append_price_column(master_list, combined_tables, indexed_columns)
csv_cleaner.write("./data/master_listings.csv", clean_csv_dict)
print("10. Appended price columns and written to single file '/data/master_listings.csv'.")
