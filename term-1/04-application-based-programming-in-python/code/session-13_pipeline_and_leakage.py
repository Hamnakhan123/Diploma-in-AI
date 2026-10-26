"""
Session 13 · Example 3: train/test split, Pipeline + ColumnTransformer, and data leakage
--------------------------------------------------------------------------------------
Rule: learn every preprocessing step (medians, scaling, categories) from the
TRAINING data only, then apply the same learned steps to the test data.
A scikit-learn Pipeline does this automatically.
Run:  python session-13_pipeline_and_leakage.py
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(13)
n = 500
df = pd.DataFrame({
    "age": rng.integers(18, 65, n).astype(float),
    "income_k": rng.lognormal(4.2, 0.4, n).round(1),
    "city": rng.choice(["Karachi", "Lahore", "Islamabad", "Peshawar"], n, p=[0.45, 0.3, 0.15, 0.1]),
    "visits": rng.poisson(4, n).astype(float),
})
logit = -6 + 0.04 * df["age"] + 0.03 * df["income_k"] + 0.25 * df["visits"] + (df["city"] == "Islamabad") * 0.8
df["bought"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
for col, k in [("age", 30), ("income_k", 25), ("city", 20)]:           # punch random holes
    df.loc[rng.choice(n, k, replace=False), col] = np.nan
print(df.head(), "\nmissing:", df.isna().sum().to_dict(), "| bought rate:", round(df["bought"].mean(), 2))

X, y = df.drop(columns="bought"), df["bought"]
# 1. Split FIRST. stratify keeps the same class balance in both parts; random_state = reproducible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
print(f"\ntrain {X_train.shape}, test {X_test.shape}, positive rate train {y_train.mean():.2f} / test {y_test.mean():.2f}")

# 2. Different steps for different column types
numeric = ["age", "income_k", "visits"]
categorical = ["city"]
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])
model = Pipeline([("prep", preprocess), ("clf", LogisticRegression(max_iter=1000))])

# 3. fit() learns medians, means/stds, categories AND the model - from training data only
model.fit(X_train, y_train)
medians = model.named_steps["prep"].named_transformers_["num"].named_steps["impute"].statistics_
print("learned medians (train only):", {c: round(float(m), 1) for c, m in zip(numeric, medians)})
print("output feature names:", list(model.named_steps["prep"].get_feature_names_out()))
print(f"test accuracy: {model.score(X_test, y_test):.3f}")
print(f"5-fold cross-validation accuracy: {cross_val_score(model, X, y, cv=5).mean():.3f}")

# 4. New data with an unseen city and missing values goes through the SAME steps
new = pd.DataFrame({"age": [np.nan, 40], "income_k": [90, np.nan], "city": ["Quetta", "Islamabad"], "visits": [6, 2]})
print("\nnew customers:\n", new)
print("predicted probability of buying:", model.predict_proba(new)[:, 1].round(2).tolist())

# 5. Data leakage demo: a 'feature' that secretly contains the answer
leaky = X.copy()
leaky["discount_code_used"] = y.values * (rng.random(n) < 0.9)       # only known AFTER the purchase!
Xl_tr, Xl_te, yl_tr, yl_te = train_test_split(leaky, y, test_size=0.25, stratify=y, random_state=42)
leak_model = Pipeline([("prep", ColumnTransformer([("num", preprocess.transformers[0][1], numeric + ["discount_code_used"]),
                                                   ("cat", preprocess.transformers[1][1], categorical)])),
                       ("clf", LogisticRegression(max_iter=1000))]).fit(Xl_tr, yl_tr)
print(f"\nwith a LEAKY feature, test accuracy jumps to {leak_model.score(Xl_te, yl_te):.3f} "
      "- too good to be true, and useless for real predictions")
