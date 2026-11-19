# Tests for weekly_report.py. Run them with: python -m pytest (in the exercise folder, with the virtual environment active).
# Each test calls one of your functions, on the weeks seed.py makes (in a temporary folder) or on a small table or
# folder written in the test, and checks what comes back or the files it wrote. A failing test says what it called,
# what it expected and what came back. You don't need to change this file.
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from seed import write_next_week
from weekly_report import items_chart, load_week, main, newest_week_file, summarize, write_report


def check(call, got, expected):
    """Fails with a message that says what the call returned and what it should return."""
    assert got == expected, f"{call} should give {expected!r}, but it gave {got!r}."


def sales(**columns):
    """A small table of sales for one test, shaped like load_week's: total is quantity times price."""
    df = pd.DataFrame(columns)
    df["total"] = df["quantity"] * df["price"]
    return df


def three_sales():
    """Elote x1 at City Park ($4.50), Street Tacos x2 at Stadium ($18.00), Elote x2 at City Park ($9.00)."""
    return sales(location=["City Park", "Stadium", "City Park"], item=["Elote", "Street Tacos", "Elote"],
                 quantity=[1, 2, 2], price=[4.50, 9.00, 4.50])


def name(path):
    """A path's last part, or the value itself when it isn't a path."""
    return Path(path).name if isinstance(path, (str, Path)) else path


# newest_week_file

def test_1_newest_week_file_of_the_eight_seeded_weeks_is_week_2026_10_26(data_folder):
    check("newest_week_file(folder).name", name(newest_week_file(data_folder)), "week-2026-10-26.csv")


def test_2_newest_week_file_is_week_2026_11_02_after_the_next_week_arrives(data_folder):
    write_next_week(data_folder)
    check("newest_week_file(folder).name after seed.py --next", name(newest_week_file(data_folder)),
          "week-2026-11-02.csv")


def test_3_newest_week_file_picks_2026_10_05_over_2026_09_28_and_skips_notes_csv(tmp_path):
    for file_name in ["week-2026-10-05.csv", "week-2026-09-28.csv", "notes.csv"]:
        (tmp_path / file_name).write_text("sold_at\n", encoding="utf-8")
    check("newest_week_file(folder).name for week-2026-10-05.csv, week-2026-09-28.csv and notes.csv",
          name(newest_week_file(tmp_path)), "week-2026-10-05.csv")


def test_4_newest_week_file_of_an_empty_folder_raises_file_not_found_naming_the_folder(tmp_path):
    with pytest.raises(FileNotFoundError) as error:
        newest_week_file(tmp_path)
    assert str(tmp_path) in str(error.value), (
        f"newest_week_file(folder) of an empty folder should raise FileNotFoundError with a message that names "
        f"the folder, but the message was {str(error.value)!r}.")


# load_week

def test_5_load_week_reads_sold_at_as_dates_and_adds_total_2_times_9_is_18(tmp_path):
    path = tmp_path / "week-2026-09-07.csv"
    path.write_text(
        "sold_at,location,item,quantity,price,payment\n"
        "2026-09-07 11:05,Office Row,Street Tacos,2,9.00,card\n"
        "2026-09-07 11:09,Office Row,Elote,1,4.50,cash\n",
        encoding="utf-8",
    )
    week = load_week(path)
    check("load_week(path)['sold_at'].dtype is a datetime64 type",
          str(week["sold_at"].dtype).startswith("datetime64"), True)
    check("load_week(path)['total'] for 2 x 9.00 and 1 x 4.50", week["total"].tolist(), [18.0, 4.5])


def test_6_load_week_on_week_2026_09_07_gives_409_sales_adding_up_to_4653_50(data_folder):
    week = load_week(data_folder / "week-2026-09-07.csv")
    check("len(load_week(week-2026-09-07.csv))", len(week), 409)
    check("round(load_week(week-2026-09-07.csv)['total'].sum(), 2)", round(float(week["total"].sum()), 2), 4653.5)


# summarize

def test_7_summarize_three_sales_gives_31_5_5_elote_and_stadium():
    check("summarize(df) for Elote x1 and x2 at City Park, Street Tacos x2 at Stadium", summarize(three_sales()),
          {"sales": 31.5, "items_sold": 5, "best_item": "Elote", "best_location": "Stadium"})


def test_8_summarize_breaks_ties_alphabetically_elote_before_horchata_city_park_before_stadium():
    df = sales(location=["Stadium", "City Park"], item=["Horchata", "Elote"], quantity=[2, 2], price=[4.50, 4.50])
    got = summarize(df)
    check("summarize(df)['best_item'] for Horchata x2 and Elote x2", got["best_item"], "Elote")
    check("summarize(df)['best_location'] for $9.00 at Stadium and $9.00 at City Park", got["best_location"],
          "City Park")


def test_9_summarize_week_2026_10_26_gives_4455_0_537_street_tacos_and_stadium(data_folder):
    got = summarize(load_week(data_folder / "week-2026-10-26.csv"))
    check("summarize(load_week(week-2026-10-26.csv))", got,
          {"sales": 4455.0, "items_sold": 537, "best_item": "Street Tacos", "best_location": "Stadium"})


# items_chart

def test_10_items_chart_has_its_title_and_axis_labels():
    fig, ax = items_chart(three_sales())
    check("items_chart(df) title", ax.get_title(), "Items sold this week")
    check("items_chart(df) x-axis label", ax.get_xlabel(), "Item")
    check("items_chart(df) y-axis label", ax.get_ylabel(), "Number sold")


def test_11_items_chart_bars_are_elote_5_street_tacos_3_horchata_1_largest_first():
    df = sales(location=["City Park"] * 4, item=["Street Tacos", "Elote", "Horchata", "Elote"],
               quantity=[3, 2, 1, 3], price=[9.00, 4.50, 3.50, 4.50])
    fig, ax = items_chart(df)
    heights = [float(bar.get_height()) for bar in ax.patches]
    labels = [tick.get_text() for tick in ax.get_xticklabels()]
    check("items_chart(df) bar heights", heights, [5.0, 3.0, 1.0])
    check("items_chart(df) bar labels", labels, ["Elote", "Street Tacos", "Horchata"])


# write_report

def test_12_write_report_makes_the_folder_and_writes_report_html_and_items_png(tmp_path):
    out_dir = tmp_path / "reports" / "2026-10-26"
    report = write_report(three_sales(), out_dir)
    check("write_report(df, out_dir) returns", name(report), "report.html")
    check("report.html written in out_dir", (out_dir / "report.html").is_file(), True)
    check("items.png written in out_dir", (out_dir / "items.png").is_file(), True)
    check("items.png starts like a PNG file", (out_dir / "items.png").read_bytes()[:4], b"\x89PNG")


def test_13_write_report_page_shows_sales_31_50_items_5_elote_and_stadium(tmp_path):
    write_report(three_sales(), tmp_path)
    page = (tmp_path / "report.html").read_text(encoding="utf-8")
    for line in ["Sales: $31.50", "Items sold: 5", "Best-selling item: Elote", "Best location: Stadium"]:
        assert line in page, f"report.html should include {line!r}, but it doesn't."


def test_14_write_report_page_has_the_chart_and_the_sales_by_location_table(tmp_path):
    write_report(three_sales(), tmp_path)
    page = (tmp_path / "report.html").read_text(encoding="utf-8")
    image = '<img src="items.png" alt="Bar chart of the number of each item sold this week">'
    assert image in page, f"report.html should include {image!r}, but it doesn't."
    table = pd.DataFrame({"location": ["Stadium", "City Park"], "sales": [18.0, 13.5]}).to_html(index=False)
    assert table in page, (
        "report.html should include the table to_html(index=False) makes from location and sales, "
        f"largest first:\n{table}")


def test_15_write_report_on_week_2026_10_26_shows_sales_4_455_00_and_closes_the_chart(data_folder, tmp_path):
    write_report(load_week(data_folder / "week-2026-10-26.csv"), tmp_path)
    page = (tmp_path / "report.html").read_text(encoding="utf-8")
    assert "Sales: $4,455.00" in page, "report.html should include 'Sales: $4,455.00', but it doesn't."
    check("charts still open after write_report(df, out_dir)", len(plt.get_fignums()), 0)


# main

def test_16_main_with_data_and_out_writes_reports_2026_10_26_report_html(data_folder, tmp_path):
    out = tmp_path / "reports"
    report = main(["--data", str(data_folder), "--out", str(out)])
    check("main([...]) returns", Path(report), out / "2026-10-26" / "report.html")
    check("reports/2026-10-26/report.html written", (out / "2026-10-26" / "report.html").is_file(), True)


def test_17_main_prints_week_2026_10_26_sales_4455_0_and_the_report(data_folder, tmp_path, capsys):
    out = tmp_path / "reports"
    main(["--data", str(data_folder), "--out", str(out)])
    lines = capsys.readouterr().out.splitlines()
    check("main([...]) printed", lines, [
        "1) week: 2026-10-26",
        "2) sales: 4455.0",
        "3) items sold: 537",
        "4) best-selling item: Street Tacos",
        "5) best location: Stadium",
        f"6) report: {(out / '2026-10-26' / 'report.html').as_posix()}",
    ])


def test_18_main_builds_2026_11_02_once_the_next_week_arrives(data_folder, tmp_path):
    write_next_week(data_folder)
    out = tmp_path / "reports"
    main(["--data", str(data_folder), "--out", str(out)])
    check("reports/2026-11-02/report.html written", (out / "2026-11-02" / "report.html").is_file(), True)


def test_19_main_with_no_options_reads_data_incoming_and_writes_reports(data_folder, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    main([])
    check("reports/2026-10-26/report.html written by main([])",
          (tmp_path / "reports" / "2026-10-26" / "report.html").is_file(), True)
