# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6

@author: Josh

Python file to interact with user and report analysis on cleaned data files

"""

from analyser import stats
from reader.data_reader import as_dictionary


def do_analysis(stat, feature, correlate):
    if stat == 'mean':
        mean = stats.get_mean(data_dict.get(feature))
        print(f"Mean is: {mean}")
    elif stat == 'mode':
        mode, mode_element = stats.get_mode(data_dict.get(feature))
        print(f"Mode is {mode_element} with {mode} occurrences")
    elif stat == 'median':
        median = stats.get_median(data_dict.get(feature))
        print(f"Median is: {median:.2f}")
    elif stat == 'standard deviation':
        std_deviation = stats.get_standard_deviation(data_dict.get(feature))
        print("The standard deviation is: ", std_deviation)
    elif stat == 'correlation':
        correlation = stats.calc_correlation(data_dict.get(feature), data_dict.get(correlate))
        print("The Correlation between two lists is: ", correlation)
    elif stat == 'all':
        mode, mode_element = stats.get_mode(data_dict.get(feature))
        mean = stats.get_mean(data_dict.get(feature))
        median = stats.get_median(data_dict.get(feature))
        std_deviation = stats.get_standard_deviation(data_dict.get(feature))
        correlation = stats.calc_correlation(data_dict.get(feature), data_dict.get(correlate))
        print(f"Mode is {mode_element} with {mode} occurrences")
        print(f"Mean is: {mean}")
        print(f"Median is: {median:.2f}")
        print("The standard deviation is: ", std_deviation)
        print("The Correlation between two lists is: ", correlation)


airbnb_file = "./data/clean_airbnb.csv"
rtb_file = "./data/clean_rtb.csv"

airbnb = as_dictionary(airbnb_file)
rtb = as_dictionary(rtb_file)

quit = ''
print("\n\nOk, data sets are stored in memory. ")
while quit != 'y':
    try:
        view = ""
        while view not in ("y", "n"):
            view = input("\nView available columns for both sets? (Yy/Nn): ").lower()

        if view == 'y':
            print("Airbnb: \n", list(airbnb.keys()))
            print("Rent Tenancy board: \n", list(rtb.keys()))

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
        print(f"\nChoose feature from {data_choice} to get stats: \n", list(data_dict.keys()))

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
                lines = rows + 1
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

        do_analysis(stat, feature, correlate)
    except KeyboardInterrupt as e:
        print("There was a key board interrupt: ", e)
    quit = ''
    while quit not in ('y', 'n'):
        quit = input("\nWould you like to end analysis? (Yy/Nn): ").strip().lower()
