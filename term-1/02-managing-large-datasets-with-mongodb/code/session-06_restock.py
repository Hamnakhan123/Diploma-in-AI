# Session 6 · The same restock script in Python (compare with session-06_restock.js)
from datetime import datetime
from store_db import get_db

db = get_db()
LOW = 5
today = datetime(2025, 6, 30)                    # fixed date so the output is repeatable

print(f"Low-stock report for {db.name} on {today:%Y-%m-%d}")
for p in db.products.find({"stock": {"$lt": LOW}}, {"name": 1, "stock": 1}).sort("stock", 1):
    order = LOW * 2 - p["stock"]
    print(f"  {p['name']:<28} stock {p['stock']:>2} -> reorder {order}")
    db.reorders.insert_one({"productId": p["_id"], "qty": order, "createdAt": today})

print(list(db.reorders.aggregate([{"$group": {"_id": None, "lines": {"$sum": 1}, "units": {"$sum": "$qty"}}}])))
