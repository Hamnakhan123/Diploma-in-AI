"""
Session 13 · Example 2: feature scaling, outliers and feature engineering
-------------------------------------------------------------------------
Run:  python session-13_scaling_outliers.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

rng = np.random.default_rng(5)
df = pd.DataFrame({
    "area_sqft": rng.normal(1200, 300, 200).round(),
    "rooms": rng.integers(1, 6, 200),
    "price_m": np.r_[rng.lognormal(3.0, 0.45, 196), [210, 260, 300, 380]].round(1),   # 4 luxury outliers
})
print("raw scales:\n", df.describe().loc[["mean", "std", "min", "max"]].round(1), "\n")

# 1. Why scale? Distance-based models (k-NN, k-means, SVM) and gradient descent
#    are dominated by the column with the biggest numbers.
a, b = df.iloc[0], df.iloc[1]
print(f"distance between rows 0 and 1: {np.linalg.norm(a - b):.1f} "
      f"(area difference {abs(a.area_sqft - b.area_sqft):.0f} swamps rooms difference {abs(a.rooms - b.rooms)})")

# 2. Three scalers
scaled = {name: pd.DataFrame(s.fit_transform(df), columns=df.columns)
          for name, s in [("StandardScaler", StandardScaler()), ("MinMaxScaler", MinMaxScaler()), ("RobustScaler", RobustScaler())]}
for name, d in scaled.items():
    print(f"{name:<15} price: mean {d.price_m.mean():6.2f}  std {d.price_m.std():5.2f}  "
          f"min {d.price_m.min():6.2f}  max {d.price_m.max():6.2f}")

# 3. Outliers: detect with IQR (Statistics module), then decide: keep, cap or remove
q1, q3 = df["price_m"].quantile([0.25, 0.75]); iqr = q3 - q1
upper = q3 + 1.5 * iqr
out = df[df["price_m"] > upper]
print(f"\nIQR fence: price > {upper:.1f} M is an outlier -> {len(out)} rows: {out['price_m'].tolist()}")
capped = df["price_m"].clip(upper=upper)                     # winsorising / capping
logged = np.log1p(df["price_m"])                              # log transform compresses the tail
print(f"skewness: raw {df['price_m'].skew():.2f}, capped {capped.skew():.2f}, log {logged.skew():.2f}")

# 4. Feature engineering: create more useful columns from existing ones
df["price_per_sqft_k"] = (df["price_m"] * 1000 / df["area_sqft"]).round(2)
df["size_band"] = pd.cut(df["area_sqft"], bins=[0, 900, 1400, np.inf], labels=["small", "medium", "large"])
print("\nengineered features:\n", df[["area_sqft", "price_m", "price_per_sqft_k", "size_band"]].head(5))
print("size bands:", df["size_band"].value_counts().to_dict())

fig, ax = plt.subplots(1, 4, figsize=(14, 3.2))
ax[0].hist(df["price_m"], bins=30, color="#F43F5E"); ax[0].set_title("raw price (skewed + outliers)")
ax[1].hist(scaled["StandardScaler"]["price_m"], bins=30, color="#FF6B1A"); ax[1].set_title("StandardScaler: same shape")
ax[2].hist(scaled["MinMaxScaler"]["price_m"], bins=30, color="#A78BFA"); ax[2].set_title("MinMax: squeezed by outliers")
ax[3].hist(logged, bins=30, color="#FCD34D"); ax[3].set_title("log1p: tail compressed")
fig.tight_layout(); fig.savefig("session-13_scaling_outliers.png", dpi=95)
print("\nSaved session-13_scaling_outliers.png")
