"""
Session 13 · Mini project: a reusable data-preparation toolkit
--------------------------------------------------------------
Three functions you can reuse on ANY tabular dataset:
  quality_report(df)            -> one row per column: type, missing %, unique values, a suggestion
  build_preprocessor(df, target)-> a ColumnTransformer chosen automatically from the column types
  save / load                   -> persist the FITTED pipeline with joblib, reload it later and
                                   transform brand-new rows exactly the same way
Demonstrated on a synthetic customer-churn table for a mobile network.
Run:  python session-13_project_prep_toolkit.py
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

pd.set_option("display.width", 140)

def quality_report(df, target=None):
    """Summarise every column and suggest a preprocessing step."""
    rows = []
    for col in df.columns:
        s = df[col]
        missing = s.isna().mean() * 100
        numeric = pd.api.types.is_numeric_dtype(s)
        if col == target:
            tip = "target: never transform with the features"
        elif s.nunique() == len(s):
            tip = "drop: unique ID, no pattern to learn"
        elif not numeric:
            tip = "one-hot encode" if s.nunique() <= 15 else "too many categories: group rare ones"
        elif abs(s.skew()) > 1:
            tip = "skewed: consider log transform, then scale"
        else:
            tip = "scale"
        if missing > 40:
            tip = "mostly missing: consider dropping"
        elif missing > 0:
            tip = ("impute median, " if numeric else "impute mode, ") + tip
        rows.append({"column": col, "dtype": str(s.dtype), "missing_%": round(missing, 1),
                     "unique": s.nunique(), "suggestion": tip})
    return pd.DataFrame(rows)

def build_preprocessor(df, target, drop=()):
    """Pick numeric and categorical columns automatically and wire up the right steps."""
    features = df.drop(columns=[target, *drop])
    num = features.select_dtypes("number").columns.tolist()
    cat = features.select_dtypes(exclude="number").columns.tolist()
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), num),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=0.02))]), cat),
    ]), num, cat

# ---------- demo dataset ----------
rng = np.random.default_rng(77)
n = 1000
df = pd.DataFrame({
    "customer_id": [f"C{100000 + i}" for i in range(n)],
    "tenure_months": rng.integers(1, 72, n).astype(float),
    "monthly_bill": rng.lognormal(7.2, 0.5, n).round(0),
    "data_gb": rng.gamma(2, 6, n).round(1),
    "complaints": rng.poisson(0.8, n).astype(float),
    "package": rng.choice(["Prepaid", "Postpaid", "Business"], n, p=[0.6, 0.3, 0.1]),
    "region": rng.choice(["Sindh", "Punjab", "KP", "Balochistan", "ICT"], n, p=[0.3, 0.4, 0.15, 0.05, 0.1]),
    "referral_note": np.where(rng.random(n) < 0.7, None, "friend"),
})
z = -0.5 - 0.04 * df["tenure_months"] + 0.6 * df["complaints"] + (df["package"] == "Prepaid") * 0.9
df["churned"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
df.loc[rng.choice(n, 60, replace=False), "monthly_bill"] = np.nan
df.loc[rng.choice(n, 30, replace=False), "region"] = np.nan

print("=== quality report ===")
print(quality_report(df, target="churned").to_string(index=False))

prep, num, cat = build_preprocessor(df, "churned", drop=["customer_id", "referral_note"])
print("\nnumeric columns    :", num)
print("categorical columns:", cat)

X, y = df.drop(columns="churned"), df["churned"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))]).fit(X_tr, y_tr)
print(f"\nchurn rate {y.mean():.2f} | test accuracy {pipe.score(X_te, y_te):.3f}")
coefs = pd.Series(pipe.named_steps["model"].coef_[0], index=pipe.named_steps["prep"].get_feature_names_out())
print("strongest signals (scaled coefficients):", coefs.sort_values(key=abs, ascending=False).head(4).round(2).to_dict())

# ---------- persist the fitted pipeline and reuse it ----------
joblib.dump(pipe, "churn_pipeline.joblib")
print(f"\nsaved churn_pipeline.joblib ({os.path.getsize('churn_pipeline.joblib') / 1024:.1f} KB)")
reloaded = joblib.load("churn_pipeline.joblib")
new_customers = pd.DataFrame({
    "customer_id": ["C900001", "C900002"], "tenure_months": [3, 60], "monthly_bill": [np.nan, 2400],
    "data_gb": [25, 4], "complaints": [3, 0], "package": ["Prepaid", "Postpaid"],
    "region": ["Gilgit-Baltistan", "Punjab"], "referral_note": [None, None],
})
probs = reloaded.predict_proba(new_customers)[:, 1]
for cid, p in zip(new_customers["customer_id"], probs):
    print(f"  {cid}: churn risk {p:.0%} -> {'offer a retention discount' if p > 0.5 else 'no action'}")
print("same predictions as the original pipeline:", np.allclose(probs, pipe.predict_proba(new_customers)[:, 1]))
os.remove("churn_pipeline.joblib")
