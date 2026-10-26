"""
Session 11 · Example 2: data manipulation - clean, sort, group, merge, reshape
-----------------------------------------------------------------------------
Run:  python session-11_manipulation.py
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 110)
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 105, 106, 107, 108],
    "date": ["2026-10-01", "2026-10-01", "2026-10-02", "2026-10-02", "2026-10-03", "2026-10-03",
             "2026-10-03", "2026-10-04", None],
    "branch": ["Clifton", "Gulshan", "Clifton", "DHA", "Gulshan", "Gulshan", "DHA", "Clifton", "DHA"],
    "item": ["Biryani", "Karahi", "Biryani", "Nihari", "Biryani", "Biryani", "Karahi", "Nihari", "Biryani"],
    "qty": [2, 1, 3, np.nan, 1, 1, 2, 2, 4],
    "price": [450, 1450, 450, 600, 450, 450, 1450, 600, 450],
})
print("raw data:\n", orders, "\n")

# 1. Missing values and duplicates
print("missing per column:", orders.isna().sum().to_dict())
print("duplicated rows:", orders.duplicated().sum())
clean = (orders.drop_duplicates()                       # remove the repeated order 105
               .dropna(subset=["date"])                 # an order with no date cannot be dated
               .assign(qty=lambda d: d["qty"].fillna(1).astype(int),      # assume 1 if missing
                       date=lambda d: pd.to_datetime(d["date"])))
clean["revenue"] = clean["qty"] * clean["price"]
print("after cleaning:", clean.shape, "\n", clean)

# 2. Sorting
print("\ntop 3 by revenue:\n", clean.sort_values("revenue", ascending=False).head(3)[["order_id", "item", "revenue"]])

# 3. apply / map on columns
size = {"Biryani": "single dish", "Karahi": "family dish", "Nihari": "single dish"}
clean["type"] = clean["item"].map(size)
clean["band"] = clean["revenue"].apply(lambda r: "high" if r >= 1400 else "normal")
print("\nmap + apply:\n", clean[["item", "type", "revenue", "band"]])

# 4. groupby + aggregate (split - apply - combine)
by_branch = clean.groupby("branch").agg(orders=("order_id", "count"), units=("qty", "sum"),
                                        revenue=("revenue", "sum")).sort_values("revenue", ascending=False)
print("\nby branch:\n", by_branch)
print("\nmean revenue per item:", clean.groupby("item")["revenue"].mean().round(0).to_dict())

# 5. pivot_table: branches as rows, items as columns
print("\npivot (revenue):\n", clean.pivot_table(index="branch", columns="item", values="revenue",
                                              aggfunc="sum", fill_value=0, margins=True))

# 6. merge (SQL-style join) with a second table
managers = pd.DataFrame({"branch": ["Clifton", "Gulshan", "DHA", "Saddar"],
                         "manager": ["Mr Asif", "Ms Rabia", "Mr Junaid", "Ms Nida"]})
merged = by_branch.reset_index().merge(managers, on="branch", how="right")
print("\nmerge how='right' (Saddar has no orders yet):\n", merged.fillna({"orders": 0, "units": 0, "revenue": 0}))

# 7. concat: stack two days of new orders under the old ones
extra = pd.DataFrame({"order_id": [109], "date": [pd.Timestamp("2026-10-05")], "branch": ["DHA"],
                      "item": ["Karahi"], "qty": [1], "price": [1450], "revenue": [1450]})
print("\nafter concat:", len(pd.concat([clean, extra], ignore_index=True)), "rows")

# 8. Dates: extract parts and resample by day
daily = clean.set_index("date")["revenue"].resample("D").sum()
print("\ndaily revenue:", {d.strftime("%a %d"): int(v) for d, v in daily.items()})
