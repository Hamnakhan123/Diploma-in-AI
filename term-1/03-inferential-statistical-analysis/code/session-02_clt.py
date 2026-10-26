"""
Session 2 · Example 4: The Central Limit Theorem, seen with your own eyes
------------------------------------------------------------------------
Population: waiting times at a bank, which are strongly RIGHT-SKEWED
(exponential with mean 8 minutes). We draw thousands of samples of size
n = 2, 5, 30 and look at the distribution of the SAMPLE MEANS.

CLT: whatever the population shape, the sample mean is approximately
Normal(mu, sigma / sqrt(n)) when n is large enough (n >= 30 is a common rule).
Chart saved to: session-02_clt.png

Run:  python session-02_clt.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
mu = sigma = 8.0                    # for an exponential distribution, sd = mean
reps = 10_000

print(f"Population: exponential, mean {mu}, sd {sigma}, skewness 2.0")
print(f"{'n':>4} {'mean of means':>14} {'sd of means':>12} {'sigma/sqrt(n)':>14} {'skewness':>9}")
fig, axes = plt.subplots(1, 4, figsize=(14, 3.4))
pop = rng.exponential(mu, size=reps)
axes[0].hist(pop, bins=60, color="#A78BFA", density=True)
axes[0].set_title("Population (skewed)")
for ax, n in zip(axes[1:], [2, 5, 30]):
    means = rng.exponential(mu, size=(reps, n)).mean(axis=1)
    print(f"{n:>4} {means.mean():>14.3f} {means.std(ddof=1):>12.3f} {sigma / np.sqrt(n):>14.3f} "
          f"{stats.skew(means):>9.3f}")
    ax.hist(means, bins=60, density=True, color="#FF6B1A", alpha=0.8)
    xs = np.linspace(means.min(), means.max(), 200)
    ax.plot(xs, stats.norm.pdf(xs, mu, sigma / np.sqrt(n)), color="#0A0716", lw=1.5, label="CLT normal")
    ax.set_title(f"Means of n = {n}"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig("session-02_clt.png", dpi=100)

# Using the CLT: probability that the AVERAGE wait of 36 customers exceeds 10 minutes
se = sigma / np.sqrt(36)
z = (10 - mu) / se
print(f"\nP(mean wait of 36 customers > 10 min) ~ P(Z > {z:.2f}) = {stats.norm.sf(z):.4f}")
sim = rng.exponential(mu, size=(reps, 36)).mean(axis=1)
print(f"Simulation check: {np.mean(sim > 10):.4f}")
print("Saved chart: session-02_clt.png")
