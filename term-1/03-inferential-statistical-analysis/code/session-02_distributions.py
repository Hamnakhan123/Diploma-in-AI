"""
Session 2 · Example 3: Random variables, expectation and common distributions
-----------------------------------------------------------------------------
A random variable maps each outcome to a number. Its distribution tells us how
likely each value is. We compute E[X] and Var(X) by hand for a discrete
variable, then use scipy.stats for the Binomial, Poisson, Uniform, Normal and
Exponential distributions, and save a 4-panel chart: session-02_distributions.png

Run:  python session-02_distributions.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- 1. A discrete random variable by hand ------------------------------------------
# X = number of customers who buy something, out of the next few visitors to a stall
values = np.array([0, 1, 2, 3, 4])
probs = np.array([0.10, 0.25, 0.35, 0.20, 0.10])
assert np.isclose(probs.sum(), 1.0), "probabilities must sum to 1"
EX = (values * probs).sum()                      # E[X]   = sum x p(x)
VarX = ((values - EX) ** 2 * probs).sum()        # Var(X) = sum (x - E[X])^2 p(x)
print(f"E[X] = {EX:.2f} buyers,  Var(X) = {VarX:.4f},  SD = {np.sqrt(VarX):.4f}")
print(f"Linearity: if profit = 500*X - 200, E[profit] = 500*{EX:.2f} - 200 = {500 * EX - 200:.0f} PKR")

# ---- 2. Binomial: number of successes in n independent yes/no trials -----------------
n, p = 10, 0.3                                   # 10 calls, each converts with prob 0.3
B = stats.binom(n, p)
print(f"\nBinomial(n={n}, p={p}): mean={B.mean():.1f}, var={B.var():.2f}")
print(f"  P(X = 3) = {B.pmf(3):.4f}   P(X <= 2) = {B.cdf(2):.4f}   P(X >= 5) = {B.sf(4):.4f}")

# ---- 3. Poisson: number of events in a fixed interval (rate lambda) ------------------
lam = 4                                          # 4 orders per 10 minutes on average
Po = stats.poisson(lam)
print(f"Poisson(lambda={lam}): P(X = 0) = {Po.pmf(0):.4f}   P(X >= 8) = {Po.sf(7):.4f}")

# ---- 4. Continuous: Uniform, Normal, Exponential -------------------------------------
U = stats.uniform(loc=10, scale=20)             # bus arrives uniformly between 10 and 30 min
print(f"Uniform(10, 30): P(wait < 15) = {U.cdf(15):.3f}, mean = {U.mean():.0f}")
heights = stats.norm(loc=165, scale=7)          # adult heights in cm
print(f"Normal(165, 7): P(height > 180) = {heights.sf(180):.4f}; 90th percentile = {heights.ppf(0.90):.1f} cm")
print(f"  P(158 < H < 172) = {heights.cdf(172) - heights.cdf(158):.4f}  (the 68 % of the empirical rule)")
E = stats.expon(scale=2.5)                       # time between orders, mean 2.5 minutes
print(f"Exponential(mean 2.5): P(gap > 5 min) = {E.sf(5):.4f}")

# ---- 5. Chart ----------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
k = np.arange(0, 11)
axes[0, 0].bar(k, B.pmf(k), color="#FF6B1A"); axes[0, 0].set_title("Binomial(n=10, p=0.3)  PMF")
k2 = np.arange(0, 13)
axes[0, 1].bar(k2, Po.pmf(k2), color="#A78BFA"); axes[0, 1].set_title("Poisson(lambda=4)  PMF")
xs = np.linspace(140, 190, 300)
axes[1, 0].plot(xs, heights.pdf(xs), color="#F43F5E", lw=2)
mask = (xs > 158) & (xs < 172)
axes[1, 0].fill_between(xs[mask], heights.pdf(xs[mask]), color="#FCD34D", alpha=0.6, label="mean +/- 1 sd")
axes[1, 0].set_title("Normal(165, 7)  PDF"); axes[1, 0].legend()
xe = np.linspace(0, 12, 300)
axes[1, 1].plot(xe, E.pdf(xe), color="#0A0716", lw=2); axes[1, 1].set_title("Exponential(mean 2.5)  PDF")
for ax in axes.flat:
    ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-02_distributions.png", dpi=100)
print("\nSaved chart: session-02_distributions.png")
