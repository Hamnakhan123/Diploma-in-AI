"""
Session 5 · Example 2: The three t tests
---------------------------------------
1. One-sample t test   - is the mean equal to a target value?
2. Independent two-sample t test (Student's pooled and Welch's) - do two groups differ?
3. Paired t test       - did the same people change between 'before' and 'after'?
Each test is done by hand and checked with SciPy. Cohen's d is reported as
the effect size. Chart of t vs normal tails: session-05_t_tests.png

Run:  python session-05_t_tests.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- 1. One-sample: average sleep of 10 students vs the recommended 8 h -------------
sleep = np.array([6.5, 7.0, 5.5, 8.0, 6.0, 7.5, 6.5, 5.0, 7.0, 6.5])
t1 = (sleep.mean() - 8) / (sleep.std(ddof=1) / np.sqrt(len(sleep)))
print(f"1) One-sample: mean = {sleep.mean():.2f} h, t = {t1:.3f}, df = {len(sleep) - 1}, "
      f"p = {2 * stats.t.sf(abs(t1), len(sleep) - 1):.5f}")
print("   scipy:", round(float(stats.ttest_1samp(sleep, 8).pvalue), 5))

# ---- 2. Independent: marks with online vs classroom teaching -------------------------
online = np.array([68, 72, 65, 70, 74, 69, 71, 66, 73, 67, 70, 72])
classroom = np.array([75, 78, 72, 80, 74, 77, 79, 73, 76, 81])
n1, n2 = len(online), len(classroom)
m1, m2 = online.mean(), classroom.mean()
v1, v2 = online.var(ddof=1), classroom.var(ddof=1)
sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)            # pooled variance
t_pooled = (m1 - m2) / np.sqrt(sp2 * (1 / n1 + 1 / n2))
se_w = np.sqrt(v1 / n1 + v2 / n2)                                  # Welch: no equal-variance assumption
t_welch = (m1 - m2) / se_w
df_w = se_w ** 4 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))   # Welch-Satterthwaite df
d = (m1 - m2) / np.sqrt(sp2)
print(f"\n2) Independent: online mean {m1:.2f}, classroom mean {m2:.2f}")
print(f"   Student (pooled): t = {t_pooled:.3f}, df = {n1 + n2 - 2}, "
      f"p = {2 * stats.t.sf(abs(t_pooled), n1 + n2 - 2):.6f}")
print(f"   Welch:            t = {t_welch:.3f}, df = {df_w:.2f}, p = {2 * stats.t.sf(abs(t_welch), df_w):.6f}")
print(f"   scipy Welch p = {stats.ttest_ind(online, classroom, equal_var=False).pvalue:.6f}")
print(f"   Levene test for equal variances: p = {stats.levene(online, classroom).pvalue:.3f}")
print(f"   Cohen's d = {d:.2f}  (0.2 small, 0.5 medium, 0.8 large)")

# ---- 3. Paired: typing speed (wpm) before and after a 2-week course ---------------
before = np.array([32, 41, 28, 35, 45, 30, 38, 33, 40, 29])
after = np.array([38, 44, 35, 37, 52, 36, 41, 39, 43, 33])
diff = after - before
t3 = diff.mean() / (diff.std(ddof=1) / np.sqrt(len(diff)))
print(f"\n3) Paired: mean gain = {diff.mean():.1f} wpm, sd of gains = {diff.std(ddof=1):.3f}, t = {t3:.3f}, "
      f"p = {2 * stats.t.sf(abs(t3), len(diff) - 1):.7f}")
print(f"   scipy ttest_rel p = {stats.ttest_rel(after, before).pvalue:.7f}")
wrong = stats.ttest_ind(after, before).pvalue
print(f"   WRONG analysis (treating them as independent groups): p = {wrong:.4f}  <- pairing matters!")

# ---- Chart: t distributions vs the standard normal --------------------------------
xs = np.linspace(-4, 4, 400)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(xs, stats.norm.pdf(xs), color="#0A0716", lw=2, label="standard normal (z)")
for dfv, c in [(2, "#F43F5E"), (5, "#FF6B1A"), (30, "#A78BFA")]:
    ax.plot(xs, stats.t.pdf(xs, dfv), color=c, ls="--", label=f"t, df = {dfv}")
ax.set_title("t distributions have heavier tails for small samples"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-05_t_tests.png", dpi=100)
print("\nCritical values (two-tailed 5%): z = 1.960, " +
      ", ".join(f"t(df={k}) = {stats.t.ppf(0.975, k):.3f}" for k in (2, 5, 30)))
print("Saved chart: session-05_t_tests.png")
