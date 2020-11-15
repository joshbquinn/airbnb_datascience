# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13
@author: Josh

Functions to plot the cleaned data.

"""

import matplotlib.pyplot as plt

from reader.data_reader import sort_keys


def plot_pie(data, title, savepath, save):
    """Plots a pie chart

    Args:
        data:
        title:
        savepath:
        save:
    """
    data = sort_keys(data)

    fig, ax = plt.subplots(figsize=(20, 20))

    ax.set_title(title)

    ax.pie(data.values(), labels=data.keys(), autopct="%.0f%%")
    plt.show()

    if save is True:
        fig.savefig(savepath, bbox_inches='tight')
        print(f"Saved the chart to '{savepath}'")


def plot_bar_pie(data, title, yaxis, xaxis, savepath, save):
    """Plots a bar chart combined with a pie chart

    Args:
        data:
        title:
        yaxis:
        xaxis:
        savepath:
        save:

    """
    data = sort_keys(data)

    fig, ax = plt.subplots(2, figsize=(15, 15))

    fig.suptitle(title)

    y_pos = [i for i in range(len(data))]

    ax[0].set_yticks(y_pos)
    ax[0].set_yticklabels(data.keys())

    ax[0].set_ylabel(yaxis)
    ax[0].set_xlabel(xaxis)

    ax[0].barh(y_pos, data.values(), align='center')
    ax[1].pie(data.values(), labels=data.keys())

    plt.show()

    if save is True:
        # save the bar chart
        fig.savefig(savepath, bbox_inches='tight')
        print(f"Saved the chart to '{savepath}'")


def plot_line(data, title, yaxis, xaxis, savepath, save):
    """Plots a line chart

    Args:
        data:
        title:
        yaxis:
        xaxis:
        savepath:
        save:
    """
    data = sort_keys(data)
    fig, ax = plt.subplots(figsize=(15, 15))

    ax.set_title(title)

    ax.set_ylabel(yaxis)
    ax.set_xlabel(xaxis)

    ax.plot(list(data.keys()), list(data.values()))
    ax.plot(fmt="go--", data=data)

    plt.show()

    if save is True:
        fig.savefig(savepath)
        print(f"Saved the chart to '{savepath}'")
