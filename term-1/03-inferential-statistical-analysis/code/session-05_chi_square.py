"""
Session 5 · Example 1: Chi-square tests (goodness of fit and independence)
------------------------------------------------------------------------
  chi2 = sum (Observed - Expected)^2 / Expected

1. Goodness of fit: is a die fair? Do weekly orders follow the expected pattern?
2. Test of independence: is preferred payment method related to age group?
   Expected counts are computed by hand: E = row total * column total / grand total.
3. Effect size: Cramer's V.

Run:  python session-05_chi_square.py
"""
import numpy as np
import pandas as pd
from scipy import stats

# ---- 1a. Goodness of fit: 120 rolls of a die ----------------------------------------
obs = np.array([16, 25, 17, 14, 28, 20])
exp = np.full(6, obs.sum() / 6)
chi2 = ((obs - exp) ** 2 / exp).sum()
df = len(obs) - 1
print("1a) Is the die fair?  H0: every face has probability 1/6")
print("    observed:", obs.tolist(), " expected: 20 each")
print(f"    chi2 = {chi2:.3f}, df = {df}, critical (alpha .05) = {stats.chi2.ppf(0.95, df):.3f}, "
      f"p = {stats.chi2.sf(chi2, df):.4f}")
print("    scipy:", tuple(round(float(v), 4) for v in stats.chisquare(obs, exp)))

# ---- 1b. Goodness of fit with unequal expected proportions --------------------------
# A cafe plans staff assuming 10% of weekly orders Mon-Thu each, 20% Fri, 20% Sat, 20% Sun.
orders = np.array([52, 48, 61, 45, 98, 120, 76])
props = np.array([0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.20])
res = stats.chisquare(orders, props * orders.sum())
print(f"\n1b) Weekly order pattern: chi2 = {res.statistic:.2f}, p = {res.pvalue:.4f} "
      f"-> {'pattern differs from the plan' if res.pvalue < 0.05 else 'consistent with the plan'}")
print("    largest contributions:", dict(zip(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      [round(float(v), 1) for v in (orders - props * orders.sum()) ** 2 / (props * orders.sum())])))

# ---- 2. Test of independence --------------------------------------------------------
table = pd.DataFrame([[48, 30, 22], [35, 42, 28], [18, 28, 49]],
                     index=["18-25", "26-40", "41+"], columns=["Wallet app", "Card", "Cash"])
print("\n2) Payment method by age group (observed)")
print(table.to_string())
row, col, N = table.sum(axis=1).values, table.sum(axis=0).values, table.values.sum()
expected = np.outer(row, col) / N
chi2 = ((table.values - expected) ** 2 / expected).sum()
dof = (table.shape[0] - 1) * (table.shape[1] - 1)
print("Expected counts if independent:")
print(pd.DataFrame(expected.round(1), index=table.index, columns=table.columns).to_string())
print(f"chi2 = {chi2:.3f}, df = {dof}, p = {stats.chi2.sf(chi2, dof):.6f}")
c2, p, d, _ = stats.chi2_contingency(table)
print(f"scipy chi2_contingency: chi2 = {c2:.3f}, p = {p:.6f}, df = {d}")

# ---- 3. Effect size -------------------------------------------------------------------
V = np.sqrt(chi2 / (N * (min(table.shape) - 1)))
print(f"Cramer's V = {V:.3f}  (about 0.1 small, 0.3 medium, 0.5 large)")
