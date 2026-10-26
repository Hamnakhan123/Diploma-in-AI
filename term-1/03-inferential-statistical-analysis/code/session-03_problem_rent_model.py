"""
Session 3 · Real-life problem: is this flat's rent fair?
-------------------------------------------------------
PROBLEM
A property website has 24 listings of two-to-four room flats in one Karachi
area (rent in thousand PKR per month, covered area in square feet, rooms,
age of the building in years). A friend is offered a 1,150 sq ft, 3-room flat in
an 8-year-old building at 95k per month. Build a model and answer:
  1. Which variable is most strongly correlated with rent (Pearson and Spearman)?
  2. Fit rent ~ area (simple) and rent ~ area + rooms + age (multiple). Which is better?
  3. Interpret each coefficient in plain words.
  4. Predict the fair rent with a 95% prediction interval. Is 95k fair?

The listings are generated from a known formula plus noise so the script is
self-contained and reproducible (seed 21).
Run:  python session-03_problem_rent_model.py
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(21)
n = 24
area = rng.integers(750, 1800, n)
rooms = np.clip((area / 450).round().astype(int) + rng.integers(-1, 2, n), 2, 4)
age = rng.integers(1, 25, n)
rent = (15 + 0.055 * area + 4 * rooms - 0.9 * age + rng.normal(0, 5, n)).round(1)
df = pd.DataFrame({"area": area, "rooms": rooms, "age": age, "rent": rent})
print(df.describe().round(1).loc[["mean", "std", "min", "max"]].to_string())

# 1. Correlations with rent
print("\n1) Correlation with rent")
print(pd.DataFrame({"pearson": df.corr()["rent"], "spearman": df.corr(method="spearman")["rent"]})
      .drop("rent").round(3).to_string())

# 2. Two models
simple = smf.ols("rent ~ area", df).fit()
multi = smf.ols("rent ~ area + rooms + age", df).fit()
print(f"\n2) simple  : R^2 {simple.rsquared:.3f}, adj R^2 {simple.rsquared_adj:.3f}, "
      f"residual SE {np.sqrt(simple.mse_resid):.2f}k")
print(f"   multiple: R^2 {multi.rsquared:.3f}, adj R^2 {multi.rsquared_adj:.3f}, "
      f"residual SE {np.sqrt(multi.mse_resid):.2f}k")

# 3. Interpretation
p = multi.params
print("\n3) Coefficients (multiple model)")
print(f"   +100 sq ft  -> {100 * p['area']:+.2f}k rent, other things equal")
print(f"   +1 room     -> {p['rooms']:+.2f}k   (p = {multi.pvalues['rooms']:.2g})")
print(f"   +1 year old -> {p['age']:+.2f}k   (p = {multi.pvalues['age']:.2g})")

# 4. Prediction interval for the offered flat
flat = pd.DataFrame({"area": [1150], "rooms": [3], "age": [8]})
pred = multi.get_prediction(flat).summary_frame(alpha=0.05).iloc[0]
print(f"\n4) Fair rent estimate: {pred['mean']:.1f}k "
      f"(95% prediction interval {pred['obs_ci_lower']:.1f}k to {pred['obs_ci_upper']:.1f}k)")
offer = 95
verdict = "ABOVE the plausible range: negotiate" if offer > pred["obs_ci_upper"] else \
          "within the plausible range" if offer >= pred["obs_ci_lower"] else "a bargain"
print(f"   Offer of {offer}k is {verdict}.")
