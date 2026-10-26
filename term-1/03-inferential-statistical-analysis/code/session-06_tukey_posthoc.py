"""
Session 6 · Example 2: Which groups differ? Post-hoc tests after ANOVA
---------------------------------------------------------------------
A significant ANOVA only says 'not all means are equal'. Post-hoc tests find
WHICH pairs differ while controlling the family-wise error rate.
  1. Why not just run three t tests? (simulation of the inflated error)
  2. Tukey's HSD with statsmodels
  3. Bonferroni-corrected pairwise t tests for comparison

Run:  python session-06_tukey_posthoc.py
"""
from itertools import combinations
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

groups = {
    "Lecture": np.array([62, 58, 65, 60, 63, 59, 61, 64]),
    "Flipped": np.array([70, 68, 74, 71, 66, 72, 69, 73]),
    "Project": np.array([66, 63, 70, 65, 68, 62, 67, 64]),
}

# 1. Multiple t tests inflate the Type I error: 5 identical groups -> 10 pairwise tests
rng = np.random.default_rng(4)
false_alarm = 0
for _ in range(2000):
    g = rng.normal(60, 5, size=(5, 10))
    if any(stats.ttest_ind(g[i], g[j]).pvalue < 0.05 for i, j in combinations(range(5), 2)):
        false_alarm += 1
print(f"1) 5 identical groups, 10 t tests at 0.05: at least one false 'difference' in "
      f"{false_alarm / 20:.1f}% of studies (ANOVA keeps it at 5%)")

# 2. Tukey HSD
scores = np.concatenate(list(groups.values()))
labels = np.repeat(list(groups), [len(v) for v in groups.values()])
tukey = pairwise_tukeyhsd(scores, labels, alpha=0.05)
print("\n2) Tukey HSD")
print(tukey.summary())

# 3. Bonferroni
pairs = list(combinations(groups, 2))
print(f"\n3) Bonferroni: compare each p with 0.05/{len(pairs)} = {0.05 / len(pairs):.4f}")
for a, b in pairs:
    p = stats.ttest_ind(groups[a], groups[b]).pvalue
    print(f"   {a} vs {b}: p = {p:.5f}, adjusted p = {min(1, p * len(pairs)):.5f} "
          f"-> {'different' if p < 0.05 / len(pairs) else 'not different'}")
