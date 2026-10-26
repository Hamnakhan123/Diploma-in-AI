"""
Session 3 · Example 4: Types of regression - multiple, polynomial and logistic
-----------------------------------------------------------------------------
1. Multiple linear regression with statsmodels (two predictors, full summary numbers)
2. Polynomial regression: a curved relationship fitted with numpy.polyfit
3. Logistic regression: predicting a yes/no outcome (pass/fail) as a probability

Run:  python session-03_regression_types.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(3)

# ---- 1. Multiple regression: marks ~ hours + attendance ----------------------------
df = pd.DataFrame({
    "hours":      [2, 3, 5, 1, 4, 6, 7, 3, 5, 8, 2, 6, 4, 7, 1],
    "attendance": [70, 80, 85, 60, 75, 90, 95, 65, 88, 98, 85, 70, 92, 80, 75],
})
df["marks"] = (20 + 4.5 * df.hours + 0.35 * df.attendance + rng.normal(0, 2.5, len(df))).round(1)
model = smf.ols("marks ~ hours + attendance", data=df).fit()
print("1) Multiple regression: marks ~ hours + attendance")
print(model.params.round(3).to_string())
print(f"R^2 = {model.rsquared:.3f}, adjusted R^2 = {model.rsquared_adj:.3f}, F p-value = {model.f_pvalue:.2e}")
print("p-values:", model.pvalues.round(4).to_dict())
new = pd.DataFrame({"hours": [5], "attendance": [90]})
print(f"Prediction for 5 h and 90% attendance: {model.predict(new).iloc[0]:.1f} marks")

# ---- 2. Polynomial regression: fuel use vs speed is U-shaped ------------------------
speed = np.array([20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
litres = np.array([9.8, 8.1, 6.9, 6.2, 5.9, 6.0, 6.4, 7.1, 8.0, 9.2, 10.6])  # litres per 100 km
lin = np.polyfit(speed, litres, 1)
quad = np.polyfit(speed, litres, 2)
def r2(y, yh):
    return 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
print("\n2) Polynomial regression: fuel use vs speed")
print(f"straight line R^2 = {r2(litres, np.polyval(lin, speed)):.3f}")
print(f"quadratic      R^2 = {r2(litres, np.polyval(quad, speed)):.3f}  "
      f"(litres = {quad[0]:.5f}v^2 {quad[1]:+.4f}v {quad[2]:+.2f})")
print(f"most efficient speed = {-quad[1] / (2 * quad[0]):.0f} km/h (vertex of the parabola)")

# ---- 3. Logistic regression: P(pass) from study hours -------------------------------
hours = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7])
passed = np.array([0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])
logit = sm.Logit(passed, sm.add_constant(hours)).fit(disp=False)
b0, b1 = logit.params
print("\n3) Logistic regression: P(pass) = 1 / (1 + exp(-(b0 + b1*hours)))")
print(f"b0 = {b0:.3f}, b1 = {b1:.3f}; odds of passing multiply by {np.exp(b1):.2f} per extra hour")
for h in [1, 3, 5]:
    print(f"  P(pass | {h} h) = {1 / (1 + np.exp(-(b0 + b1 * h))):.3f}")
print(f"  50% chance at {-b0 / b1:.2f} hours")
