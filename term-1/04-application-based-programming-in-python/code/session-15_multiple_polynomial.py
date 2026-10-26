"""
Session 15 · Example 2: multiple and polynomial regression, and overfitting
---------------------------------------------------------------------------
Multiple regression:   y = b0 + b1*x1 + b2*x2 + ...      (several features)
Polynomial regression: y = b0 + b1*x + b2*x^2 + ...      (a curve, still 'linear' in the b's)
Too high a degree memorises noise: low training error, high test error.
Run:  python session-15_multiple_polynomial.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(15)
# ---- Part A: multiple linear regression - monthly electricity use of homes ----
n = 300
homes = pd.DataFrame({"area_sqyd": rng.integers(80, 500, n), "people": rng.integers(1, 9, n),
                      "acs": rng.integers(0, 4, n), "avg_temp": rng.uniform(18, 38, n).round(1)})
homes["units"] = (50 + 0.6 * homes.area_sqyd + 25 * homes.people + 140 * homes.acs * (homes.avg_temp - 15) / 10
                  + rng.normal(0, 40, n)).round(0)
X, y = homes.drop(columns="units"), homes["units"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
lin = LinearRegression().fit(Xtr, ytr)
print("Multiple regression: units =", f"{lin.intercept_:.1f}",
      " ".join(f"{c:+.2f}*{f}" for f, c in zip(X.columns, lin.coef_)))
print(f"test R^2 = {r2_score(yte, lin.predict(Xte)):.3f}, RMSE = {np.sqrt(mean_squared_error(yte, lin.predict(Xte))):.1f} units")
std = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
print("standardised coefficients (comparable importance):",
      {f: round(float(c), 1) for f, c in zip(X.columns, std[-1].coef_)})

# An interaction feature captures 'ACs matter more on hot days'
homes["ac_heat"] = homes.acs * homes.avg_temp
Xtr2, Xte2 = Xtr.join(homes.loc[Xtr.index, ["ac_heat"]]), Xte.join(homes.loc[Xte.index, ["ac_heat"]])
lin2 = LinearRegression().fit(Xtr2, ytr)
print(f"with interaction feature ac_heat: test R^2 = {r2_score(yte, lin2.predict(Xte2)):.3f}")

# ---- Part B: polynomial regression and overfitting ----
x = np.sort(rng.uniform(0, 10, 40))
y_curve = 2 + 1.5 * x - 0.12 * x ** 2 + rng.normal(0, 0.6, 40)     # a gentle curve + noise
xtr, xte, ytr_c, yte_c = train_test_split(x.reshape(-1, 1), y_curve, test_size=0.3, random_state=2)
print("\ndegree  train RMSE  test RMSE")
results = {}
for d in [1, 2, 3, 6, 12]:
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(xtr, ytr_c)
    tr = np.sqrt(mean_squared_error(ytr_c, m.predict(xtr)))
    te = np.sqrt(mean_squared_error(yte_c, m.predict(xte)))
    results[d] = (m, tr, te)
    print(f"{d:>6}  {tr:10.3f}  {te:9.3f}" + ("   <- underfits" if d == 1 else "   <- overfits" if d == 12 else ""))
best = min(results, key=lambda d: results[d][2])
print("best degree on the test set:", best)

fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
grid = np.linspace(0, 10, 300).reshape(-1, 1)
ax[0].scatter(xtr, ytr_c, color="#6B7280", s=18, label="train"); ax[0].scatter(xte, yte_c, color="#F43F5E", s=18, label="test")
for d, col in [(1, "#A78BFA"), (2, "#FF6B1A"), (12, "#22C55E")]:
    ax[0].plot(grid, np.clip(results[d][0].predict(grid), -5, 15), color=col, label=f"degree {d}")
ax[0].set_ylim(-1, 9); ax[0].legend(fontsize=8); ax[0].set_title("Underfit, good fit, overfit")
ds = list(results)
ax[1].plot(ds, [results[d][1] for d in ds], "o-", color="#FF6B1A", label="train RMSE")
ax[1].plot(ds, [results[d][2] for d in ds], "s-", color="#F43F5E", label="test RMSE")
ax[1].set_yscale("log"); ax[1].set_xlabel("polynomial degree"); ax[1].legend(); ax[1].set_title("Training error keeps falling; test error does not")
fig.tight_layout(); fig.savefig("session-15_multiple_polynomial.png", dpi=100)
print("Saved session-15_multiple_polynomial.png")
