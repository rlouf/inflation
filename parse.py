""" Parse the data obtained from the U.S. Bureau of Labour statistics.
"""
import csv
import sqlite3


def read_areas(conn, path):
    with open(path, "r") as datafile:
        reader = csv.reader(datafile, delimiter="\t")
        reader.__next__()  # skip column name
        with conn:
            conn.executemany("INSERT OR IGNORE INTO areas VALUES(?,?);", reader)


def read_items(conn, path):
    with open(path, "r") as datafile:
        reader = csv.reader(datafile, delimiter="\t")
        reader.__next__()  # skip column name
        items = [(row[2], row[3]) for row in reader]
        with conn:
            conn.executemany("INSERT OR IGNORE INTO items VALUES(?,?);", items)


def read_series(conn, path_prices, path_series):

    # We first read the mapping series_id -> (area_id, item_id)
    with open(path_series, "r") as datafile:
        reader = csv.reader(datafile, delimiter="\t")
        reader.__next__()  # skip column name
        items = {row[0]: (row[1], row[2]) for row in reader}

    # We then read all the prices
    with open(path_prices, "r") as datafile:
        reader = csv.reader(datafile, delimiter="\t")
        reader.__next__()  # skip column name

        convert_value = lambda entry: None if "-" in entry else float(entry.lstrip())
        prices = [
            (row[0].rstrip(),)
            + items[row[0]]
            + (
                int(row[1]),
                int(row[2].replace("M", "")),
                convert_value(row[3]),
            )
            for row in reader
        ]
        with conn:
            conn.executemany(
                "INSERT OR IGNORE INTO series VALUES(?,?,?,?,?,?);", prices
            )


if __name__ == "__main__":
    conn = sqlite3.connect("us-prices.db")
    read_areas(conn, "data/raw/ap.area")
    read_items(conn, "data/raw/ap.series")
    read_series(conn, "data/raw/ap.data.0.Current", "data/raw/ap.series")
