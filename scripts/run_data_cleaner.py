# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12

@author: Josh

Script to call functions from data_cleaner. This cleans the data from the cleaned csv files.
This is the second step to clean the data prior to analysis.

"""

from cleaner.csv_cleaner import save_dict
from cleaner.data_cleaner import fix_numerics, aggregate_columns, do_clean
from reader.data_reader import as_dictionary


def save_data(savepath, dataset):
    save = ''
    while save not in ('y', 'n'):
        save = input("Would you like to save the cleaned table? [Yy/Nn]: ")
        if save == 'y':
            save_dict(savepath, dataset)
            print("Data has been saved for future use! ")
        elif save == 'n':
            confirm = ''
            while confirm not in ('y', 'n'):
                confirm = input("Are you sure? This will save a lot of time in the future! [Yy/Nn]: ")
                if confirm == 'y':
                    save = 'n'
                else:
                    save = ''


def reuse_cleaned_data(filepath):
    stored_data = as_dictionary(filepath)
    print()
    if stored_data is None:
        print("Nothing saved from previous clean.")
    elif len(stored_data) > 0:
        print("There is previously cleaned data for this dataset.")
        print(f"There are {len(stored_data.keys())} columns with {len(stored_data.get(list(stored_data.keys())[0]))} columns each")
        use = ''
        while use not in ('n', 'y'):
            use = input("Do you want to use this dataset? [Yy/Nn] ").strip().lower()
            if use == 'y':
                return stored_data
            if use == 'n':
                return None


# File paths
rtb_file = "./data/rtb.csv"
rtb_clean = "./data/clean_rtb.csv"
airbnb_file = "./data/master_listings.csv"
airbnb_clean = "./data/clean_airbnb.csv"

# Clean the RTB data
clean_data = reuse_cleaned_data(rtb_clean)
if clean_data is not None:
    rtb = do_clean(rtb_clean, clean_data)
else:
    uncleaned_rtb = as_dictionary(rtb_file)
    uncleaned_rtb = fix_numerics(uncleaned_rtb)
    save_dict(rtb_clean, uncleaned_rtb)
    rtb = do_clean(rtb_clean, uncleaned_rtb)
save_data(rtb_clean, rtb)


# Clean the Airbnb data
clean_data = reuse_cleaned_data(airbnb_clean)
if clean_data is not None:
    airbnb = do_clean(airbnb_clean, clean_data)
else:
    unclean_airbnb = as_dictionary(airbnb_file)
    unclean_airbnb = fix_numerics(unclean_airbnb)
    unclean_airbnb = aggregate_columns(unclean_airbnb)
    save_dict(airbnb_clean, unclean_airbnb)
    airbnb = do_clean(airbnb_clean, unclean_airbnb)
save_data(airbnb_clean, airbnb)

