"""
Session 12 · Example 2: statistical charts with seaborn and pandas plotting
---------------------------------------------------------------------------
seaborn works directly with DataFrames: give it the table and column names.
The dataset is generated with a fixed seed (no internet download needed).
Run:  python session-12_seaborn_pandas.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(12)
n = 240
df = pd.DataFrame({
    "program": rng.choice(["AI", "Data Science", "Web Dev"], n, p=[0.4, 0.35, 0.25]),
    "shift": rng.choice(["Morning", "Evening"], n),
    "study_hours": rng.gamma(4, 2, n).round(1),
})
df["attendance"] = np.clip(rng.normal(82, 9, n), 40, 100).round(0)
df["score"] = np.clip(18 + 3.0 * df["study_hours"] + 0.3 * df["attendance"]
                      + df["program"].map({"AI": 3, "Data Science": 1, "Web Dev": -2}) + rng.normal(0, 7, n), 0, 100).round(0)
print(df.head(), "\n")
print(df.groupby("program")[["study_hours", "score"]].mean().round(1), "\n")

sns.set_theme(style="whitegrid", palette=["#FF6B1A", "#A78BFA", "#F43F5E"])
fig, axes = plt.subplots(2, 3, figsize=(13, 7))
sns.histplot(data=df, x="score", hue="program", kde=True, element="step", ax=axes[0, 0])
axes[0, 0].set_title("Distribution of scores (histogram + KDE)")
sns.boxplot(data=df, x="program", y="score", hue="shift", ax=axes[0, 1])
axes[0, 1].set_title("Box plot: score by program and shift")
sns.violinplot(data=df, x="program", y="study_hours", ax=axes[0, 2], inner="quartile")
axes[0, 2].set_title("Violin: study hours by program")
sns.scatterplot(data=df, x="study_hours", y="score", hue="program", alpha=0.7, ax=axes[1, 0])
sns.regplot(data=df, x="study_hours", y="score", scatter=False, color="black", ax=axes[1, 0])
axes[1, 0].set_title("Scatter + regression line")
sns.countplot(data=df, x="program", hue="shift", ax=axes[1, 1])
axes[1, 1].set_title("Count plot: students per group")
corr = df[["study_hours", "attendance", "score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="rocket_r", vmin=-1, vmax=1, ax=axes[1, 2])
axes[1, 2].set_title("Heatmap: correlation matrix")
fig.tight_layout(); fig.savefig("session-12_seaborn_pandas.png", dpi=95)
print("Correlation matrix:\n", corr.round(2), "\n")

# pandas has plotting built in: DataFrame.plot(kind=...)
summary = df.pivot_table(index="program", columns="shift", values="score", aggfunc="mean")
ax = summary.plot(kind="barh", figsize=(6, 3), color=["#FCD34D", "#6B7280"], title="pandas .plot(): mean score")
ax.set_xlabel("mean score"); plt.tight_layout(); plt.savefig("session-12_seaborn_pandas_pandasplot.png", dpi=100)
print("Mean score by program and shift:\n", summary.round(1))
print("\nSaved session-12_seaborn_pandas.png and session-12_seaborn_pandas_pandasplot.png")
