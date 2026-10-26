"""
Session 1 · Example 1: Types of data and frequency tables
---------------------------------------------------------
Before computing any statistic you must know WHAT KIND of variable you have.
This script builds a small survey of 12 students, labels every column with its
level of measurement, and prints the summaries that are valid for each level.

Run:  python session-01_data_types.py
"""
import pandas as pd

# A tiny survey from a Karachi classroom (made-up but realistic values).
survey = pd.DataFrame({
    "student":      ["Ali", "Sara", "Bilal", "Hira", "Usman", "Zoya",
                     "Hamza", "Iqra", "Saad", "Maha", "Fahad", "Noor"],
    "area":         ["Gulshan", "Clifton", "Gulshan", "DHA", "Saddar", "Clifton",
                     "Gulshan", "DHA", "Saddar", "Gulshan", "Clifton", "DHA"],
    "grade":        ["B", "A", "C", "A", "B", "A", "C", "B", "B", "A", "C", "B"],
    "temp_c":       [31, 29, 33, 30, 34, 28, 32, 30, 35, 31, 29, 30],      # room temperature at home
    "siblings":     [2, 1, 3, 0, 4, 1, 2, 2, 5, 1, 3, 0],
    "commute_min":  [35, 20, 40, 15, 55, 25, 30, 18, 60, 33, 22, 16],
})

# Level of measurement for each variable, and what you are allowed to do with it.
levels = {
    "area":        ("Nominal",  "categories, no order -> counts, mode"),
    "grade":       ("Ordinal",  "ordered categories -> counts, mode, median"),
    "temp_c":      ("Interval", "equal steps, no true zero -> mean, std (no ratios)"),
    "siblings":    ("Ratio (discrete)",   "true zero, counts -> every statistic"),
    "commute_min": ("Ratio (continuous)", "true zero, measured -> every statistic"),
}
print("Variable      Level                Valid summaries")
print("-" * 72)
for col, (lvl, ok) in levels.items():
    print(f"{col:<13} {lvl:<20} {ok}")

# 1) Nominal: a frequency table with relative and percentage frequency
freq = survey["area"].value_counts().rename("count").to_frame()
freq["relative"] = (freq["count"] / freq["count"].sum()).round(3)
freq["percent"] = (freq["relative"] * 100).round(1)
print("\nFrequency table for 'area' (nominal):")
print(freq.to_string())
print("Mode of area:", survey["area"].mode().tolist())

# 2) Ordinal: keep the natural order A > B > C, then the median makes sense
grade_order = pd.CategoricalDtype(["C", "B", "A"], ordered=True)
grades = survey["grade"].astype(grade_order)
counts = grades.value_counts(sort=False)
print("\nGrade counts in order (ordinal):", {k: int(v) for k, v in counts.items()})
median_code = int(grades.cat.codes.median())          # codes: C=0, B=1, A=2
print("Median grade:", grade_order.categories[median_code])

# 3) Interval vs ratio: 35 C is NOT "1.25x as hot" as 28 C (0 C is not "no heat"),
#    but a 60-minute commute IS 4x a 15-minute one (0 minutes really means none).
print(f"\nCommute ratio Saad/Hira = {survey.commute_min[8] / survey.commute_min[3]:.1f}x (valid: ratio scale)")

# 4) Grouped frequency table (class intervals) for a continuous variable
bins = [10, 20, 30, 40, 50, 60]
classes = pd.cut(survey["commute_min"], bins=bins, right=True)
grouped = classes.value_counts(sort=False).rename("students").to_frame()
grouped["cumulative"] = grouped["students"].cumsum()
print("\nGrouped frequency table for commute (minutes):")
print(grouped.to_string())
