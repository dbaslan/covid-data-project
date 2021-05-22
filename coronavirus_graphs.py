# File name: coronavirus_graphs.py
# Author: Deniz Aslan
# Date created: 06.05.2021
# Last modified: 22.05.2021
# Python Version: 3.9

import coronavirus_statistics as cs
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def regions_piechart(region, show=False):
    """receive a region, draw a piechart of coronavirus deaths and
    recoveries in the region and save it as region_piechart.png under
    /graphs
    """
    region_array = cs.region_data()
    index = np.where(region_array == region)[0][0]
    n_deaths = int(region_array[index, 2])
    n_recovered = int(region_array[index, 1]) - n_deaths

    # visualize as pie chart and save:
    plt.figure(figsize=(6, 6))
    labels = "dead", "recovered"
    fractions = [n_deaths, n_recovered]
    plt.pie(fractions, labels=labels, autopct="%1.1f%%")
    plt.title(f"Fraction of COVID-19 patients in {region} who died")
    plt.savefig("graphs/region_piechart.png")
    if show:
        plt.show()


def countries_barchart(countries=None, show=False):
    """receive list of countries, draw two bar charts showing their number of
    cases and deaths and save it as countries_barchart.png under /graphs
    """
    bar_array = cs.country_data(countries)

    # multiply by a million:
    for row in bar_array:
        row[1] = str(float(row[1]) * 1000000)
        row[2] = str(float(row[2]) * 1000000)

    # visualize as two bar charts and save:
    plt.subplot(2, 1, 1)
    plt.bar(bar_array[:, 0], bar_array[:, 1].astype(float))
    if len(bar_array) > 6:
        plt.xticks(rotation="vertical")
    plt.xlabel("Country")
    plt.ylabel("Cases per 1 Million")
    plt.title("Covid Cases & Deaths Per 1 Million, By Country")
    plt.grid()
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.bar(bar_array[:, 0], bar_array[:, 2].astype(float))
    if len(bar_array) > 6:
        plt.xticks(rotation="vertical")
    plt.xlabel("Country")
    plt.ylabel("Deaths per 1 Million")
    plt.grid()
    plt.tight_layout()
    plt.savefig("graphs/countries_barchart.png")
    if show:
        plt.show()


def highest_mortality(k, n=0, show=False):
    """receive integers k, n and draw a bar chart of k countries with
    the highest normalized deaths with n minimum population, and save
    it as top_countries_barchart.png under /graphs
    """
    trimmed_array = cs.top_country_data(k, n)

    # visualize as br chart and save:
    plt.bar(trimmed_array[:, 0], trimmed_array[:, 1].astype(float) * 1000000)
    if len(trimmed_array) > 6:
        plt.xticks(rotation="vertical")
    plt.xlabel("Country")
    plt.ylabel("Deaths per 1 Million")
    plt.title("Covid Deaths Per 1 Million, By Country")
    plt.grid()
    plt.tight_layout()
    plt.savefig("graphs/top_countries_barchart.png")
    if show:
        plt.show()


def map(k, show=False):
    """receive integer k, mark k countries with highest number of
    normalized deaths on a map and save it as top_countries_map.png
    under /graphs
    """
    trimmed_array = cs.top_country_data(k)

    # visualize as map and save:
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.plot(trimmed_array[:, 3].astype(float),
            trimmed_array[:, 2].astype(float),
            "ro", markersize=2, transform=ccrs.Geodetic())
    plt.title(f"Top {k} Countries With Highest Rates Of Covid-19 Deaths, "
              f"Normalized By Population")
    plt.tight_layout()
    plt.savefig("graphs/top_countries_map.png", bbox_inches="tight")
    if show:
        plt.show()


def main():
    """Ask user for input, choose which function to use for visualizing data,
    continue as prompted, exit as prompted
    """
    choice_1 = choice_2 = choice_3 = ask_show = cont = region = None
    regions = ["Asia", "Africa", "Europe", "North America",
               "South America", "Australia/Oceania"]

    while choice_1 not in ["yes", "no", "y", "n"]:
        choice_1 = input("Would you like to study global Covid-19 "
                         "data? Type yes or no.")

    if choice_1 in ["no", "n"]:
        print("Okay, goodbye.")
        exit()
    else:
        while choice_2 not in ["1", "2", "3", "4"]:
            choice_2 = input("Please pick an option by typing its number: "
                             "\n1. Pick a region and visualize the ratio of "
                             "Covid infections and deaths. \n2. Pick a few "
                             "countries and visualize the number of Covid "
                             "cases and deaths per 1 million. \n3. Pick a "
                             "number of countries with the highest ratio of "
                             "Covid deaths per 1 million and visualize the "
                             "deaths. \n4. Pick a number of countries with "
                             "the highest ratio of Covid deaths "
                             "normalized by population and visualize them on "
                             "a map.")

    if choice_2 == "1":
        while region not in regions:
            region = input("Please pick a continent (Australia/Oceania, "
                           "Africa, North America, South America, Europe, "
                           "Asia:")
        while ask_show not in ["yes", "no", "y", "n"]:
            ask_show = input("Would you like to view the chart? (yes/no)")
        if ask_show in ["yes", "y"]:
            regions_piechart(region, True)
        else:
            regions_piechart(region)
        while cont not in ["yes", "no", "y", "n"]:
            cont = input("Would you like to continue? (yes/no)")
        if cont in ["yes", "y"]:
            main()
        else:
            print("Okay, goodbye.")
            exit()
    elif choice_2 == "2":
        countries = input("Please provide a list of countries, "
                          "separated by commas. e.g. Japan,Hungary,Turkey. "
                          "Leave empty to select all:")
        while ask_show not in ["yes", "no", "y", "n"]:
            ask_show = input("Would you like to view the chart? "
                             "(yes/no)")
        if countries == "":
            if ask_show in ["yes", "y"]:
                countries_barchart(None, True)
            else:
                countries_barchart(None)
        else:
            if ask_show in ["yes", "y"]:
                countries_barchart(countries, True)
            else:
                countries_barchart(countries)
        while cont not in ["yes", "no", "y", "n"]:
            cont = input("Would you like to continue? (yes/no)")
        if cont in ["yes", "y"]:
            main()
        else:
            print("Okay, goodbye.")
            exit()
    elif choice_2 == "3":
        n_countries = input("Please provide the number of countries "
                            "you would like to include:")
        while ask_show not in ["yes", "no", "y", "n"]:
            ask_show = input("Would you like to view the chart? (yes/no)")
        while choice_3 not in ["yes", "no", "y", "n"]:
            choice_3 = input("Would you lke to specify a minimum number "
                             "for the population? (yes/no)")
        if choice_3 in ["yes", "y"]:
            mini_pop = input("Please provide a number for the minimum "
                             "population:")
            if mini_pop == "":
                mini_pop = 0
            if ask_show in ["yes", "y"]:
                highest_mortality(int(n_countries), int(mini_pop), True)
            else:
                highest_mortality(int(n_countries), int(mini_pop))
        else:
            if ask_show in ["yes", "y"]:
                highest_mortality(int(n_countries), show=True)
            else:
                highest_mortality(int(n_countries))
        while cont not in ["yes", "no", "y", "n"]:
            cont = input("Would you like to continue? (yes/no)")
        if cont in ["yes", "y"]:
            main()
        else:
            print("Okay, goodbye.")
            exit()
    elif choice_2 == "4":
        n_countries = input("Please provide the number of countries you "
                            "would like to include:")
        while ask_show not in ["yes", "no", "y", "n"]:
            ask_show = input("Would you like to view the chart? (yes/no)")
        if ask_show in ["yes", "y"]:
            map(int(n_countries), True)
        else:
            map(int(n_countries))
        while cont not in ["yes", "no", "y", "n"]:
            cont = input("Would you like to continue? (yes/no)")
        if cont in ["yes", "y"]:
            main()
        else:
            print("Okay, goodbye.")
            exit()


if __name__ == "__main__":
    main()
