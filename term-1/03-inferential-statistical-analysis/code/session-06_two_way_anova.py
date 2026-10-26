"""
Session 6 · Example 3: Two-way ANOVA (two-way classification) with interaction
-----------------------------------------------------------------------------
Crop yield (kg per plot) for 3 fertilisers x 2 irrigation methods, 4 plots per
combination. Two-way ANOVA tests:
   * main effect of fertiliser
   * main effect of irrigation
   * the INTERACTION (does the best fertiliser depend on irrigation?)
Also shown: two-way ANOVA WITHOUT replication (one value per cell, no
interaction term), and an interaction plot: session-06_two_way_anova.png

Run:  python session-06_two_way_anova.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = []
cell_means = {("F1", "Drip"): 30, ("F2", "Drip"): 36, ("F3", "Drip"): 34,
              ("F1", "Flood"): 28, ("F2", "Flood"): 29, ("F3", "Flood"): 35}
offsets = [-1.5, 0.5, 1.2, -0.2]                 # fixed within-cell variation (deterministic)
for (fert, irr), m in cell_means.items():
    for i, o in enumerate(offsets):
        rows.append({"fertiliser": fert, "irrigation": irr, "yield_kg": m + o + 0.3 * (i % 2)})
df = pd.DataFrame(rows)

print("Cell means (kg):")
print(df.pivot_table(values="yield_kg", index="fertiliser", columns="irrigation", aggfunc="mean").round(2).to_string())

model = smf.ols("yield_kg ~ C(fertiliser) * C(irrigation)", data=df).fit()
table = sm.stats.anova_lm(model, typ=2)
table["eta_sq"] = table["sum_sq"] / table["sum_sq"].sum()
print("\nTwo-way ANOVA with interaction (Type II sums of squares)")
print(table.assign(**{"PR(>F)": lambda t: t["PR(>F)"].map(lambda v: "" if v != v else f"{v:.2e}")}).round(4).to_string())

# Without replication: one observation per cell (e.g. 4 shops x 3 weeks of sales)
sales = pd.DataFrame({"shop": np.repeat(["S1", "S2", "S3", "S4"], 3),
                      "week": ["W1", "W2", "W3"] * 4,
                      "sales": [52, 58, 61, 47, 50, 56, 60, 66, 70, 45, 49, 53]})
m2 = smf.ols("sales ~ C(shop) + C(week)", data=sales).fit()
print("\nTwo-way ANOVA without replication (no interaction term possible)")
print(sm.stats.anova_lm(m2, typ=2).assign(**{"PR(>F)": lambda t: t["PR(>F)"].map(lambda v: "" if v != v else f"{v:.2e}")}).round(4).to_string())

fig, ax = plt.subplots(figsize=(7, 4))
means = df.groupby(["fertiliser", "irrigation"]).yield_kg.mean().unstack()
for irr, c in zip(means.columns, ["#FF6B1A", "#A78BFA"]):
    ax.plot(means.index, means[irr], marker="o", color=c, lw=2, label=irr)
ax.set_xlabel("fertiliser"); ax.set_ylabel("mean yield (kg)")
ax.set_title("Interaction plot: crossing lines = interaction"); ax.legend(title="irrigation"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-06_two_way_anova.png", dpi=100)
print("Saved chart: session-06_two_way_anova.png")
