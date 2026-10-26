"""
Session 4 · Mini project: an A/B testing toolkit for a website
-------------------------------------------------------------
An online bookshop tests a new 'Buy now' button (B) against the old one (A).
The toolkit:
  1. plans the experiment: sample size per group for a chosen minimum effect,
     alpha and power (normal-approximation formula)
  2. analyses the results: two-proportion z test, p-value, 95% CI for the lift
  3. double-checks with a permutation test (no formulas, just shuffling)
  4. shows the danger of 'peeking' (stopping as soon as p < 0.05) by simulation
  5. saves a chart of the conversion rates with CIs: session-04_project_ab_test.png

Run:  python session-04_project_ab_test.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def sample_size(p1, p2, alpha=0.05, power=0.80):
    """Visitors needed PER GROUP to detect p1 -> p2 with a two-sided test."""
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    pbar = (p1 + p2) / 2
    num = (za * np.sqrt(2 * pbar * (1 - pbar)) + zb * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return int(np.ceil(num / (p1 - p2) ** 2))

def two_prop_test(xa, na, xb, nb):
    pa, pb = xa / na, xb / nb
    pool = (xa + xb) / (na + nb)
    se0 = np.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))          # SE under H0 (pooled)
    z = (pb - pa) / se0
    p = 2 * stats.norm.sf(abs(z))
    se = np.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)           # SE for the CI (unpooled)
    diff = pb - pa
    return pa, pb, z, p, (diff - 1.96 * se, diff + 1.96 * se)

# 1. Plan
n_needed = sample_size(0.040, 0.050)
print(f"1) To detect 4.0% -> 5.0% with alpha 0.05 and power 0.80: {n_needed:,} visitors per group")

# 2. Analyse (results after running the test with that many visitors)
na = nb = 6800
xa, xb = 272, 343
pa, pb, z, p, ci = two_prop_test(xa, na, xb, nb)
print(f"\n2) A: {xa}/{na} = {pa:.2%}   B: {xb}/{nb} = {pb:.2%}")
print(f"   z = {z:.3f}, p = {p:.4f}, lift = {pb - pa:+.2%} (95% CI {ci[0]:+.2%} to {ci[1]:+.2%}), "
      f"relative lift = {(pb / pa - 1):+.1%}")
print("   ->", "B is significantly better: ship it" if p < 0.05 and ci[0] > 0 else "no clear winner")

# 3. Permutation test
rng = np.random.default_rng(0)
outcomes = np.r_[np.ones(xa + xb), np.zeros(na + nb - xa - xb)]
observed = pb - pa
diffs = np.empty(2000)
for i in range(2000):
    rng.shuffle(outcomes)
    diffs[i] = outcomes[:nb].mean() - outcomes[nb:].mean()
print(f"\n3) Permutation test: p = {np.mean(np.abs(diffs) >= abs(observed)):.4f} (2,000 shuffles)")

# 4. The peeking problem: A and B are IDENTICAL (4% each), but we check after every 500 visitors
false_wins = 0
for _ in range(1000):
    a = rng.random(10_000) < 0.04
    b = rng.random(10_000) < 0.04
    for m in range(500, 10_001, 500):
        if two_prop_test(a[:m].sum(), m, b[:m].sum(), m)[3] < 0.05:
            false_wins += 1
            break
print(f"\n4) Peeking 20 times when there is NO real difference: false 'winner' in {false_wins / 10:.1f}% "
      f"of experiments (should be 5%)")

# 5. Chart
fig, ax = plt.subplots(figsize=(6, 4))
rates = [pa, pb]
errs = [1.96 * np.sqrt(r * (1 - r) / n) for r, n in zip(rates, [na, nb])]
ax.bar(["A (old button)", "B (new button)"], [100 * r for r in rates], yerr=[100 * e for e in errs],
       color=["#A78BFA", "#FF6B1A"], capsize=8)
ax.set_ylabel("conversion rate (%)"); ax.set_title(f"A/B test: p = {p:.4f}")
for i, r in enumerate(rates):
    ax.text(i, 100 * r / 2, f"{r:.2%}", ha="center", color="white", fontweight="bold")
fig.tight_layout(); fig.savefig("session-04_project_ab_test.png", dpi=100)
print("Saved chart: session-04_project_ab_test.png")
