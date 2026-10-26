"""
Session 5 · Mini project: a persistent expense tracker (JSON file + exceptions)
------------------------------------------------------------------------------
Expenses are saved to expenses.json so they survive between runs. The program
  - loads the file safely (missing file -> start empty; corrupt file -> back it up),
  - validates every new expense with custom exceptions,
  - saves atomically (write to a temp file, then replace) so a crash never
    leaves a half-written file,
  - exports a CSV report and a chart by category.
Run:  python session-05_project_expense_tracker.py
"""
import csv
import json
import os
from datetime import date

DATA_FILE = "expenses.json"
CATEGORIES = {"food", "transport", "bills", "education", "other"}

class ExpenseError(Exception):
    """Base class for all tracker errors."""
class InvalidAmountError(ExpenseError):
    pass
class UnknownCategoryError(ExpenseError):
    pass

def load(path=DATA_FILE):
    """Return the list of expenses; never crash on a missing or broken file."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  (no {path} yet - starting a new tracker)")
        return []
    except json.JSONDecodeError:
        os.replace(path, path + ".corrupt")
        print(f"  ({path} was corrupt - moved to {path}.corrupt, starting fresh)")
        return []

def save(expenses, path=DATA_FILE):
    """Atomic save: write a temporary file first, then swap it in."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)
    os.replace(tmp, path)

def add(expenses, day, category, amount, note=""):
    """Validate and append one expense; raise an ExpenseError subclass on bad input."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise InvalidAmountError(f"amount {amount!r} is not a number") from None
    if amount <= 0:
        raise InvalidAmountError("amount must be positive")
    category = category.lower().strip()
    if category not in CATEGORIES:
        raise UnknownCategoryError(f"{category!r} is not one of {sorted(CATEGORIES)}")
    date.fromisoformat(day)                      # raises ValueError for a bad date
    expenses.append({"date": day, "category": category, "amount": amount, "note": note})

# Start clean for a reproducible demo
for leftover in (DATA_FILE, DATA_FILE + ".corrupt"):
    if os.path.exists(leftover):
        os.remove(leftover)

print("Run 1: first use")
expenses = load()
entries = [
    ("2026-10-01", "Bills", 6_800, "electricity"), ("2026-10-02", "food", 1_250, "groceries"),
    ("2026-10-03", "transport", 900, "ride to campus"), ("2026-10-04", "education", "3,500", "books"),
    ("2026-10-05", "food", -40, "refund?"), ("2026-10-06", "shopping", 2_000, "shoes"),
    ("2026-10-07", "education", 3_500, "books"), ("2026-10-08", "food", 2_100, "dinner out"),
    ("2026-10-31", "transport", 1_400, "fuel"), ("2026-10-32", "other", 500, "typo date"),
]
for day, cat, amt, note in entries:
    try:
        add(expenses, day, cat, amt, note)
        print(f"  added   {day} {cat:<10} {float(amt):>8,.0f}")
    except ExpenseError as e:
        print(f"  skipped {day}: {type(e).__name__}: {e}")
    except ValueError as e:
        print(f"  skipped {day}: bad date ({e})")
save(expenses)
print(f"  saved {len(expenses)} expenses to {DATA_FILE}")

print("\nRun 2: the program starts again and reloads the file")
expenses = load()
print(f"  loaded {len(expenses)} expenses, total Rs {sum(e['amount'] for e in expenses):,.0f}")

print("\nRun 3: someone corrupts the file by hand")
with open(DATA_FILE, "a", encoding="utf-8") as f:
    f.write("}}} oops")
expenses_after = load()
print("  recovered list length:", len(expenses_after))

# Report from the good data loaded in run 2
totals = {}
for e in expenses:
    totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
with open("expense_report.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["category", "total", "share"])
    grand = sum(totals.values())
    for cat, t in sorted(totals.items(), key=lambda kv: -kv[1]):
        w.writerow([cat, f"{t:.0f}", f"{t / grand:.1%}"])
print("\nexpense_report.csv")
print(open("expense_report.csv", encoding="utf-8").read().rstrip())

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
cats = sorted(totals, key=totals.get, reverse=True)
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.bar(cats, [totals[c] for c in cats], color=["#FF6B1A", "#FCD34D", "#A78BFA", "#F43F5E"][:len(cats)])
ax.set_ylabel("Rs"); ax.set_title("October spending by category (valid entries only)")
fig.tight_layout(); fig.savefig("session-05_project_expense_tracker.png", dpi=110)

for f in (DATA_FILE, DATA_FILE + ".corrupt"):      # tidy the demo files, keep the report
    if os.path.exists(f):
        os.remove(f)
print("Chart saved: session-05_project_expense_tracker.png")
