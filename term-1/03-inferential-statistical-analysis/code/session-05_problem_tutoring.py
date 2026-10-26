"""
Session 5 · Real-life problem: did the peer-tutoring programme work?
-------------------------------------------------------------------
PROBLEM
A department ran a 6-week peer-tutoring programme for first-year programming
students. It has:
  * pre-test and post-test scores for the same 15 tutored students
  * final exam scores for 15 tutored and 14 non-tutored students
  * a pass/fail table by group
Questions (alpha = 0.05):
  1. Did tutored students improve from pre-test to post-test?      -> paired t test
  2. Did tutored students score higher in the final exam?          -> one-sided Welch t test
  3. Is passing associated with being tutored?                     -> chi-square independence
  4. Report effect sizes and a one-paragraph recommendation.
Assumption checks (Shapiro-Wilk normality of differences, Levene) are included.

Run:  python session-05_problem_tutoring.py
"""
import numpy as np
from scipy import stats

pre = np.array([42, 55, 38, 61, 47, 50, 35, 58, 44, 52, 40, 63, 49, 46, 54])
post = np.array([51, 60, 47, 66, 55, 54, 45, 61, 52, 58, 46, 70, 53, 55, 59])
final_tut = np.array([68, 74, 61, 80, 70, 66, 58, 77, 69, 72, 63, 84, 71, 67, 75])
final_not = np.array([62, 70, 55, 66, 59, 73, 52, 64, 61, 58, 68, 57, 65, 60])
passfail = np.array([[13, 2],     # tutored:     pass, fail
                     [9, 5]])     # not tutored: pass, fail

# 1. Paired t test
d = post - pre
sw = stats.shapiro(d)
r1 = stats.ttest_rel(post, pre)
dz = d.mean() / d.std(ddof=1)
print("1) Pre vs post (same students)")
print(f"   mean gain {d.mean():.2f} points, Shapiro p = {sw.pvalue:.3f} (differences look normal)")
print(f"   t = {r1.statistic:.3f}, p = {r1.pvalue:.2e}, effect size d_z = {dz:.2f}")
ci = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=d.std(ddof=1) / np.sqrt(len(d)))
print(f"   95% CI for the gain: [{ci[0]:.2f}, {ci[1]:.2f}]")

# 2. Welch t test, one-sided (tutored > not tutored)
lev = stats.levene(final_tut, final_not)
r2 = stats.ttest_ind(final_tut, final_not, equal_var=False, alternative="greater")
sp = np.sqrt(((len(final_tut) - 1) * final_tut.var(ddof=1) + (len(final_not) - 1) * final_not.var(ddof=1))
             / (len(final_tut) + len(final_not) - 2))
d2 = (final_tut.mean() - final_not.mean()) / sp
print("\n2) Final exam: tutored vs not tutored")
print(f"   means {final_tut.mean():.2f} vs {final_not.mean():.2f}; Levene p = {lev.pvalue:.3f}")
print(f"   Welch t = {r2.statistic:.3f}, one-sided p = {r2.pvalue:.4f}, Cohen's d = {d2:.2f}")

# 3. Chi-square (with Fisher's exact test because some expected counts are < 5)
c2, p3, dof, exp = stats.chi2_contingency(passfail)
print("\n3) Pass/fail by group")
print("   expected counts:", exp.round(2).tolist())
print(f"   chi2 (Yates corrected) = {c2:.3f}, p = {p3:.4f}")
print(f"   Fisher's exact p = {stats.fisher_exact(passfail).pvalue:.4f}  (preferred: expected counts below 5)")

# 4. Recommendation
print(f"\n4) Recommendation: tutored students improved by about {d.mean():.1f} points (d_z = {dz:.1f}, very large)")
print(f"   and scored {final_tut.mean() - final_not.mean():.1f} points higher in the final exam (d = {d2:.2f}, large).")
rates = passfail[:, 0] / passfail.sum(axis=1)
print(f"   The pass-rate difference ({rates[0]:.0%} vs {rates[1]:.0%}) is not significant with groups this small.")
print("   Caveat: students CHOSE to join, so motivation may explain part of the gap; a randomised")
print("   pilot next semester would give stronger evidence. Continue and expand the programme.")
