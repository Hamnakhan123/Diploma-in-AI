"""
Session 1 · Real-life problem: the exam-result report
-----------------------------------------------------
PROBLEM
A lecturer has the final marks (out of 100) of two sections. The head of
department wants, for each section:
  1. n, mean, median, standard deviation, min, max, Q1, Q3, IQR
  2. any outliers by the 1.5 x IQR rule AND by |z| > 2.5
  3. the grade distribution (A >= 85, B >= 70, C >= 55, D >= 40, F below)
  4. a one-line verdict: which section did better and which was more consistent?

SOLUTION (pure pandas + numpy, no hidden helpers)
Run:  python session-01_problem_exam_report.py
"""
import numpy as np
import pandas as pd

marks = {
    "Section A": [72, 65, 88, 91, 54, 77, 69, 83, 95, 60, 74, 81, 12, 70, 79, 86, 68, 73],
    "Section B": [66, 71, 69, 74, 70, 68, 72, 75, 67, 73, 70, 69, 71, 76, 65, 72, 70, 74],
}

def grade(m):
    """Convert a mark to a letter grade using the department's cut-offs."""
    for cut, letter in [(85, "A"), (70, "B"), (55, "C"), (40, "D")]:
        if m >= cut:
            return letter
    return "F"

def describe_section(name, values):
    x = pd.Series(values, name=name)
    q1, q3 = x.quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr          # Tukey fences
    z = (x - x.mean()) / x.std(ddof=1)                 # standard scores
    report = {
        "n": len(x), "mean": x.mean(), "median": x.median(), "std": x.std(ddof=1),
        "min": x.min(), "Q1": q1, "Q3": q3, "max": x.max(), "IQR": iqr,
        "IQR outliers": x[(x < lo) | (x > hi)].tolist(),
        "z outliers": x[z.abs() > 2.5].tolist(),
    }
    grades = x.map(grade).value_counts().reindex(list("ABCDF"), fill_value=0)
    return report, grades

rows, grade_tables = {}, {}
for name, vals in marks.items():
    rows[name], grade_tables[name] = describe_section(name, vals)

table = pd.DataFrame(rows)
pd.set_option("display.width", 100)
print("Descriptive report")
print(table.to_string(formatters=None))
print("\nGrade distribution")
print(pd.DataFrame(grade_tables).T.to_string())

# Same summary after removing the outlier from Section A (was it a data-entry error or an absent student?)
clean_a = [m for m in marks["Section A"] if m not in rows["Section A"]["IQR outliers"]]
print(f"\nSection A without outliers: mean {np.mean(clean_a):.2f}, "
      f"median {np.median(clean_a):.1f}, std {np.std(clean_a, ddof=1):.2f}")

better = max(rows, key=lambda k: rows[k]["median"])
steadier = min(rows, key=lambda k: rows[k]["IQR"])
print(f"\nVerdict: {better} has the higher median mark; {steadier} is the more consistent section "
      f"(smaller IQR). Check the outlier in Section A before publishing.")
