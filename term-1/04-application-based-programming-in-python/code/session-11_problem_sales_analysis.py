"""
Session 11 · Real-life problem: monthly sales analysis for a restaurant chain
----------------------------------------------------------------------------
PROBLEM
A restaurant chain with 3 Karachi branches exports one CSV row per order.
The export is messy: branch names in mixed case with spaces, prices stored as
text like "Rs 1,450", some missing quantities and duplicate order ids.
Management wants:
  1. a clean DataFrame,
  2. revenue per branch per month (pivot table),
  3. the best-selling item in each branch,
  4. the busiest weekday,
  5. a chart of monthly revenue by branch, and a clean CSV export.
The data is generated with a fixed random seed so the results are reproducible.
Run:  python session-11_problem_sales_analysis.py
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 110)
rng = np.random.default_rng(7)

# ---------- 1. create a realistic messy export (stands in for a real file) ----------
menu = {"Biryani": 450, "Chicken Karahi": 1450, "Nihari": 600, "Haleem": 400, "BBQ Platter": 1900}
n = 600
raw = pd.DataFrame({
    "order_id": np.arange(5001, 5001 + n),
    "date": pd.Timestamp("2026-07-01") + pd.to_timedelta(rng.integers(0, 92, n), unit="D"),
    "branch": rng.choice([" clifton", "Gulshan ", "DHA", "CLIFTON", "gulshan"], n),
    "item": rng.choice(list(menu), n, p=[0.32, 0.18, 0.2, 0.18, 0.12]),
    "qty": rng.integers(1, 5, n).astype(float),
})
raw["price"] = raw["item"].map(lambda i: f"Rs {menu[i]:,}")
raw.loc[rng.choice(n, 25, replace=False), "qty"] = np.nan          # missing quantities
raw = pd.concat([raw, raw.sample(12, random_state=1)])              # duplicated rows
raw.to_csv("sales_raw.csv", index=False)
print("raw export:", raw.shape, "| sample:\n", raw.head(3).to_string(index=False))

# ---------- 2. clean ----------
df = pd.read_csv("sales_raw.csv", parse_dates=["date"])
before = len(df)
df = df.drop_duplicates(subset="order_id")
df["branch"] = df["branch"].str.strip().str.title().replace({"Dha": "DHA"})   # title() would spoil the acronym
df["price"] = df["price"].str.replace(r"[^\d]", "", regex=True).astype(int)
df["qty"] = df["qty"].fillna(df.groupby("item")["qty"].transform("median")).astype(int)
df["revenue"] = df["qty"] * df["price"]
df["month"] = df["date"].dt.to_period("M").astype(str)
df["weekday"] = df["date"].dt.day_name()
print(f"\ncleaned: removed {before - len(df)} duplicates; branches now {sorted(df['branch'].unique())}")

# ---------- 3. analysis ----------
pivot = df.pivot_table(index="branch", columns="month", values="revenue", aggfunc="sum", margins=True, margins_name="Total")
print("\nRevenue (Rs) by branch and month:\n", pivot.map(lambda v: f"{v:,.0f}"))

best = (df.groupby(["branch", "item"])["qty"].sum().reset_index()
          .sort_values("qty", ascending=False).drop_duplicates("branch").set_index("branch"))
print("\nBest-selling item per branch (units):\n", best)

share = df.groupby("item")["revenue"].sum().sort_values(ascending=False)
print("\nRevenue share by item:", (share / share.sum() * 100).round(1).to_dict())

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
by_day = df.groupby("weekday")["order_id"].count().reindex(order)
print("\nOrders by weekday:", by_day.to_dict(), "-> busiest:", by_day.idxmax())

avg_ticket = df.groupby("branch")["revenue"].mean().round(0)
print("Average order value:", avg_ticket.to_dict())

df.to_csv("sales_clean.csv", index=False)
print("\nSaved sales_clean.csv with", len(df), "rows and columns", list(df.columns))

# ---------- 4. chart ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
monthly = df.pivot_table(index="month", columns="branch", values="revenue", aggfunc="sum") / 1000
ax = monthly.plot(kind="bar", figsize=(7, 3.6), color=["#FF6B1A", "#A78BFA", "#F43F5E"], rot=0)
ax.set_ylabel("Revenue (Rs thousand)"); ax.set_xlabel(""); ax.set_title("Monthly revenue by branch, Q3 2026")
ax.legend(title="Branch", fontsize=8)
plt.tight_layout(); plt.savefig("session-11_problem_sales_analysis.png", dpi=110)
print("Chart saved: session-11_problem_sales_analysis.png")
