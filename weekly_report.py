"""The Greenway Food Truck's weekly report: six functions for you to finish.

The docstring under each function says what it should do, with examples. Replace each
raise NotImplementedError("Not built yet.") line with your own code.

Run the finished report with:
    python weekly_report.py
or, with your own folders:
    python weekly_report.py --data data/incoming --out reports
"""
import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def newest_week_file(folder):
    """Return the Path of the newest week-*.csv file in folder (a str or a Path).

    The files are named by the Monday their week starts on, year first, so sorting the names
    puts them in date order and the last one is the newest:
    week-2026-09-07.csv, week-2026-09-14.csv, ... week-2026-10-26.csv -> week-2026-10-26.csv

    If folder holds no week-*.csv file, raise FileNotFoundError with a message that names the
    folder, for example: No week-*.csv file in data/incoming
    """
    raise NotImplementedError("Not built yet.")


def load_week(path):
    """Read one week's sales file into a DataFrame, and add a total column.

    sold_at is read as dates and times (datetime64), not text, and total is each sale's
    quantity times its price:
    quantity 2, price 9.00 -> total 18.0
    """
    raise NotImplementedError("Not built yet.")


def summarize(df):
    """Return a dictionary of the week's four headline numbers, from a table load_week made.

    {"sales": the sum of total, rounded to 2 decimal places,
     "items_sold": the sum of quantity, as an int,
     "best_item": the item with the largest quantity sold,
     "best_location": the location with the largest sum of total}

    When two items (or two locations) tie, the one that comes first alphabetically wins.
    Three sales, Elote x1 at City Park ($4.50), Street Tacos x2 at Stadium ($18.00) and
    Elote x2 at City Park ($9.00), give:
    {"sales": 31.5, "items_sold": 5, "best_item": "Elote", "best_location": "Stadium"}
    """
    raise NotImplementedError("Not built yet.")


def items_chart(df):
    """Return (fig, ax): a bar chart of how many of each item sold, largest first.

    One bar per item, its height the item's total quantity, sorted from the most sold to the
    least. Title: Items sold this week. X-axis label: Item. Y-axis label: Number sold.
    """
    raise NotImplementedError("Not built yet.")


def write_report(df, out_dir):
    """Write the week's report into out_dir (a str or a Path) and return the Path of report.html.

    Make out_dir if it isn't there (and any folders above it). Write two files into it:
    - items.png: the chart items_chart(df) makes, saved with savefig, and the figure closed.
    - report.html: a web page with the four numbers from summarize(df), the chart, and a
      table of sales by location. For the seeded week-2026-10-26.csv, the page's text
      includes these five lines exactly:
        Sales: $4,455.00
        Items sold: 537
        Best-selling item: Street Tacos
        Best location: Stadium
        <img src="items.png" alt="Bar chart of the number of each item sold this week">
      The sales have a dollar sign, a comma between thousands and 2 decimal places
      (16543.5 -> $16,543.50), and the items sold a comma between thousands (1402 -> 1,402).
      Then the table that to_html(index=False) makes from a DataFrame with the columns
      location and sales (each location's sum of total), largest sales first.
    """
    raise NotImplementedError("Not built yet.")


def main(argv):
    """Build the report for the newest week, from the command line's words in argv (a list).

    Options: --data, the folder of week files (default data/incoming), and --out, the folder the
    reports go in (default reports). The report goes in a folder of its own inside --out, named
    by the week's date from the file name: week-2026-10-26.csv -> reports/2026-10-26/

    Then print, one line each (these are the seeded week-2026-10-26.csv's):
        1) week: 2026-10-26
        2) sales: 4455.0
        3) items sold: 537
        4) best-selling item: Street Tacos
        5) best location: Stadium
        6) report: reports/2026-10-26/report.html
    (line 6 is the Path write_report returned). Return that Path too.
    """
    raise NotImplementedError("Not built yet.")


if __name__ == "__main__":
    main(sys.argv[1:])
