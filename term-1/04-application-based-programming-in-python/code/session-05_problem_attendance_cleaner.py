"""
Session 5 · Real-life problem: cleaning a messy attendance file
---------------------------------------------------------------
PROBLEM
A biometric machine exported attendance_raw.csv, but the file has problems:
lower-case status codes, unknown codes, text in a number column, missing
names, short rows and an impossible date. Write a program that
  1. reads the raw file row by row,
  2. validates each row inside try/except, raising clear custom errors,
  3. writes good rows to attendance_clean.csv and bad rows (with the reason)
     to attendance_errors.log,
  4. prints each student's attendance percentage and draws a chart.
The program must NEVER crash on bad data, and must always report what it skipped.
Run:  python session-05_problem_attendance_cleaner.py
"""
import csv
from datetime import datetime

VALID_STATUS = {"P": "present", "A": "absent", "L": "leave"}

class BadRowError(Exception):
    """A row that cannot be trusted; the message explains why."""

def validate(row, line_no):
    """Return a cleaned dict or raise BadRowError."""
    if len(row) != 5:
        raise BadRowError(f"expected 5 fields, got {len(row)}")
    date_text, roll, name, status, late = (x.strip() for x in row)
    try:
        date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        raise BadRowError(f"invalid date {date_text!r}") from None
    if not name:
        raise BadRowError("missing name")
    status = status.upper()                      # accept 'p' as 'P'
    if status not in VALID_STATUS:
        raise BadRowError(f"unknown status {status!r}")
    try:
        late = int(late) if late else 0
    except ValueError:
        raise BadRowError(f"minutes_late is not a number: {late!r}") from None
    return {"date": date.isoformat(), "roll": roll, "name": name, "status": status, "minutes_late": late}

good, bad = [], []
try:
    with open("attendance_raw.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for line_no, row in enumerate(reader, start=2):      # line 1 is the header
            try:
                good.append(validate(row, line_no))
            except BadRowError as e:
                bad.append((line_no, str(e), ",".join(row)))
except FileNotFoundError:
    raise SystemExit("attendance_raw.csv not found - put it next to this script")

with open("attendance_clean.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(good[0]))
    w.writeheader(); w.writerows(good)
with open("attendance_errors.log", "w", encoding="utf-8") as f:
    for line_no, reason, raw in bad:
        f.write(f"line {line_no}: {reason} | {raw}\n")

print(f"read {len(good) + len(bad)} data rows: {len(good)} clean, {len(bad)} rejected")
print("\nattendance_errors.log")
print(open("attendance_errors.log", encoding="utf-8").read().rstrip())

# Attendance % per student (leave counts as excused, i.e. not held against them)
stats = {}
for r in good:
    s = stats.setdefault(r["name"], {"P": 0, "A": 0, "L": 0, "late": 0})
    s[r["status"]] += 1
    s["late"] += r["minutes_late"]
print(f"\n{'Student':12} {'P':>2} {'A':>2} {'L':>2} {'Attend %':>9} {'Late min':>9}")
names, pcts = [], []
for name, s in stats.items():
    counted = s["P"] + s["A"]
    pct = s["P"] / counted * 100 if counted else 0
    flag = "  <- below 75 %" if pct < 75 else ""
    print(f"{name:12} {s['P']:>2} {s['A']:>2} {s['L']:>2} {pct:>8.1f}% {s['late']:>9}{flag}")
    names.append(name); pcts.append(pct)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 3.4))
colours = ["#F43F5E" if p < 75 else "#FF6B1A" for p in pcts]
ax.barh(names, pcts, color=colours)
ax.axvline(75, color="#A78BFA", ls="--", label="75 % rule")
for i, p in enumerate(pcts):
    ax.text(p + 1, i, f"{p:.0f}%", va="center")
ax.set_xlim(0, 110); ax.set_xlabel("Attendance % (clean rows only)"); ax.legend(loc="lower right")
ax.set_title("Attendance after cleaning the raw export")
fig.tight_layout(); fig.savefig("session-05_problem_attendance_cleaner.png", dpi=110)
print("\nFiles written: attendance_clean.csv, attendance_errors.log, session-05_problem_attendance_cleaner.png")
