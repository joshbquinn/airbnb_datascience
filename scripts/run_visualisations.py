# -*- coding: utf-8 -*-
"""
Created on Tue Dec  13

@author: Josh

Python script to run further analysis and visualisations functions.
"""
from reader import data_reader
from analyser import stats
from reader.data_reader import combine_data_if_key_contains
from analyser.visualiser import plot_bar_pie, plot_line


def south_north_dublin(dataset):
    knownareas = []
    south_dublin = {}
    north_dublin = {}
    for post_code in range(1, 28):
        for location, listings in dataset.items():
            if str(post_code) in location:
                knownareas.append(location)
            if post_code % 2 == 0:
                south_dublin.update(
                    combine_data_if_key_contains(post_code, location, listings, south_dublin, post_code, 'D'))
            else:
                north_dublin.update(
                    combine_data_if_key_contains(post_code, location, listings, north_dublin, post_code, 'D'))

    return south_dublin, north_dublin, knownareas


data = data_reader.as_dictionary('./data/clean_rtb.csv')
headers = data_reader.get_headers('./data/clean_rtb.csv')
rows = data_reader.transpose_to_rows(data)

listings_grouped_by_location = stats.group_by_rows(headers, rows, 'location', 'location', )
listings_by_location = stats.sum_grouped_string_feature(listings_grouped_by_location)
south_dublin_listings, north_dublin_listings, known_areas = south_north_dublin(listings_by_location)

try:
    listings_by_location = dict({(k, v) for (k, v) in listings_by_location.items() if k not in known_areas})
except KeyError as e:
    print("KeyError", e)

plot_bar_pie(stats.sum_grouped_feature(south_dublin_listings), 'RTB listings in S. Dublin by Post Code, Q1 2019', 'Area', 'Number of Listings',
             './data/plots/listings_s_dublin_rtb.png', False)
plot_bar_pie(stats.sum_grouped_feature(north_dublin_listings), 'RTB listings in N. Dublin by Post Code, Q1 2019', 'Area', 'Number of Listings',
             './data/plots/listings_n_dublin_rtb.png', False)
plot_bar_pie(listings_by_location, 'RTB listings in Dublin without Post Code data, Q1 2019', 'Area',
             'Number of Listings', './data/plots/listings_dublin_rtb.png', False)


prices_grouped_by_area = stats.group_by_rows(headers, rows, "price_19q1", "location")
avg_prices_grouped_by_area = stats.calc_feature_average(prices_grouped_by_area)
south_dublin_prices, north_dublin_prices, known_areas = south_north_dublin(avg_prices_grouped_by_area)
try:
    avg_prices_grouped_by_area = dict({(k, v) for (k, v) in avg_prices_grouped_by_area.items() if k not in known_areas})
except KeyError as e:
    print("KeyError", e)


plot_line(stats.calc_feature_average(south_dublin_prices), "Average RTB prices in S Dublin, Q1 2019", "Area", "Price", 's_dublin_rtb.png', False)
plot_line(stats.calc_feature_average(north_dublin_prices), "Average RTB prices in N Dublin, Q1 2019", "Area", "Price", 'n_dublin_rtb.png', False)
plot_line(avg_prices_grouped_by_area, "Average RTB prices in N Dublin, Q1 2019", "Area", "Price", 'n_dublin_rtb.png', False)
