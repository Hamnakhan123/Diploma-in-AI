"""
Session 1 · Example 3: Spread and shape, with a chart
-----------------------------------------------------
Two food-delivery riders have the SAME average delivery time but very different
reliability. Measures of dispersion (range, variance, standard deviation, IQR,
coefficient of variation) and shape (skewness, kurtosis) reveal the difference.
The script also saves a histogram + box plot: session-01_dispersion_shape.png

Run:  python session-01_dispersion_shape.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")                      # draw to a file, no window needed
import matplotlib.pyplot as plt
from scipy import stats

# Delivery times in minutes for 15 orders each (deterministic data, no randomness)
rider_a = np.array([28, 29, 30, 30, 31, 29, 30, 31, 30, 32, 29, 30, 31, 30, 30])
rider_b = np.array([15, 18, 45, 20, 50, 22, 25, 40, 19, 38, 21, 55, 24, 23, 35])

def summary(name, x):
    q1, q3 = np.percentile(x, [25, 75])
    var_pop = np.var(x)              # divide by n      (population)
    var_smp = np.var(x, ddof=1)      # divide by n - 1  (sample, Bessel's correction)
    sd = np.std(x, ddof=1)
    print(f"{name}: n={len(x)}  mean={x.mean():.2f}  median={np.median(x):.1f}")
    print(f"   range={x.max() - x.min()}  IQR={q3 - q1:.1f}  (Q1={q1:.1f}, Q3={q3:.1f})")
    print(f"   variance pop={var_pop:.2f}  sample={var_smp:.2f}  std(sample)={sd:.2f}")
    print(f"   coefficient of variation = {100 * sd / x.mean():.1f}%")
    print(f"   skewness={stats.skew(x):.3f}  excess kurtosis={stats.kurtosis(x):.3f}")
    print(f"   five-number summary: {x.min()}, {q1:.1f}, {np.median(x):.1f}, {q3:.1f}, {x.max()}")

summary("Rider A", rider_a)
summary("Rider B", rider_b)

# Variance by hand for Rider A, step by step
dev = rider_a - rider_a.mean()
print("\nRider A by hand: sum of squared deviations =", round(float((dev ** 2).sum()), 2),
      "-> / (n-1) =", round(float((dev ** 2).sum() / (len(rider_a) - 1)), 3))

# Empirical rule check on Rider B (how many orders within 1 standard deviation?)
m, s = rider_b.mean(), rider_b.std(ddof=1)
inside = ((rider_b >= m - s) & (rider_b <= m + s)).sum()
print(f"Rider B: {inside}/{len(rider_b)} orders lie within mean +/- 1 sd "
      f"({m - s:.1f} to {m + s:.1f} min)")

# ---- Chart: histogram and box plot side by side --------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
bins = np.arange(10, 61, 5)
ax1.hist(rider_a, bins=bins, alpha=0.75, color="#FF6B1A", label="Rider A", edgecolor="white")
ax1.hist(rider_b, bins=bins, alpha=0.6, color="#A78BFA", label="Rider B", edgecolor="white")
ax1.axvline(rider_a.mean(), color="#0A0716", linestyle="--", linewidth=1, label="both means = 30")
ax1.set_title("Same mean, different spread")
ax1.set_xlabel("delivery time (minutes)"); ax1.set_ylabel("orders"); ax1.legend()
ax2.boxplot([rider_a, rider_b], patch_artist=True,
            boxprops=dict(facecolor="#FCD34D"), medianprops=dict(color="#F43F5E", linewidth=2))
ax2.set_xticks([1, 2]); ax2.set_xticklabels(["Rider A", "Rider B"])
ax2.set_title("Box plots: IQR and whiskers"); ax2.set_ylabel("minutes")
fig.tight_layout()
fig.savefig("session-01_dispersion_shape.png", dpi=110)
print("\nSaved chart: session-01_dispersion_shape.png")
