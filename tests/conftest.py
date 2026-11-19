# Shared set-up for the tests. You don't need to change this file.
# Charts are drawn with matplotlib's Agg backend, which draws into memory and never opens a window,
# so the tests can read each chart's title, labels and bars without showing it.
# Each test that asks for data_folder gets its own fresh copy of the eight weeks of sales, made by
# seed.py in a temporary folder, so the tests check your code against the same data even if you
# changed the files in data/incoming.
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from seed import write_weeks


@pytest.fixture
def data_folder(tmp_path):
    """A temporary data/incoming folder holding the eight seeded weeks, week-2026-09-07.csv to week-2026-10-26.csv."""
    folder = tmp_path / "data" / "incoming"
    write_weeks(folder)
    return folder


@pytest.fixture(autouse=True)
def close_charts():
    """Closes every open chart before and after each test, so one test's charts never reach the next."""
    plt.close("all")
    yield
    plt.close("all")
