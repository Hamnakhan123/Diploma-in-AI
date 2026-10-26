"""
Session 13 · Example 1: missing values and categorical encoding
---------------------------------------------------------------
Machine-learning models need a complete, NUMERIC table. This example
shows how to (1) find and fill missing values and (2) turn text categories
into numbers with pandas and scikit-learn.
Run:  python session-13_missing_and_encoding.py
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder

pd.set_option("display.width", 140); pd.set_option("display.max_columns", 20)
df = pd.DataFrame({
    "age":       [24, 31, np.nan, 45, 29, 38, np.nan, 52],
    "income_k":  [55, 80, 62, np.nan, 48, 120, 70, 95],          # monthly income, thousand Rs
    "city":      ["Karachi", "Lahore", "Karachi", np.nan, "Islamabad", "Karachi", "Lahore", "Karachi"],
    "education": ["Bachelors", "Masters", "Intermediate", "Masters", "Bachelors", "PhD", "Bachelors", np.nan],
    "bought":    ["no", "yes", "no", "yes", "no", "yes", "no", "yes"],   # the target to predict
})
print("raw data:\n", df, "\n")

# 1. Detect missing values
print("missing per column:", df.isna().sum().to_dict())
print(f"rows with any missing value: {df.isna().any(axis=1).sum()} of {len(df)}")

# 2. Option A: drop (only when few rows are affected and they are missing at random)
print("dropna would keep", len(df.dropna()), "rows - too much data lost here")

# 3. Option B: impute. Numbers -> median (robust to outliers); categories -> most frequent
num_cols, cat_cols = ["age", "income_k"], ["city", "education"]
filled = df.copy()
filled[num_cols] = SimpleImputer(strategy="median").fit_transform(df[num_cols])
filled[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])
print("medians used:", df[num_cols].median().to_dict(), "| modes used:", df[cat_cols].mode().iloc[0].to_dict())
# A missing-indicator column keeps the information that a value WAS missing
filled["age_was_missing"] = df["age"].isna().astype(int)
print("\nafter imputation:\n", filled, "\n")

# 4. Encoding categories
# 4a. NOMINAL (no order): one-hot encoding -> one 0/1 column per category
print("pandas get_dummies:\n", pd.get_dummies(filled["city"], prefix="city", dtype=int).head(4), "\n")
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
city_matrix = ohe.fit_transform(filled[["city"]])
print("OneHotEncoder categories:", ohe.categories_[0].tolist())
print("unknown city 'Quetta' encodes to:", ohe.transform(pd.DataFrame({"city": ["Quetta"]})).tolist(), "(all zeros, no crash)")

# 4b. ORDINAL (natural order): map to ordered integers
levels = [["Intermediate", "Bachelors", "Masters", "PhD"]]
filled["education_level"] = OrdinalEncoder(categories=levels).fit_transform(filled[["education"]]).ravel()
print("\neducation -> level:", dict(zip(filled["education"], filled["education_level"])))

# 4c. TARGET labels: LabelEncoder (for y only)
le = LabelEncoder()
y = le.fit_transform(filled["bought"])
print("target classes:", le.classes_.tolist(), "-> y =", y.tolist())

# 5. The final all-numeric feature matrix X
X = pd.concat([filled[["age", "income_k", "age_was_missing", "education_level"]],
               pd.DataFrame(city_matrix, columns=ohe.get_feature_names_out(), index=filled.index)], axis=1)
print("\nfeature matrix X:", X.shape, "\n", X.round(1))
