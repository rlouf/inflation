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


if __name__ == "__main__":
    conn = sqlite3.connect("us-prices.db")
    read_areas(conn, "data/raw/ap.area")
    read_items(conn, "data/raw/ap.series")
