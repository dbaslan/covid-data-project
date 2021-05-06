import coronavirus_statistics as cs
import numpy as np
import matplotlib.pyplot as plt


def regions_piechart(region, show=False):
    """receive a region, draw a piechart of coronavirus deaths and
    recoveries in the region and save it as region_piechart.png under
    /graphs
    """
    region_array = cs.region_data()
    index = np.where(region_array == region)[0][0]
    n_deaths = int(region_array[index, 2])
    n_recovered = int(region_array[index, 1]) - n_deaths

    plt.figure(figsize=(6, 6))
    labels = "dead", "recovered"
    fractions = [n_deaths, n_recovered]
    plt.pie(fractions, labels=labels, autopct="%1.1f%%")
    plt.title(f"Fraction of COVID-19 patients in {region} who died")
    plt.savefig("graphs/region_piechart.png")
    if show:
        plt.show()


def countries_barchart(show=False):
    """hello
    """


def highest_mortality(n, k, show=False):
    """
    """


def map(k, show=False):
    """
    """


def main():
    """
    """


if __name__ == "__main__":
    main()
