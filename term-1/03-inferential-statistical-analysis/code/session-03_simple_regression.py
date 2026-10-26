"""
Session 3 · Example 3: Simple linear regression with least squares
-----------------------------------------------------------------
Fit  marks = b0 + b1 * hours  using the closed-form least-squares formulas

      b1 = sum((x - x_bar)(y - y_bar)) / sum((x - x_bar)^2)
      b0 = y_bar - b1 * x_bar

then compute fitted values, residuals, SST = SSR + SSE, R^2, the standard
error of the slope, a 95% CI for the slope, and predictions. Compare with
scipy.stats.linregress and save a fit + residual chart (session-03_simple_regression.png).

Run:  python session-03_simple_regression.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.array([2, 3, 5, 1, 4, 6, 7, 3, 5, 8], dtype=float)       # study hours
y = np.array([55, 60, 70, 48, 66, 75, 82, 58, 68, 88], dtype=float)
n = len(x)

# ---- 1. Coefficients ----------------------------------------------------------------
Sxy = ((x - x.mean()) * (y - y.mean())).sum()
Sxx = ((x - x.mean()) ** 2).sum()
b1 = Sxy / Sxx
b0 = y.mean() - b1 * x.mean()
print(f"Sxy = {Sxy:.2f}, Sxx = {Sxx:.2f}")
print(f"Fitted line: marks = {b0:.3f} + {b1:.3f} * hours")
print(f"Meaning: each extra weekly study hour is associated with {b1:.2f} more marks.")

# ---- 2. Goodness of fit -------------------------------------------------------------
y_hat = b0 + b1 * x
resid = y - y_hat
SST = ((y - y.mean()) ** 2).sum()          # total variation
SSR = ((y_hat - y.mean()) ** 2).sum()      # explained by the line
SSE = (resid ** 2).sum()                   # left over (errors)
print(f"\nSST = {SST:.2f} = SSR {SSR:.2f} + SSE {SSE:.2f}")
print(f"R^2 = SSR/SST = {SSR / SST:.4f}")
s = np.sqrt(SSE / (n - 2))                 # residual standard error
se_b1 = s / np.sqrt(Sxx)
t_crit = stats.t.ppf(0.975, n - 2)
print(f"Residual standard error = {s:.3f} marks")
print(f"SE(b1) = {se_b1:.4f}; 95% CI for slope = [{b1 - t_crit * se_b1:.3f}, {b1 + t_crit * se_b1:.3f}]")
print(f"Residuals sum to {resid.sum():.1e} (always ~0 for least squares)")

# ---- 3. Check with SciPy ------------------------------------------------------------
lr = stats.linregress(x, y)
print(f"\nlinregress: slope {lr.slope:.3f}, intercept {lr.intercept:.3f}, r {lr.rvalue:.4f}, "
      f"p {lr.pvalue:.2e}, stderr {lr.stderr:.4f}")

# ---- 4. Prediction (and the danger of extrapolation) --------------------------------
for h in [4.5, 9, 20]:
    pred = b0 + b1 * h
    note = "" if h <= 8 else "  <- extrapolation: outside the observed 1-8 h, treat with caution"
    if pred > 100:
        note = "  <- IMPOSSIBLE: marks cannot exceed 100; the straight line does not hold out here"
    print(f"Predicted marks for {h:>4} h: {b0 + b1 * h:6.1f}{note}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
a1.scatter(x, y, color="#FF6B1A", zorder=3)
xs = np.linspace(0, 9, 50)
a1.plot(xs, b0 + b1 * xs, color="#0A0716", label=f"y = {b0:.1f} + {b1:.2f}x")
for xi, yi, yh in zip(x, y, y_hat):
    a1.plot([xi, xi], [yi, yh], color="#A78BFA", lw=1)          # residual segments
a1.set_xlabel("study hours"); a1.set_ylabel("marks"); a1.set_title("Least-squares line"); a1.legend()
a2.scatter(y_hat, resid, color="#F43F5E"); a2.axhline(0, color="grey", ls="--")
a2.set_xlabel("fitted value"); a2.set_ylabel("residual"); a2.set_title("Residuals: no pattern = good")
for ax in (a1, a2):
    ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-03_simple_regression.png", dpi=100)
print("Saved chart: session-03_simple_regression.png")
