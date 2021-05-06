# File name: crawler.py
# Author: Deniz Aslan
# Date created: 15.04.2021
# Last modified: 06.05.2021
# Python Version: 3.9

import requests
import numpy as np
from bs4 import BeautifulSoup


def cases_death():
    """Scrape Covid data from worldometers,clean it and store it in a
    numpy array.
    """
    link = "https://bit.ly/3din7Bs"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    table_raw = soup.select("tr td")
    table_text = []
    for i in table_raw:
        table_text.append(i.get_text().replace(",", ""))
    table_text_array = np.array(table_text)
    formatted_array = np.reshape(table_text_array,
                                 (int(len(table_text) / 4), 4))

    # find MS Zaandam and remove from array
    zaandam_index = np.where(formatted_array == "MS Zaandam")
    covid_array = np.delete(formatted_array, zaandam_index[0][0], axis=0)

    # find Japan and fix its name
    japan_index = np.where(covid_array == "Japan (+Diamond Princess)")
    covid_array[japan_index[0][0]][0] = "Japan"

    return covid_array


def population():
    """Scrape population data from worldometers, clean it and store it
    in a numpy array.
    """
    link = "https://bit.ly/3lWkVDO"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    table_raw = soup.select("tr td")
    table_text = []
    for i in table_raw:
        table_text.append(i.get_text().replace(",", ""))
    table_text_array = np.array(table_text)
    formatted_array = np.reshape(table_text_array,
                                 (int(len(table_text) / 12), 12))
    population_array = formatted_array[:, [1, 2]]

    return population_array


def capital_coordinates():
    """Read the file worldcities.csv and store capital city coordinates
    into numpy array.
    """
    file = open("worldcities.csv", "r", encoding="utf8")
    lines = file.readlines()
    file.close()
    cities_list = []
    for line in lines[1:]:
        cities_list.append(line.split(","))
    capitals_list = []

    # remove countries with multiple capital cities
    multiple_capitals = ["The Hague", "Cotonou", "Bujumbura", "Dar es Salaam"
                         "Pretoria", "Bloemfontein", "Colombo"]
    for city in cities_list:
        if city[8] == "primary" and city[1] not in multiple_capitals:
            capitals_list.append(city)

    capitals_array = np.array(capitals_list)
    capitals_array[:, [0, 4]] = capitals_array[:, [4, 0]]
    capitals_array = capitals_array[:, 0:4]

    return capitals_array


def main():
    """Call cases_death(), population(), capital_coordinates(), merge
    the data into a single numpy array and write it on a csv file.
    """
    capitals_array = capital_coordinates()
    population_array = population()
    covid_array = cases_death()
    all_countries = []

    # make a list of all countries in the three arrays
    for array in [capitals_array, population_array, covid_array]:
        for country in array[:, 0]:
            if country not in all_countries:
                all_countries.append(country)

    # make a list of the countries common to all three arrays
    common_countries = []
    for country in all_countries:
        if country in capitals_array[:, 0] \
                and country in population_array[:, 0] \
                and country in covid_array[:, 0] \
                and country not in common_countries:
            common_countries.append(country)

    # create a country array, add countries and add header
    final_array = np.reshape(np.array(common_countries),
                             (len(common_countries), 1))
    empty_array = np.zeros((len(common_countries), 6), str)
    final_array = np.hstack((final_array, empty_array))
    header = ["Country", "Number of Covid cases", "Number of Covid deaths",
              "Region", "Population", "Latitude of capital",
              "Longitude of capital"]
    final_array = np.insert(final_array, 0, np.array(header), 0)

    # copy the data from the three arrays into one final array
    for country in common_countries:
        final_array[np.where(final_array == country)[0][0]][1:4] = \
            covid_array[np.where(covid_array == country)[0][0]][1:4]
        final_array[np.where(final_array == country)[0][0]][4] = \
            population_array[np.where(population_array == country)[0][0]][1]
        final_array[np.where(final_array == country)[0][0]][5:7] = \
            capitals_array[np.where(capitals_array == country)[0][0]][2:4]

    # save the final array into a csv file
    file = open("coronavirus_data.csv", "w", encoding="utf8")
    for row in final_array:
        for column in row:
            file.write(column)
            if column != row[-1]:
                file.write(",")
        file.write("\n")
    file.close()


if __name__ == "__main__":
    main()
