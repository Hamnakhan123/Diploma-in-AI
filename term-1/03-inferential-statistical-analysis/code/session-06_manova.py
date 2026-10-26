"""
Session 6 · Example 4: MANOVA - several outcomes at once
-------------------------------------------------------
Three study programmes are compared on TWO outcomes measured on the same
students: exam score and project score. MANOVA tests whether the vector of
means (exam, project) differs between programmes, using the correlation
between the outcomes. We report Wilks' lambda, Pillai's trace and friends,
then follow up with one univariate ANOVA per outcome.

Run:  python session-06_manova.py
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

rng = np.random.default_rng(17)
centres = {"Evening": (62, 70), "Weekend": (64, 64), "Regular": (70, 72)}
cov = [[25, 12], [12, 25]]                         # exam and project scores are correlated
frames = []
for prog, mu in centres.items():
    xy = rng.multivariate_normal(mu, cov, size=15).round(1)
    frames.append(pd.DataFrame({"programme": prog, "exam": xy[:, 0], "project": xy[:, 1]}))
df = pd.concat(frames, ignore_index=True)

print("Means by programme")
print(df.groupby("programme")[["exam", "project"]].mean().round(2).to_string())
print(f"Correlation between exam and project: {df.exam.corr(df.project):.2f}")

mv = MANOVA.from_formula("exam + project ~ programme", data=df)
res = mv.mv_test()
stat = res.results["programme"]["stat"]
print("\nMANOVA (effect: programme)")
print(stat.round(4).to_string())

print("\nFollow-up univariate ANOVAs")
for dv in ["exam", "project"]:
    t = sm.stats.anova_lm(smf.ols(f"{dv} ~ C(programme)", data=df).fit(), typ=2)
    print(f"   {dv:<8} F = {t.loc['C(programme)', 'F']:.3f}, p = {t.loc['C(programme)', 'PR(>F)']:.5f}")
