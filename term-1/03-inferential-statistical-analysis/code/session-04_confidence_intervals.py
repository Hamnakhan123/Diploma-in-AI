"""
Session 4 · Example 2: Standard error and confidence intervals
-------------------------------------------------------------
1. Build a 95% confidence interval for a mean, step by step (t interval).
2. A confidence interval for a proportion.
3. How sample size and confidence level change the width.
4. What '95% confidence' really means: draw 100 samples from a known
   population and count how many intervals capture the true mean.
   Chart saved to session-04_confidence_intervals.png

Run:  python session-04_confidence_intervals.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- 1. CI for a mean: daily mobile-data use (GB) of 12 students -----------------
x = np.array([1.8, 2.4, 3.1, 2.2, 2.9, 1.5, 3.6, 2.7, 2.0, 3.3, 2.5, 2.8])
n, xbar, s = len(x), x.mean(), x.std(ddof=1)
se = s / np.sqrt(n)
t_crit = stats.t.ppf(0.975, df=n - 1)
print("1) 95% CI for mean data use")
print(f"   n = {n}, x_bar = {xbar:.3f}, s = {s:.3f}, SE = s/sqrt(n) = {se:.4f}")
print(f"   t* (df = {n - 1}) = {t_crit:.3f}, margin of error = {t_crit * se:.3f}")
print(f"   CI = [{xbar - t_crit * se:.3f}, {xbar + t_crit * se:.3f}] GB")
print("   scipy:", tuple(round(float(v), 3) for v in stats.t.interval(0.95, n - 1, loc=xbar, scale=se)))

# ---- 2. CI for a proportion: 312 of 520 surveyed customers prefer digital payment -
k, m = 312, 520
p_hat = k / m
se_p = np.sqrt(p_hat * (1 - p_hat) / m)
z = stats.norm.ppf(0.975)
print(f"\n2) Proportion: p_hat = {p_hat:.3f}, SE = {se_p:.4f}, "
      f"95% CI = [{p_hat - z * se_p:.3f}, {p_hat + z * se_p:.3f}]")
# Sample size needed for a +/- 3 percentage-point margin (worst case p = 0.5)
print(f"   Sample size for a +/-3% margin: n = {int(np.ceil((z / 0.03) ** 2 * 0.25))}")

# ---- 3. Width vs n and confidence level -----------------------------------------
print("\n3) Width of a CI for a mean with s = 10")
print("   n      90%     95%     99%")
for nn in [10, 40, 160, 640]:
    w = [2 * stats.t.ppf(1 - a / 2, nn - 1) * 10 / np.sqrt(nn) for a in (0.10, 0.05, 0.01)]
    print(f"   {nn:<5}" + "".join(f"{v:8.2f}" for v in w))
print("   4x the sample -> about half the width; more confidence -> wider interval")

# ---- 4. Coverage simulation --------------------------------------------------------
rng = np.random.default_rng(8)
mu, sigma, nn = 50, 12, 25
hits, rows = 0, []
for i in range(100):
    smp = rng.normal(mu, sigma, nn)
    lo, hi = stats.t.interval(0.95, nn - 1, loc=smp.mean(), scale=smp.std(ddof=1) / np.sqrt(nn))
    ok = lo <= mu <= hi
    hits += ok
    rows.append((lo, hi, ok))
print(f"\n4) {hits} of 100 intervals contain the true mean {mu} (expected about 95)")

fig, ax = plt.subplots(figsize=(10, 4))
for i, (lo, hi, ok) in enumerate(rows):
    ax.plot([i, i], [lo, hi], color="#A78BFA" if ok else "#F43F5E", lw=2 if not ok else 1.2)
ax.axhline(mu, color="#FF6B1A", lw=2, label="true mean = 50")
ax.set_xlabel("sample number"); ax.set_ylabel("95% CI")
ax.set_title(f"100 confidence intervals: {hits} capture the true mean (red = miss)")
ax.legend(); fig.tight_layout(); fig.savefig("session-04_confidence_intervals.png", dpi=100)
print("Saved chart: session-04_confidence_intervals.png")
