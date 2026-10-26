"""
Session 6 · Mini project: a one-click ANOVA experiment report
------------------------------------------------------------
Give the function a DataFrame, an outcome column and one or two factor
columns. It produces a complete, publication-style report:
  * descriptive table (n, mean, sd per group)
  * assumption checks (Levene, Shapiro-Wilk on residuals)
  * one-way or two-way ANOVA table with eta squared
  * automatic switch to Welch's ANOVA or Kruskal-Wallis when assumptions fail
  * Tukey HSD for significant one-way results
  * a plain-English conclusion
Demonstrated on (a) a website-layout experiment and (b) a fertiliser x soil trial.

Run:  python session-06_project_experiment_report.py
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.oneway import anova_oneway


def anova_report(df, outcome, factors, alpha=0.05):
    print("=" * 70)
    print(f"Outcome: {outcome}   Factor(s): {', '.join(factors)}   N = {len(df)}")
    desc = df.groupby(factors)[outcome].agg(["count", "mean", "std"]).round(2)
    print(desc.to_string())
    formula = f"{outcome} ~ " + " * ".join(f"C({f})" for f in factors)
    model = smf.ols(formula, data=df).fit()
    groups = [g[outcome].values for _, g in df.groupby(factors)]
    lev_p = stats.levene(*groups).pvalue
    sh_p = stats.shapiro(model.resid).pvalue
    print(f"Assumptions: Levene p = {lev_p:.3f} ({'ok' if lev_p > alpha else 'unequal variances'}), "
          f"Shapiro residuals p = {sh_p:.3f} ({'ok' if sh_p > alpha else 'not normal'})")

    if len(factors) == 1 and sh_p <= alpha:
        r = stats.kruskal(*groups)
        print(f"Kruskal-Wallis H = {r.statistic:.3f}, p = {r.pvalue:.4g}")
        sig = r.pvalue < alpha
    elif len(factors) == 1 and lev_p <= alpha:
        r = anova_oneway(df[outcome], df[factors[0]], use_var="unequal")
        print(f"Welch's ANOVA F = {r.statistic:.3f}, p = {r.pvalue:.4g}")
        sig = r.pvalue < alpha
    else:
        table = sm.stats.anova_lm(model, typ=2)
        table["eta_sq"] = table["sum_sq"] / table["sum_sq"].sum()
        print(table.assign(**{"PR(>F)": lambda t: t["PR(>F)"].map(lambda v: "" if v != v else f"{v:.2e}")}).round(4).to_string())
        sig = (table["PR(>F)"].dropna() < alpha).any()
    if len(factors) == 1 and sig:
        print(pairwise_tukeyhsd(df[outcome], df[factors[0]], alpha=alpha).summary())

    # plain-English conclusion
    best = desc["mean"].idxmax()
    print("Conclusion:", f"at least one group differs (alpha = {alpha}); highest mean: {best}"
          if sig else "no significant differences between groups were found.")


rng = np.random.default_rng(2024)
# (a) minutes spent on a course website with three page layouts
layout = pd.DataFrame({
    "layout": np.repeat(["Classic", "Cards", "Video-first"], 20),
    "minutes": np.r_[rng.normal(6.0, 1.5, 20), rng.normal(7.4, 1.5, 20), rng.normal(7.0, 1.5, 20)].round(2),
})
anova_report(layout, "minutes", ["layout"])

# (b) wheat yield for 2 fertilisers x 3 soil types, 5 plots each
soil_effect = {"Clay": 0, "Loam": 4, "Sandy": -3}
trial = pd.DataFrame([{"fertiliser": f, "soil": s,
                       "yield_kg": 40 + soil_effect[s] + (3 if f == "Organic" and s == "Sandy" else 0)
                       + (2 if f == "Urea" else 0) + rng.normal(0, 1.5)}
                      for f in ["Urea", "Organic"] for s in soil_effect for _ in range(5)])
anova_report(trial, "yield_kg", ["fertiliser", "soil"])
