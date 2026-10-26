"""
Session 5 · Mini project: an automatic 'which test should I use?' assistant
-------------------------------------------------------------------------
Choosing the right test is the hardest part for beginners. This tool:
  * takes a description of the data (types of variables, groups, pairing)
  * checks assumptions automatically (normality with Shapiro-Wilk, equal
    variance with Levene, expected counts for chi-square)
  * picks the test (and a non-parametric fallback when assumptions fail)
  * runs it and prints a plain-English report with the effect size

Run:  python session-05_project_test_selector.py
"""
import numpy as np
from scipy import stats


def cohen_d(a, b):
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    return (np.mean(a) - np.mean(b)) / sp


def analyse(name, a=None, b=None, mu0=None, paired=False, table=None, alpha=0.05):
    print(f"\n=== {name} ===")
    if table is not None:                                         # two categorical variables
        table = np.asarray(table)
        chi2, p, dof, exp = stats.chi2_contingency(table)
        if (exp < 5).any() and table.shape == (2, 2):
            p, test = stats.fisher_exact(table).pvalue, "Fisher's exact test (expected counts < 5)"
        else:
            test = f"chi-square test of independence (df = {dof})"
        v = np.sqrt(chi2 / (table.sum() * (min(table.shape) - 1)))
        effect = f"Cramer's V = {v:.2f}"
    elif b is None:                                               # one numeric sample vs a value
        normal = stats.shapiro(a).pvalue > alpha
        if normal:
            p, test = stats.ttest_1samp(a, mu0).pvalue, "one-sample t test"
        else:
            p, test = stats.wilcoxon(np.asarray(a) - mu0).pvalue, "Wilcoxon signed-rank (data not normal)"
        effect = f"d = {(np.mean(a) - mu0) / np.std(a, ddof=1):.2f}"
    elif paired:
        diff = np.asarray(a) - np.asarray(b)
        normal = stats.shapiro(diff).pvalue > alpha
        if normal:
            p, test = stats.ttest_rel(a, b).pvalue, "paired t test"
        else:
            p, test = stats.wilcoxon(a, b).pvalue, "Wilcoxon signed-rank (differences not normal)"
        effect = f"d_z = {diff.mean() / diff.std(ddof=1):.2f}"
    else:                                                         # two independent groups
        normal = stats.shapiro(a).pvalue > alpha and stats.shapiro(b).pvalue > alpha
        equal_var = stats.levene(a, b).pvalue > alpha
        if normal:
            p = stats.ttest_ind(a, b, equal_var=equal_var).pvalue
            test = "Student's t test (equal variances)" if equal_var else "Welch's t test (unequal variances)"
        else:
            p, test = stats.mannwhitneyu(a, b).pvalue, "Mann-Whitney U (data not normal)"
        effect = f"Cohen's d = {cohen_d(a, b):.2f}"
    verdict = "significant" if p < alpha else "not significant"
    print(f"Test chosen : {test}")
    print(f"Result      : p = {p:.4g} -> {verdict} at alpha = {alpha}; {effect}")


rng = np.random.default_rng(12)
analyse("Do students sleep less than 8 h?", a=rng.normal(6.8, 1.0, 25), mu0=8)
before_cdn = rng.normal(3.2, 0.5, 20)                     # same 20 pages measured twice
after_cdn = before_cdn - rng.normal(0.4, 0.2, 20)          # each page gets a bit faster
analyse("Website load time before/after a CDN (s)", a=before_cdn, b=after_cdn, paired=True)
analyse("Delivery minutes: rider app A vs B", a=rng.normal(32, 4, 30), b=rng.normal(35, 9, 30))
analyse("Customer spending (very skewed) in two cities", a=rng.lognormal(7, 1, 40), b=rng.lognormal(7.5, 1, 40))
analyse("Gender vs choice of elective", table=[[30, 15, 25], [20, 30, 20]])
analyse("Small trial: new drug vs placebo cured", table=[[9, 1], [4, 6]])
