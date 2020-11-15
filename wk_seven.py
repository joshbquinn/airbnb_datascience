''' Exercise 1 '''
import sys


def hello():
    print("hello world")


'''Exercise 2'''


def address(house, street, town, county):
    print(house + ",\n" + street + ",\n" + town + ",\n" + county)


'''Exercise 3'''


def print_name(name):
    print("Your name is ", name)


# name = input("What's your name?")
# print_name(name)

'''Exercise 4'''


def draw_char(char, num):
    print(char * num)


# char = input("Enter a char to draw")
# num = int(input("How many times do you want to draw it?"))
# draw_char(char, num)

'''Exercise 5'''


def disk_space_calc(total, used, min_acceptable):
    free = float((total - used) / total * 100)
    print(f"Total free: {free:.1f}%")
    if free < min_acceptable:
        print("Not sufficient space")
    else:
        print("Sufficient space")


# total = int(input("Enter total disk space: "))
# used = int(input("Enter used disk space: "))
# min_acceptable = int(input("Enter mnimum allowed"))
# disk_space_calc(total, used, min_acceptable)

'''
Exercise 6
'''


def calc_download_time(speed, size):
    time = (size * 8.388608) / speed
    print(f'Download time is {time:.2f} secs')


# connection_speed = float(input("Enter the connection speed in Mbps: "))
# filesize = float("Enter th efile size in MB: ")
# calc_download_time(connection_speed, filesize)

'''
Exercise 7
'''


def count_letters(string):
    count = 0
    for l in string:
        if l.isalpha():
            count += 1

    print(f"Number of letters in string is {count}.")


# string = input("Enter a sentence or phrase: ")
# count_letters(string)

'''Exercise 8'''


def calc_area_and_perim(length, width):
    area = float(length) * float(width)
    perimeter = 2 * float(length) + float(width)
    print(f"Area is {area} and perimeter is {perimeter}")


# w = int(input("Enter the width"))
# l = int(input("Enter the length"))
# calc_area_and_perim(l, w)

'''
9.Surface Area and Volume of a Cylinder
'''


def calc_surf_area_volume(radius, height):
    pi = 14159
    surf_area = (2 * pi) * (radius ** 2) + (2 * pi) * (radius * height)
    volume = 3.14 * (radius ** 2) * height
    print(f"The surface is {surf_area:.2f} and the volume is {volume:.2f}.")


# r = int(input("Enter the radius: "))
# h = int(input("Enter the height: "))
# calc_surf_area_volume(r, h)

'''
10.Networking Calculations: Latency
'''


def calc_latency(frame_size, bit_rate, network_load):
    store_forward_latency = frame_size / bit_rate
    queuing_latency = network_load * store_forward_latency
    print(f"Store and Forward Latency is: {store_forward_latency} secs")
    print(f"Queuing Latency is : {queuing_latency} secs")


# fs = int(input("Enter the frame size: "))
# br = int(input("Enter the bit rate: "))
# nl = float(input("Enter the network load: "))
# calc_latency(fs, br, nl)

'''
11.Networking Calculations: Frequency Modulation
'''


def calc_freq_modulation(peak_freq_deviation, max_freq):
    modulation_index = peak_freq_deviation / max_freq
    bandwidth_requirement = 2 * (peak_freq_deviation + max_freq)
    print("Module Index is: ", modulation_index)
    print("Badnwidth Reqirement is: ", bandwidth_requirement)


# peak_freq_deviation = int(input("Enter the peak frequency deviation: "))
# max_freq = int(input("Enter the max frequency: "))

'''
12.Mean (Average)
'''


def get_mean(nums_mean):
    total_mean = 0
    if len(nums_mean) == 0:
        print(f"Mean is : {None}")
    try:
        for n in nums_mean:
            total_mean += n

        mean = float(total_mean) / len(nums_mean)
        print(f"Mean is: {mean:.2f}")
        return mean
    except (ZeroDivisionError, TypeError):
        print(f"We got an error in the list...{nums_mean}", sys.exc_info()[0], )


# nums = [int(x) for x in input("Eneter a list of numbers seperated by space: ").split()]
# get_mean(nums)
# string_list = ['hi', 'there']
# get_mean(string_list)

'''
13.Check if the list elements are all numbers
'''


def check_list_for_nums_and_size(nums_boolean):
    if len(nums_boolean) < 1:
        print("List has zero values")
        return False
    list_boolean = [type(x) == int or type(x) == float for x in nums_boolean]
    if all(list_boolean) is False:
        "List contains non-numeric values."
    return all(list_boolean)


# list_True = [1, 2, 3, 45, 6]
# check_list_for_nums_and_size(list_True)
# list_False = [1, 2, 3, "5"]
# check_list_for_nums_and_size(list_False)


'''
14.Median
'''


def get_median(nums_median):
    if len(nums_median) == 0 or check_list_for_nums_and_size(nums_median) is False:
        print(f"Mean is : {None}")
    else:
        nums_median = sorted(nums_median)
        if len(nums_median) % 2 != 0:
            index = ((len(nums_median) -1) / 2)
            median = nums_median[int(index)]
            print(f"Median is: {median:.1f}")
        else:
            middle_two = nums_median[int(((len(nums_median) / 2)) -1)] + nums_median[int((len(nums_median) / 2))]
            median = middle_two / 2
            print(f"Median is: {median:.1f}")
        return median


# nums = [int(x) for x in input("Enter an odd number of numbers separated by space: ").split()]
# get_mean(nums)
# string_list = ['hi', 'there']
# get_mean(string_list)
# nums2 = [int(x) for x in input("Enter an even number of numbers separated by space: ").split()]
# get_mean(nums2)


'''
15.Mode/Most Common Value
'''


def get_mode(list_mode):
    mode_element = ''
    mode = 0
    if check_list_for_nums_and_size(list_mode) is False:
        return None
    else:
        for element in list_mode:
            if list_mode.count(element) > mode:
                mode = list_mode.count(element)
                mode_element = element

        print(f"Mode is {mode_element} with {mode} occurrences")
        return mode


'''
16.Standard Deviation
'''


def get_standard_deviation(nums_std_dev):
    if check_list_for_nums_and_size(nums_std_dev) is False:
        return None
    else:
        summed_squares = 0
        mean = get_mean(nums_std_dev)
        for number_std in nums_std_dev:
            summed_squares += (number_std - mean) ** 2
        summed_squared_mean = summed_squares / len(nums_std_dev)
        std_deviation = summed_squared_mean ** 0.5
        print("The standard deviation is: ", std_deviation)
        return std_deviation


'''
17.Correlation
'''


def calc_correlation(nums_corr_1, nums_corr_2):
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
        print("The Correlation between two lists is: ", correlation)
        return correlation
