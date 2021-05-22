# File name: coronavirus_statistics.py
# Author: Deniz Aslan
# Date created: 26.04.2021
# Last modified: 22.05.2021
# Python Version: 3.9

import numpy as np


def read_data():
    """read coronavirus_data.csv and load the data into a
    numpy array.
    """
    covid_list = []
    file = open("coronavirus_data.csv", "r", encoding="utf8")
    lines = file.readlines()
    file.close()
    for line in lines[1:]:
        data = line.split(",")
        covid_list.append(data)
    covid_array = np.array(covid_list)

    return covid_array


def region_data():
    """read data from covid_array and return a 2D numpy array where
    each line contains a region, number of cases, number of deaths and
    population for that region.
    """
    covid_array = read_data()
    region_list = []
    for row in covid_array:
        if row[3] not in region_list:
            region_list.append(row[3])

    # create empty array and add regions as first column
    region_array = np.empty((6, 4), dtype=np.dtype('U20'))
    for index, row in enumerate(region_array):
        row[0] = region_list[index]

    # sum the data from each country and add into appropriate region
    n_cases = 0
    n_deaths = 0
    population = 0
    for region in region_list:
        for row in covid_array:
            if row[3] == region:
                n_cases += int(row[1])
                n_deaths += int(row[2])
                population += int(row[4])
        region_array[np.where(region_array == region)[0][0]][1] = n_cases
        region_array[np.where(region_array == region)[0][0]][2] = n_deaths
        region_array[np.where(region_array == region)[0][0]][3] = population

    return region_array


def country_data(countries=None):
    """receive a list of countries and return a 2D numpy array where
    each line contains: country, number of cases normalized by
    population, number of deaths normalized by population, population
    """
    covid_array = read_data()
    if countries is None:
        countries = np.ndarray.tolist(covid_array[:, 0])
    indexes = []
    if isinstance(countries, str):
        countries = countries.split(",")
    for index, row in enumerate(covid_array):
        if row[0] in countries:
            indexes.append(index)
    normalized_array = np.delete(covid_array[indexes], [3, 5, 6], 1)

    # divide by population to normalize number of cases and deaths
    for row in normalized_array:
        row[1] = str(int(row[1]) / int(row[3]))
        row[2] = str(int(row[2]) / int(row[3]))

    return normalized_array


def top_country_data(k, n=0):
    """receive two integers, k and n and return a 2D numpy array that
    contains k lines of the format country, number of deaths normalized
    by population, latitude and longitude. The countries are the subset
    of the countries with population size at least n that have the
    highest number of deaths normalized by population.
    """
    trimmed_array = np.delete(read_data(), [1, 3], 1)
    indexes = []

    # find rows with population >= n and delete the rest, using indexes
    for index, row in enumerate(trimmed_array):
        if not int(row[2]) >= n:
            indexes.append(index)
    trimmed_array = np.delete(trimmed_array, indexes, 0)

    # divide by population then remove population column
    for row in trimmed_array:
        row[1] = int(row[1]) / int(row[2])
    trimmed_array = np.delete(trimmed_array, [2], 1)

    # sort rows by normalized death rate and select first k rows
    trimmed_array = trimmed_array[np.argsort(
        -trimmed_array[:, 1].astype(float))]
    trimmed_array = trimmed_array[:k]

    return trimmed_array
