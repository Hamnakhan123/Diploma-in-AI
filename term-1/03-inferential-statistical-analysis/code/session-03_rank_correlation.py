"""
Session 3 · Example 2: Rank correlation (Spearman and Kendall)
--------------------------------------------------------------
Two judges rank 8 entries in a university poster competition. Ranks are
ORDINAL, so Pearson's r is not appropriate; we use Spearman's rho:

      rho = 1 - 6 * sum(d^2) / (n (n^2 - 1))      (valid when there are no ties)

We also show that Spearman is robust to an outlier and measures any MONOTONIC
relationship, and handle tied values with average ranks.

Run:  python session-03_rank_correlation.py
"""
import numpy as np
from scipy import stats

entries = ["A", "B", "C", "D", "E", "F", "G", "H"]
judge1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
judge2 = np.array([2, 1, 4, 3, 6, 5, 8, 7])

d = judge1 - judge2
n = len(d)
rho = 1 - 6 * (d ** 2).sum() / (n * (n ** 2 - 1))
print("entry  J1  J2   d  d^2")
for e, a, b, di in zip(entries, judge1, judge2, d):
    print(f"  {e}    {a}   {b}  {di:+d}   {di * di}")
print(f"sum d^2 = {(d ** 2).sum()}  ->  rho = 1 - 6*{(d ** 2).sum()}/({n}*{n * n - 1}) = {rho:.4f}")
print(f"scipy spearmanr = {stats.spearmanr(judge1, judge2).statistic:.4f}, "
      f"kendalltau = {stats.kendalltau(judge1, judge2).statistic:.4f}")

# ---- Ties: give tied values the AVERAGE of the ranks they occupy -------------------
scores = np.array([70, 85, 85, 60, 90, 70, 75])
print("\nScores:", scores.tolist())
print("Average ranks:", stats.rankdata(scores).tolist(), " (the two 85s share ranks 5 and 6 -> 5.5)")

# ---- Robustness and monotonic relationships ---------------------------------------
income = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 900])   # one billionaire-style outlier
spend = np.array([20, 24, 27, 30, 33, 35, 38, 41, 43, 60])
print(f"\nWith an outlier: Pearson r = {stats.pearsonr(income, spend).statistic:.3f}, "
      f"Spearman rho = {stats.spearmanr(income, spend).statistic:.3f}")
x = np.arange(1, 11)
y = np.exp(x / 2)                                              # monotonic but curved
print(f"Exponential curve: Pearson r = {stats.pearsonr(x, y).statistic:.3f}, "
      f"Spearman rho = {stats.spearmanr(x, y).statistic:.3f} (perfectly monotonic)")
