"""
Session 3 · Example 1: Covariance and Pearson correlation, by hand and with SciPy
-------------------------------------------------------------------------------
Do students who study more hours score higher? We compute covariance and
Pearson's r step by step, test whether r is significantly different from 0,
and draw a 3-panel chart of positive, negative and 'no linear' relationships
(session-03_correlation.png), including a curved pattern where r is near 0
even though the variables are strongly related.

Run:  python session-03_correlation.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

hours = np.array([2, 3, 5, 1, 4, 6, 7, 3, 5, 8])            # weekly study hours
marks = np.array([55, 60, 70, 48, 66, 75, 82, 58, 68, 88])   # exam marks

# ---- Step by step -----------------------------------------------------------------
dx, dy = hours - hours.mean(), marks - marks.mean()
cov = (dx * dy).sum() / (len(hours) - 1)                       # sample covariance
r = cov / (hours.std(ddof=1) * marks.std(ddof=1))              # Pearson r = cov / (sx * sy)
print(f"mean hours = {hours.mean():.1f}, mean marks = {marks.mean():.1f}")
print(f"sum of cross-products = {(dx * dy).sum():.1f}")
print(f"covariance  = {cov:.3f}    (np.cov gives {np.cov(hours, marks)[0, 1]:.3f})")
print(f"Pearson r   = {r:.4f}   (r^2 = {r * r:.4f}: {100 * r * r:.1f}% of the variation in marks is linearly explained)")

# ---- Library + significance test --------------------------------------------------
res = stats.pearsonr(hours, marks)
t = r * np.sqrt((len(hours) - 2) / (1 - r ** 2))               # t statistic with n-2 df
print(f"scipy: r = {res.statistic:.4f}, p-value = {res.pvalue:.2e}; by hand t = {t:.2f} on {len(hours) - 2} df")

# ---- Covariance depends on units, correlation does not ----------------------------
minutes = hours * 60
print(f"\nStudy time in MINUTES: covariance = {np.cov(minutes, marks)[0, 1]:.1f} (60x bigger), "
      f"r = {np.corrcoef(minutes, marks)[0, 1]:.4f} (unchanged)")

# ---- Correlation matrix of several variables --------------------------------------
sleep = np.array([8, 7, 6, 9, 7, 6, 5, 8, 6, 5])               # hours of sleep
phone = np.array([5, 4, 3, 6, 3, 2, 1, 4, 3, 1])               # hours on phone per day
M = np.corrcoef([hours, marks, sleep, phone])
names = ["hours", "marks", "sleep", "phone"]
print("\nCorrelation matrix")
print(" " * 7 + "".join(f"{n:>8}" for n in names))
for n, row in zip(names, M):
    print(f"{n:<7}" + "".join(f"{v:>8.2f}" for v in row))

# ---- A strong but NON-linear relationship: r misses it ----------------------------
x = np.linspace(-3, 3, 25)
y = x ** 2
print(f"\ny = x^2 on [-3, 3]: Pearson r = {np.corrcoef(x, y)[0, 1]:.3f}  <- 'no LINEAR relationship', not 'no relationship'")

fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
axes[0].scatter(hours, marks, color="#FF6B1A"); axes[0].set_title(f"Hours vs marks: r = {r:.2f}")
axes[1].scatter(phone, marks, color="#A78BFA"); axes[1].set_title(f"Phone vs marks: r = {np.corrcoef(phone, marks)[0, 1]:.2f}")
axes[2].scatter(x, y, color="#F43F5E"); axes[2].set_title("y = x squared: r = 0.00")
for ax in axes:
    ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-03_correlation.png", dpi=100)
print("Saved chart: session-03_correlation.png")
