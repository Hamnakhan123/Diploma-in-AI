"""
Session 1 · Mini project: build your own describe()
---------------------------------------------------
Goal: write a small, reusable descriptive-statistics toolkit WITHOUT numpy,
then prove it is correct by comparing it with pandas on a real-looking data set
(daily electricity units used by a Karachi household over 30 days).

Features
  * mean, median, mode(s), variance and std (sample or population)
  * quantiles with linear interpolation (same method as pandas/numpy default)
  * IQR, outliers, skewness (adjusted Fisher-Pearson, same as pandas)
  * a text histogram so you can 'see' the data in a terminal

Run:  python session-01_project_stats_toolkit.py
"""
from collections import Counter
import math
import pandas as pd


class Describe:
    def __init__(self, data):
        if not data:
            raise ValueError("data must not be empty")
        self.x = sorted(float(v) for v in data)
        self.n = len(self.x)

    # ---- centre --------------------------------------------------------------
    def mean(self):
        return sum(self.x) / self.n

    def median(self):
        return self.quantile(0.5)

    def modes(self):
        c = Counter(self.x)
        top = max(c.values())
        return sorted(v for v, k in c.items() if k == top) if top > 1 else []

    # ---- spread --------------------------------------------------------------
    def var(self, sample=True):
        m = self.mean()
        ss = sum((v - m) ** 2 for v in self.x)
        return ss / (self.n - 1 if sample else self.n)

    def std(self, sample=True):
        return math.sqrt(self.var(sample))

    def quantile(self, q):
        """Linear interpolation between closest ranks: position = q * (n - 1)."""
        pos = q * (self.n - 1)
        lo = math.floor(pos)
        hi = min(lo + 1, self.n - 1)
        return self.x[lo] + (pos - lo) * (self.x[hi] - self.x[lo])

    def iqr(self):
        return self.quantile(0.75) - self.quantile(0.25)

    def outliers(self, k=1.5):
        q1, q3 = self.quantile(0.25), self.quantile(0.75)
        return [v for v in self.x if v < q1 - k * self.iqr() or v > q3 + k * self.iqr()]

    # ---- shape ---------------------------------------------------------------
    def skew(self):
        """Adjusted Fisher-Pearson skewness (the formula pandas uses)."""
        m, s, n = self.mean(), self.std(), self.n
        g = sum(((v - m) / s) ** 3 for v in self.x)
        return n / ((n - 1) * (n - 2)) * g

    # ---- report --------------------------------------------------------------
    def report(self):
        return {"count": self.n, "mean": self.mean(), "std": self.std(), "min": self.x[0],
                "25%": self.quantile(0.25), "50%": self.median(), "75%": self.quantile(0.75),
                "max": self.x[-1], "skew": self.skew()}

    def text_histogram(self, bins=6, width=30):
        lo, hi = self.x[0], self.x[-1]
        step = (hi - lo) / bins
        counts = [0] * bins
        for v in self.x:
            i = min(int((v - lo) / step), bins - 1)
            counts[i] += 1
        top = max(counts)
        for i, c in enumerate(counts):
            left = lo + i * step
            print(f"  {left:6.1f}-{left + step:6.1f} | {'#' * round(width * c / top):<{width}} {c}")


units = [14, 15, 13, 16, 18, 17, 15, 14, 19, 22, 21, 16, 15, 14, 13,
         17, 18, 16, 15, 14, 31, 16, 15, 17, 18, 19, 16, 15, 14, 16]   # day 21: a wedding at home!

d = Describe(units)
mine = d.report()
theirs = pd.Series(units, dtype=float).describe().to_dict()
theirs["skew"] = pd.Series(units).skew()

print(f"{'statistic':<8} {'toolkit':>10} {'pandas':>10}  match")
for k in mine:
    ok = math.isclose(mine[k], theirs[k], rel_tol=1e-9)
    print(f"{k:<8} {mine[k]:>10.3f} {theirs[k]:>10.3f}  {'yes' if ok else 'NO'}")
print("modes:", d.modes(), "  IQR:", d.iqr(), "  outliers:", d.outliers())
print("\nText histogram of daily units:")
d.text_histogram()
