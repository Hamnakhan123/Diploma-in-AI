# Session 12 · From MongoDB to pandas for analysis
import pandas as pd
from store_db import get_db

db = get_db()
pd.set_option("display.width", 120)

# 1) Let MongoDB do the heavy lifting, then hand pandas a small, tidy result
pipeline = [
    {"$match": {"status": {"$ne": "Cancelled"}}},
    {"$unwind": "$items"},
    {"$lookup": {"from": "products", "localField": "items.productId", "foreignField": "_id", "as": "p"}},
    {"$unwind": "$p"},
    {"$lookup": {"from": "customers", "localField": "customerId", "foreignField": "_id", "as": "c"}},
    {"$unwind": "$c"},
    {"$project": {"_id": 0, "orderId": "$_id", "date": "$orderDate", "city": "$c.city",
                  "category": "$p.category", "qty": "$items.qty",
                  "revenue": {"$multiply": ["$items.qty", "$items.price"]}}},
]
df = pd.DataFrame(list(db.orders.aggregate(pipeline)))
print("Order lines:", df.shape)
print(df.head().to_string(index=False))

print("\nRevenue by city and category (pivot table):")
print(df.pivot_table(index="city", columns="category", values="revenue", aggfunc="sum", fill_value=0).to_string())

print("\nMonthly revenue:")
print(df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().to_string())

# 2) Nested documents -> flat columns with json_normalize
prod = pd.json_normalize(list(db.products.find({}, {"tags": 0})))
print("\nProducts flattened:", list(prod.columns))
print(prod.groupby("specs.brand")["price"].agg(["count", "mean"]).sort_values("count", ascending=False).head(3).to_string())

# 3) Write analysis results back to MongoDB
summary = df.groupby("category", as_index=False)["revenue"].sum()
db.category_summary.insert_many(summary.to_dict("records"))
print("\nSaved", db.category_summary.count_documents({}), "summary documents to kgs.category_summary")
