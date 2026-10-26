"""
Session 1 · Example 2: Mean, median, mode and the effect of an outlier
----------------------------------------------------------------------
We compute every measure of central tendency TWICE: once by hand with plain
Python (so you see the formula) and once with the library (so you trust it).
Then one CEO salary is added to show why the median is 'robust'.

Run:  python session-01_central_tendency.py
"""
from collections import Counter
import statistics as st
import numpy as np

# Monthly salaries (thousand PKR) of 9 employees at a small software house
salaries = [85, 90, 95, 95, 110, 120, 130, 140, 160]

def mean(xs):
    """Arithmetic mean: sum of values divided by how many there are."""
    return sum(xs) / len(xs)

def median(xs):
    """Middle value of the SORTED data (average of the two middles if n is even)."""
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 == 1 else (s[mid - 1] + s[mid]) / 2

def modes(xs):
    """All values that occur most often (data can be multimodal)."""
    c = Counter(xs)
    top = max(c.values())
    return [v for v, k in c.items() if k == top]

print("Salaries (k PKR):", salaries)
print(f"By hand  -> mean {mean(salaries):.2f}, median {median(salaries)}, mode {modes(salaries)}")
print(f"Library  -> mean {np.mean(salaries):.2f}, median {np.median(salaries)}, mode {st.multimode(salaries)}")

# Weighted mean: a student's GPA where courses carry different credit hours
grades_points = [4.0, 3.3, 3.7, 2.7]
credit_hours = [3, 4, 3, 1]
gpa = sum(g * w for g, w in zip(grades_points, credit_hours)) / sum(credit_hours)
print(f"\nWeighted mean (GPA) = {gpa:.3f}   (np.average gives {np.average(grades_points, weights=credit_hours):.3f})")

# Geometric mean: the right average for growth rates
growth = [1.10, 1.25, 0.95]          # +10 %, +25 %, -5 % yearly growth of a shop's revenue
gm = st.geometric_mean(growth)
print(f"Geometric mean growth factor = {gm:.4f} -> average growth {100 * (gm - 1):.2f}% per year")
print(f"(The arithmetic mean would wrongly say {100 * (mean(growth) - 1):.2f}% per year)")

# Harmonic mean: the right average for rates such as speed over equal distances
speeds = [60, 40]                      # km/h there and back on the same road
print(f"Harmonic mean speed = {st.harmonic_mean(speeds):.1f} km/h (not {mean(speeds):.0f})")

# The outlier test: the owner adds her own salary
with_ceo = salaries + [1500]
print("\nAdd one owner salary of 1500k:")
print(f"  mean   {mean(salaries):7.2f} -> {mean(with_ceo):7.2f}   (jumps by {mean(with_ceo) - mean(salaries):.1f})")
print(f"  median {median(salaries):7.2f} -> {median(with_ceo):7.2f}   (moves by {median(with_ceo) - median(salaries):.1f})")
print(f"  trimmed mean (drop top & bottom 10%): {st.mean(sorted(with_ceo)[1:-1]):.2f}")
print("Conclusion: report the MEDIAN for skewed data such as salaries or house prices.")
