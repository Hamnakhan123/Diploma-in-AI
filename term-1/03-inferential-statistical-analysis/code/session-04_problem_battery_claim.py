"""
Session 4 · Real-life problem: testing a power-bank seller's claim
-----------------------------------------------------------------
PROBLEM
An online seller claims its 10,000 mAh power bank gives AT LEAST 20 hours of
phone use on average, and that NO MORE than 5% of units are faulty.
A university tech club tests 40 units:
  * hours of use (data below)
  * 5 of the 40 units were faulty
At alpha = 0.05:
  1. Is there evidence that mean battery life is LESS than 20 hours? (one-tailed t)
  2. Is there evidence that the fault rate is MORE than 5%?        (one-tailed z for a proportion,
     plus an exact binomial test because n*p0 = 2 is small)
  3. Give 95% confidence intervals for both.
  4. Write a short, non-technical verdict.

Run:  python session-04_problem_battery_claim.py
"""
import numpy as np
from scipy import stats

hours = np.array([19.2, 20.5, 18.7, 19.9, 21.1, 18.4, 19.6, 20.2, 18.9, 19.4,
                  20.8, 19.1, 18.6, 19.8, 20.1, 19.3, 18.8, 21.0, 19.5, 19.0,
                  20.4, 18.5, 19.7, 20.0, 19.2, 18.9, 20.6, 19.4, 19.1, 20.3,
                  18.7, 19.9, 19.6, 20.9, 18.8, 19.3, 20.2, 19.0, 19.5, 18.6])
alpha = 0.05

# ---- 1. Mean battery life -----------------------------------------------------------
n, xbar, s = len(hours), hours.mean(), hours.std(ddof=1)
t = (xbar - 20) / (s / np.sqrt(n))
p1 = stats.t.cdf(t, n - 1)                       # lower-tailed
print("1) H0: mu >= 20 h   vs   H1: mu < 20 h")
print(f"   n = {n}, mean = {xbar:.3f} h, sd = {s:.3f}, t = {t:.3f}, p = {p1:.5f}")
print("   ->", "reject H0: mean life is below 20 h" if p1 < alpha else "not enough evidence")
res = stats.ttest_1samp(hours, 20, alternative="less")
print(f"   scipy check: t = {res.statistic:.3f}, p = {res.pvalue:.5f}")

# ---- 2. Fault rate ---------------------------------------------------------------------
k, p0 = 5, 0.05
p_hat = k / n
z = (p_hat - p0) / np.sqrt(p0 * (1 - p0) / n)    # SE uses p0 under H0
p_z = stats.norm.sf(z)
p_exact = stats.binomtest(k, n, p0, alternative="greater").pvalue
print("\n2) H0: p <= 0.05   vs   H1: p > 0.05")
print(f"   p_hat = {p_hat:.3f}, z = {z:.3f}, normal-approx p = {p_z:.4f}")
print(f"   n*p0 = {n * p0:.0f} < 10, so the normal approximation is shaky; exact binomial p = {p_exact:.4f}")
print("   ->", "reject H0" if p_exact < alpha else "fail to reject H0: 5/40 is suspicious but not conclusive")

# ---- 3. Confidence intervals ----------------------------------------------------------
lo, hi = stats.t.interval(0.95, n - 1, loc=xbar, scale=s / np.sqrt(n))
ci_p = stats.binomtest(k, n).proportion_ci(confidence_level=0.95, method="wilson")
print(f"\n3) 95% CI mean life: [{lo:.2f}, {hi:.2f}] h")
print(f"   95% CI fault rate (Wilson): [{ci_p.low:.3f}, {ci_p.high:.3f}]")

# ---- 4. Verdict -------------------------------------------------------------------------
print(f"\n4) Verdict: average life is about {xbar:.1f} h, significantly below the advertised 20 h. "
      f"The fault rate in our sample ({p_hat:.1%}) is also significantly above 5% "
      f"(exact p = {p_exact:.3f}), but only just, and the plausible range is wide "
      f"({ci_p.low:.0%} to {ci_p.high:.0%}); test more units before a formal complaint about faults.")
