"""
Session 13 · Real-life problem: preparing messy loan applications for a model
-----------------------------------------------------------------------------
PROBLEM
A microfinance team wants to predict whether an applicant will repay.
Their export is messy: income written as text ("85,000"), employment typed
in different ways ("Salaried", "salaried ", "SALARIED"), impossible ages,
missing values and a highly skewed loan amount. Your job:
  1. audit data quality and fix the obvious errors,
  2. engineer useful features (debt-to-income ratio, log of the loan amount),
  3. build ONE preprocessing pipeline (impute, scale, one-hot),
  4. show that proper preprocessing beats a naive approach on the SAME model,
  5. chart the effect.
The dataset is synthetic (seeded) so results are reproducible.
Run:  python session-13_problem_loan_preprocessing.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(31)
n = 800
age = rng.integers(21, 60, n)
income = rng.lognormal(11.2, 0.45, n)                                      # monthly income, Rs
employment = rng.choice(["Salaried", "Business", "Daily wage"], n, p=[0.5, 0.3, 0.2])
loan = rng.lognormal(12.0, 0.7, n)
dti = loan / (income * 12)
score = 1.6 - 6.0 * dti + 0.04 * (age - 35) + np.where(employment == "Salaried", 1.0, 0) - np.where(employment == "Daily wage", 1.2, 0)
repaid = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)
raw = pd.DataFrame({
    "age": age.astype(float),
    "monthly_income": [f"{v:,.0f}" for v in income],                       # numbers stored as text!
    "employment": [e if rng.random() > 0.3 else rng.choice([e.lower() + " ", e.upper()]) for e in employment],
    "loan_amount": loan.round(-2),
    "repaid": repaid,
})
raw.loc[rng.choice(n, 6, replace=False), "age"] = rng.choice([0, 150, 999], 6)   # typos
raw.loc[rng.choice(n, 40, replace=False), "monthly_income"] = np.nan
raw.loc[rng.choice(n, 25, replace=False), "employment"] = np.nan

print("=== 1. data-quality audit ===")
print("dtypes:", raw.dtypes.astype(str).to_dict())
print("missing:", raw.isna().sum().to_dict())
print("employment spellings:", {str(k): v for k, v in raw["employment"].value_counts(dropna=False).items()})
print("impossible ages:", sorted(raw.loc[(raw["age"] < 18) | (raw["age"] > 100), "age"].unique().tolist()))
print(f"loan_amount skewness: {raw['loan_amount'].skew():.2f}")

df = raw.copy()
df["monthly_income"] = pd.to_numeric(df["monthly_income"].str.replace(",", ""), errors="coerce")
df["employment"] = df["employment"].str.strip().str.title()
df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = np.nan                  # treat typos as missing
df["dti"] = df["loan_amount"] / (df["monthly_income"] * 12)                     # debt-to-income ratio
df["log_loan"] = np.log(df["loan_amount"])
print("\n=== 2. after fixing and engineering ===")
print("employment now:", {str(k): v for k, v in df["employment"].value_counts(dropna=False).items()})
print(df[["age", "monthly_income", "loan_amount", "dti", "log_loan"]].describe().round(2).loc[["mean", "50%", "max"]])

X, y = df.drop(columns="repaid"), df["repaid"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)

# Naive approach: raw numeric columns, missing rows filled with 0, no scaling, no categories
naive_cols = ["age", "monthly_income", "loan_amount"]
naive = KNeighborsClassifier(n_neighbors=15).fit(X_tr[naive_cols].fillna(0), y_tr)
acc_naive = naive.score(X_te[naive_cols].fillna(0), y_te)
from sklearn.model_selection import cross_val_score
cv_naive = cross_val_score(KNeighborsClassifier(n_neighbors=15), X[naive_cols].fillna(0), y, cv=5).mean()

# Proper approach: engineered features + impute + scale + one-hot, all inside a pipeline
num = ["age", "monthly_income", "log_loan", "dti"]
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), ["employment"]),
])
proper = Pipeline([("prep", prep), ("knn", KNeighborsClassifier(n_neighbors=15))]).fit(X_tr, y_tr)
acc_proper = proper.score(X_te, y_te)
cv_proper = cross_val_score(Pipeline([("prep", prep), ("knn", KNeighborsClassifier(n_neighbors=15))]), X, y, cv=5).mean()
baseline = max(y_te.mean(), 1 - y_te.mean())

print("\n=== 3. same model (k-NN, k = 15), different preprocessing ===")
print(f"always guess the majority class : {baseline:.3f}")
print(f"naive (fill 0, no scaling)      : {acc_naive:.3f}   5-fold CV {cv_naive:.3f}")
print(f"proper pipeline                 : {acc_proper:.3f}   5-fold CV {cv_proper:.3f}")

fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
bars = ax[0].bar(["majority\nguess", "naive", "proper\npipeline"], [baseline, acc_naive, acc_proper],
                 color=["#6B7280", "#F43F5E", "#FF6B1A"])
ax[0].bar_label(bars, fmt="%.3f"); ax[0].set_ylim(0, 1); ax[0].set_title("Test accuracy, same k-NN model")
ax[1].hist(df["dti"].dropna().clip(upper=3), bins=30, color="#A78BFA")
ax[1].set_title("Engineered feature: debt-to-income ratio"); ax[1].set_xlabel("loan / yearly income (capped at 3)")
fig.tight_layout(); fig.savefig("session-13_problem_loan_preprocessing.png", dpi=100)
print("Saved session-13_problem_loan_preprocessing.png")
