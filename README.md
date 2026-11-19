# Exercise: Food Truck Weekly Report

Exercise code for the lesson **Exercise: Food Truck Weekly Report** in the Python for Data Analysis course on [ask-codey.com](https://www.ask-codey.com).

Every Monday, the Greenway Food Truck's owner wants last week's numbers: the sales, how many items sold, the best-selling item and the best spot to park. A new file of sales arrives each week. You'll write the six functions in `weekly_report.py` that find the newest week, sum it up, chart it and write it as a web page, so one command builds the report from whichever week is newest. Tests call each function, run the whole script, and check the files it writes.

## What's here

- `seed.py`: makes eight weeks of sales in `data/incoming/`, one file a week (`week-2026-09-07.csv` to `week-2026-10-26.csv`), our own made-up data. `python seed.py --next` adds the week after the newest, as a new week arriving. It uses fixed random seeds, so it writes the same files on every computer. Ready to use.
- `weekly_report.py`: the six functions, `newest_week_file`, `load_week`, `summarize`, `items_chart`, `write_report` and `main`. Each one stops with `NotImplementedError: Not built yet.` for now. The docstring under each says what it should do, with examples. For you to finish.
- `explore.ipynb`: a notebook for looking at the weeks and trying your functions as you write them. Its first cell turns on autoreload, so each change you save in `weekly_report.py` is used at once. The tests don't read it. Ready to use, and yours to change.
- `tests/test_weekly_report.py`: tests that call your functions and check what comes back and the files written. You don't need to change this file.
- `tests/conftest.py`: gives each test a fresh copy of the eight weeks, made by `seed.py` in a temporary folder, so the tests use the same data even if you changed `data/incoming`, and draws the charts without opening a window. Ready to use.
- `requirements.txt`: the packages this exercise needs, each at an exact version: pandas, matplotlib, ipykernel (so VS Code can run the notebook) and pytest. Ready to use.
- `pytest.ini`: tells pytest where the tests are and where to find `weekly_report.py` and `seed.py`. Ready to use.
- `.gitignore`: tells Git to leave out the virtual environment, the files Python and pytest make as they run, `data/` (which `seed.py` makes again whenever it's needed) and `reports/` (which your script makes). Ready to use.

## Before you start

The packages go in a virtual environment: a private set of packages for this folder only. In VS Code's terminal, in this folder, run these three commands.

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On a Mac (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- The first command makes the virtual environment, in a folder named `.venv`.
- The second turns it on for this terminal: the prompt starts with `(.venv)` from then on.
- The third installs the packages `requirements.txt` lists into it.

*Virtual Environments and pip* explains all three. The `.venv` folder is in `.gitignore`, so Git leaves it out: these commands make it again on any computer.

If PowerShell answers that running scripts is disabled on this system, run this once, then run the second command again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Each new terminal starts with the virtual environment off. If the prompt doesn't start with `(.venv)`, run the second command again. (VS Code often turns it on for you.)

Then make the data, once:

```bash
python seed.py
```

It prints one line for each of the eight weeks it writes, from `Wrote data/incoming/week-2026-09-07.csv: 409 sales.` to `Wrote data/incoming/week-2026-10-26.csv: 390 sales.` To look at the weeks, open `explore.ipynb`, choose the `.venv` kernel with **Select Kernel** (top right), and run the cells.

## Check your work

```bash
python -m pytest
```

At first every test fails: that is expected, because each function stops with a `NotImplementedError` for now. Each function you finish turns its tests green. A failing test's message says what it called, what it expected and what came back, for example *newest_week_file(folder).name should give 'week-2026-10-26.csv', but it gave 'week-2026-09-07.csv'.*

To build the report for the newest week, run:

```bash
python weekly_report.py
```

It writes `reports/2026-10-26/report.html` and `reports/2026-10-26/items.png`. Open `report.html` in your browser to see the page. Then make next week's file and build again:

```bash
python seed.py --next
python weekly_report.py
```

This time the report goes in `reports/2026-11-02/`, and last week's report is still there beside it.

## The rules

- Keep each function's name and parameters as they are.
- The newest week is the last `week-*.csv` file by name. The names start with the year, so sorting them puts them in date order.
- `write_report` and `main` take folders as a `str` or a `Path`, and make the output folder if it isn't there.
- `write_report` saves the chart with `savefig` and closes it with `plt.close(fig)`.
- The report's text matches the formats in `write_report`'s docstring exactly: the sales with a dollar sign, a comma and 2 decimal places, the items sold with a comma.
- `main` reads its options from the list it's given (`argv`), not from `sys.argv`, so the tests can call it with their own folders.
- Don't change the tests, `conftest.py` or `seed.py`.

## Tips

- Try each step in `explore.ipynb` first, on the real weeks, then move the lines that work into `weekly_report.py`.
- `sorted(Path(folder).glob("week-*.csv"))` gives the week files in date order; `[-1]` is the last of them.
- `pd.read_csv(path, parse_dates=["sold_at"])` reads a column as dates and times.
- `groupby(...)[...].sum().idxmax()` gives the label of the largest total; for a tie, it gives the first label, and groupby sorts labels alphabetically.
- `f"{16543.5:,.2f}"` gives `16,543.50`, and `f"{1402:,}"` gives `1,402`.
- `Path(folder) / "2026-10-26"` builds a path, `.mkdir(parents=True, exist_ok=True)` makes the folder (and any above it), and `.write_text(page, encoding="utf-8")` writes a file.
- A path's `.stem` is its file name without `.csv`, and `.removeprefix("week-")` takes `week-` off the front: `week-2026-10-26.csv` gives `2026-10-26`.

## Hand it in

When it works, push your solution to a public repo of your own on GitHub, then paste that repo's address into **Submit your exercise** on the lesson page at [ask-codey.com](https://www.ask-codey.com). That's what completes the lesson. The lesson page shows the Git commands, step by step.
