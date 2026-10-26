"""
Session 6 · Real-life problem: do delivery times differ by zone and time of day?
-------------------------------------------------------------------------------
PROBLEM
A food-delivery start-up in Karachi recorded delivery times (minutes) for
orders in 4 zones (Clifton, Gulshan, Saddar, North Nazimabad) at 2 times of
day (Lunch, Dinner), 6 orders per combination (48 orders).
Operations wants to know:
  1. Do mean delivery times differ by zone? (one-way ANOVA + Tukey)
  2. Does time of day matter, and does its effect depend on the zone? (two-way ANOVA)
  3. Are the assumptions reasonable? (Levene, Shapiro on residuals)
  4. Which zone-time combinations need extra riders?

Run:  python session-06_problem_delivery_zones.py
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

rng = np.random.default_rng(99)
base = {"Clifton": 28, "Gulshan": 34, "Saddar": 38, "North Nazimabad": 33}
dinner_extra = {"Clifton": 2, "Gulshan": 3, "Saddar": 9, "North Nazimabad": 3}   # Saddar traffic at night
rows = [{"zone": z, "time": t, "minutes": round(base[z] + (dinner_extra[z] if t == "Dinner" else 0)
                                              + rng.normal(0, 3), 1)}
        for z in base for t in ["Lunch", "Dinner"] for _ in range(6)]
df = pd.DataFrame(rows)

print("Mean minutes by zone and time")
print(df.pivot_table(values="minutes", index="zone", columns="time", aggfunc="mean").round(1).to_string())

# 1. One-way ANOVA by zone + Tukey
f1 = stats.f_oneway(*[g.minutes for _, g in df.groupby("zone")])
print(f"\n1) One-way ANOVA by zone: F = {f1.statistic:.2f}, p = {f1.pvalue:.2e}")
print(pairwise_tukeyhsd(df.minutes, df.zone).summary())

# 2. Two-way ANOVA with interaction
model = smf.ols("minutes ~ C(zone) * C(time)", data=df).fit()
print("\n2) Two-way ANOVA")
print(sm.stats.anova_lm(model, typ=2).assign(**{"PR(>F)": lambda t: t["PR(>F)"].map(lambda v: "" if v != v else f"{v:.2e}")}).round(4).to_string())

# 3. Assumptions
print(f"\n3) Levene across the 8 cells p = {stats.levene(*[g.minutes for _, g in df.groupby(['zone', 'time'])]).pvalue:.3f}; "
      f"Shapiro on residuals p = {stats.shapiro(model.resid).pvalue:.3f}")

# 4. Action list: cells more than 3 minutes above the overall mean
cells = df.groupby(["zone", "time"]).minutes.mean()
overall = df.minutes.mean()
print(f"\n4) Overall mean {overall:.1f} min. Cells that need extra riders (> mean + 3 min):")
for (z, t), m in cells.items():
    if m > overall + 3:
        print(f"   {z} at {t}: {m:.1f} min")
