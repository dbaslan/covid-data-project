import requests
import numpy as np
from bs4 import BeautifulSoup


def cases_death():
    """Scrape Covid data from worldometers, clean it and store it in a numpy array"""
    link = "https://bit.ly/3din7Bs"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_raw = soup.select("tr td")
    table_text = []
    for i in table_raw:
        table_text.append(i.get_text().replace(",", ""))
    table_text_array = np.array(table_text)
    formatted_array = np.reshape(table_text_array, (int(len(table_text) / 4), 4))
    zaandam_index = np.where(formatted_array == "MS Zaandam")
    formatted_array = np.delete(formatted_array, zaandam_index[0][0], axis=0)
    Japan_index = np.where(formatted_array == "Japan (+Diamond Princess)")
    formatted_array[Japan_index[0][0]][0] = "Japan"
    return formatted_array


def population():
    """Scrape population data from worldometers, clean it and store it in a numpy array"""
    link = "https://bit.ly/3lWkVDO"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_raw = soup.select("tr td")
    table_text = []
    for i in table_raw:
        table_text.append(i.get_text().replace(",", ""))
    table_text_array = np.array(table_text)
    formatted_array = np.reshape(table_text_array, (int(len(table_text) / 12), 12))
    formatted_array = formatted_array[:, [1, 2]]
    return formatted_array


def capital_coordinates():
    """Read the file worldcities.csv and store capital city coordinates into numpy array"""
    file = open("worldcities.csv", "r", encoding="utf8")
    lines = file.readlines()
    file.close()
    cities_list = []
    for line in lines[1:]:
        cities_list.append(line.split(","))
    capitals_list = []
    for city in cities_list:
        if city[8] == "primary":
            capitals_list.append(city)
    capitals_array = np.array(capitals_list)
    capitals_array = capitals_array[:, 1:4]
    return capitals_array

def main():
    file = open("coronavirus_data.csv", "w", encoding="utf8")
    for i in range(4):
        file.write("lol")
    file.close()