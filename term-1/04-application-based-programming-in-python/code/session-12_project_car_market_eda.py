"""
Session 12 · Mini project: visual exploratory analysis of a used-car market
---------------------------------------------------------------------------
A buyer (or a pricing model, Session 15) needs to understand used-car prices.
The project builds a synthetic listings dataset (seeded), then answers six
questions with six charts arranged in one dashboard, printing the numbers
behind each chart so every visual claim can be checked.
Run:  python session-12_project_car_market_eda.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(99)
brands = {"Suzuki": (2.6, 0.10), "Toyota": (5.8, 0.07), "Honda": (5.2, 0.08), "Hyundai": (4.9, 0.09), "KIA": (5.0, 0.09)}
n = 400
brand = rng.choice(list(brands), n, p=[0.32, 0.24, 0.2, 0.12, 0.12])
age = rng.integers(0, 15, n)
mileage = np.clip(age * rng.normal(14000, 3000, n) + rng.normal(5000, 3000, n), 500, None).round(-2)
base = np.array([brands[b][0] for b in brand])
depr = np.array([brands[b][1] for b in brand])
trans = rng.choice(["Manual", "Automatic"], n, p=[0.45, 0.55])
price = base * (1 - depr) ** age * np.where(trans == "Automatic", 1.12, 1.0) * np.exp(rng.normal(0, 0.08, n)) - mileage / 1e6 * 0.4
df = pd.DataFrame({"brand": brand, "age": age, "mileage_km": mileage, "transmission": trans,
                   "price_m": price.round(2)})                     # price in million rupees
df = df[df["price_m"] > 0.3]
print("listings:", len(df), "\n", df.describe().round(2).T[["mean", "min", "50%", "max"]], "\n")

sns.set_theme(style="whitegrid")
pal = dict(zip(brands, ["#FF6B1A", "#A78BFA", "#F43F5E", "#FCD34D", "#6B7280"]))
fig, ax = plt.subplots(2, 3, figsize=(15, 8.5))
fig.suptitle("Used-car market: six questions, six charts (synthetic listings)", fontsize=14, fontweight="bold")

# Q1 What do prices look like? -> histogram (right-skewed)
sns.histplot(df["price_m"], bins=30, ax=ax[0, 0], color="#FF6B1A")
ax[0, 0].axvline(df["price_m"].median(), color="black", ls="--", label=f"median {df['price_m'].median():.2f} M")
ax[0, 0].set(title="Q1 Price distribution", xlabel="price (million Rs)"); ax[0, 0].legend()
print(f"Q1 median price {df['price_m'].median():.2f} M, mean {df['price_m'].mean():.2f} M, skew {df['price_m'].skew():.2f}")

# Q2 Which brands are most common? -> sorted bar
counts = df["brand"].value_counts()
ax[0, 1].bar(counts.index, counts.values, color=[pal[b] for b in counts.index])
ax[0, 1].set(title="Q2 Listings per brand", ylabel="listings")
print("Q2 listings:", counts.to_dict())

# Q3 How do brands compare on price? -> box plot ordered by median
order = df.groupby("brand")["price_m"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="brand", y="price_m", hue="brand", order=order, palette=pal, legend=False, ax=ax[0, 2])
ax[0, 2].set(title="Q3 Price by brand", ylabel="price (million Rs)", xlabel="")
print("Q3 median price by brand:", df.groupby("brand")["price_m"].median().round(2).reindex(order).to_dict())

# Q4 How fast do cars lose value? -> line of median price by age per brand
med = df.groupby(["age", "brand"])["price_m"].median().unstack()
for b in brands:
    ax[1, 0].plot(med.index, med[b].rolling(3, min_periods=1).mean(), label=b, color=pal[b], lw=2)
ax[1, 0].set(title="Q4 Depreciation: median price by age", xlabel="age (years)", ylabel="price (million Rs)")
ax[1, 0].legend(fontsize=8)
keep = (med.loc[med.index >= 8].mean() / med.loc[med.index <= 1].mean()).round(2)
print("Q4 value kept after 8+ years vs nearly new:", keep.sort_values(ascending=False).to_dict())

# Q5 Does mileage matter? -> scatter with transparency
sns.scatterplot(data=df, x="mileage_km", y="price_m", hue="transmission", alpha=0.6, s=18, ax=ax[1, 1],
                palette={"Manual": "#6B7280", "Automatic": "#FF6B1A"})
ax[1, 1].set(title=f"Q5 Price vs mileage (r = {df['mileage_km'].corr(df['price_m']):.2f})", xlabel="mileage (km)")
print(f"Q5 correlation price-mileage r = {df['mileage_km'].corr(df['price_m']):.2f}")

# Q6 Automatic vs manual premium by brand -> grouped bar
prem = df.pivot_table(index="brand", columns="transmission", values="price_m", aggfunc="median").reindex(order)
prem.plot(kind="bar", ax=ax[1, 2], color=["#FF6B1A", "#6B7280"], rot=0)
ax[1, 2].set(title="Q6 Median price: automatic vs manual", ylabel="price (million Rs)", xlabel="")
print("Q6 automatic premium:", ((prem["Automatic"] / prem["Manual"] - 1) * 100).round(0).to_dict(), "(%)")

fig.tight_layout()
fig.savefig("session-12_project_car_market_eda.png", dpi=80)
print("\nSaved session-12_project_car_market_eda.png")
