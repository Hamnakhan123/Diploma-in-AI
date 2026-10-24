# Session 4 · Reporting stages: $addFields, $cond, dates, $bucket, $facet, $out
from store_db import get_db, show

db = get_db()

print("1) Monthly sales (all non-cancelled orders)")
show(db.orders.aggregate([
    {"$match": {"status": {"$ne": "Cancelled"}}},
    {"$addFields": {"lineTotals": {"$map": {"input": "$items", "as": "i",
                                            "in": {"$multiply": ["$$i.qty", "$$i.price"]}}},
                    "month": {"$dateToString": {"format": "%Y-%m", "date": "$orderDate"}}}},
    {"$addFields": {"total": {"$sum": "$lineTotals"}}},
    {"$group": {"_id": "$month", "orders": {"$sum": 1}, "sales": {"$sum": "$total"}}},
    {"$sort": {"_id": 1}},
]))

print("\n2) $cond labels each product as Budget / Mid / Premium")
show(db.products.aggregate([
    {"$project": {"_id": 0, "name": 1, "price": 1,
                  "band": {"$cond": [{"$lt": ["$price", 10000]}, "Budget",
                           {"$cond": [{"$lt": ["$price", 100000]}, "Mid", "Premium"]}]}}},
    {"$sort": {"price": 1}},
]))

print("\n3) $bucket: how many products fall in each price range")
show(db.products.aggregate([
    {"$bucket": {"groupBy": "$price", "boundaries": [0, 5000, 20000, 100000, 1000000],
                 "default": "other", "output": {"count": {"$sum": 1}, "names": {"$push": "$name"}}}},
]))

print("\n4) $facet: several summaries in one pass")
show(db.products.aggregate([
    {"$facet": {
        "outOfStock": [{"$match": {"stock": 0}}, {"$project": {"_id": 0, "name": 1}}],
        "byBrand":    [{"$group": {"_id": "$specs.brand", "n": {"$sum": 1}}}, {"$match": {"n": {"$gt": 1}}}],
        "priceStats": [{"$group": {"_id": None, "min": {"$min": "$price"}, "max": {"$max": "$price"},
                                   "avg": {"$avg": "$price"}}}],
    }},
]))

print("\n5) $out writes the result to a new collection (a materialised report)")
list(db.orders.aggregate([{"$match": {"status": "Delivered"}},
                          {"$project": {"customerId": 1, "orderDate": 1}},
                          {"$out": "delivered_orders"}]))
print("collections now:", sorted(db.list_collection_names()))
print("documents in delivered_orders:", db.delivered_orders.count_documents({}))
