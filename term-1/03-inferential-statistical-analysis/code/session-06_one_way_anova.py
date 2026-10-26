"""
Session 6 · Example 1: One-way ANOVA (one-way classification), by hand
---------------------------------------------------------------------
Three teaching methods were used with three groups of students. Do the mean
test scores differ?  H0: mu_lecture = mu_flipped = mu_project

We build the full ANOVA table by hand:
   SST (total) = SSB (between groups) + SSW (within groups)
   MSB = SSB / (k - 1),  MSW = SSW / (N - k),  F = MSB / MSW
then check it with scipy.stats.f_oneway, test the assumptions, compute eta
squared, and save a box plot: session-06_one_way_anova.png

Run:  python session-06_one_way_anova.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

groups = {
    "Lecture": np.array([62, 58, 65, 60, 63, 59, 61, 64]),
    "Flipped": np.array([70, 68, 74, 71, 66, 72, 69, 73]),
    "Project": np.array([66, 63, 70, 65, 68, 62, 67, 64]),
}
allx = np.concatenate(list(groups.values()))
N, k, grand = len(allx), len(groups), allx.mean()

print("Group means:", {g: round(float(x.mean()), 2) for g, x in groups.items()}, f" grand mean = {grand:.3f}")
SSB = sum(len(x) * (x.mean() - grand) ** 2 for x in groups.values())
SSW = sum(((x - x.mean()) ** 2).sum() for x in groups.values())
SST = ((allx - grand) ** 2).sum()
dfb, dfw = k - 1, N - k
MSB, MSW = SSB / dfb, SSW / dfw
F = MSB / MSW
p = stats.f.sf(F, dfb, dfw)

print("\nANOVA table")
print(f"{'Source':<16}{'SS':>10}{'df':>5}{'MS':>10}{'F':>9}{'p':>11}")
print(f"{'Between groups':<16}{SSB:>10.3f}{dfb:>5}{MSB:>10.3f}{F:>9.3f}{p:>11.2e}")
print(f"{'Within groups':<16}{SSW:>10.3f}{dfw:>5}{MSW:>10.3f}")
print(f"{'Total':<16}{SST:>10.3f}{N - 1:>5}")
print(f"Check: SSB + SSW = {SSB + SSW:.3f} = SST")
print(f"Critical F(0.95; {dfb}, {dfw}) = {stats.f.ppf(0.95, dfb, dfw):.3f}")
print("scipy f_oneway:", tuple(round(float(v), 6) for v in stats.f_oneway(*groups.values())))

eta2 = SSB / SST
print(f"\nEffect size eta^2 = SSB/SST = {eta2:.3f} -> {100 * eta2:.0f}% of score variation is explained by method")
print("Assumptions:")
for g, x in groups.items():
    print(f"   Shapiro-Wilk {g:<8} p = {stats.shapiro(x).pvalue:.3f}")
print(f"   Levene (equal variances) p = {stats.levene(*groups.values()).pvalue:.3f}")
print(f"Non-parametric check: Kruskal-Wallis p = {stats.kruskal(*groups.values()).pvalue:.5f}")

fig, ax = plt.subplots(figsize=(7, 4))
bp = ax.boxplot(list(groups.values()), patch_artist=True, medianprops=dict(color="#0A0716"))
for patch, c in zip(bp["boxes"], ["#A78BFA", "#FF6B1A", "#FCD34D"]):
    patch.set_facecolor(c)
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(list(groups))
ax.axhline(grand, color="#F43F5E", ls="--", label=f"grand mean {grand:.1f}")
ax.set_ylabel("test score"); ax.set_title(f"One-way ANOVA: F = {F:.1f}, p = {p:.1e}"); ax.legend()
fig.tight_layout(); fig.savefig("session-06_one_way_anova.png", dpi=100)
print("Saved chart: session-06_one_way_anova.png")
