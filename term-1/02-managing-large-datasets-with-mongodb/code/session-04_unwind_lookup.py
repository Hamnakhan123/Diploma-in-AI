# Session 4 · $unwind and $lookup: revenue reports across collections
from store_db import get_db, show

db = get_db()
delivered = {"$match": {"status": "Delivered"}}

print("1) $unwind turns one order with 2 items into 2 documents")
show(db.orders.aggregate([{"$match": {"_id": 5001}}, {"$unwind": "$items"},
                          {"$project": {"items": 1}}]))

print("\n2) Revenue per category from delivered orders ($unwind + $lookup + $group)")
show(db.orders.aggregate([
    delivered,
    {"$unwind": "$items"},
    {"$lookup": {"from": "products", "localField": "items.productId",
                 "foreignField": "_id", "as": "product"}},
    {"$unwind": "$product"},
    {"$group": {"_id": "$product.category",
                "units": {"$sum": "$items.qty"},
                "revenue": {"$sum": {"$multiply": ["$items.qty", "$items.price"]}}}},
    {"$sort": {"revenue": -1}},
]))

print("\n3) Top 3 customers by spend, with their names")
show(db.orders.aggregate([
    delivered,
    {"$unwind": "$items"},
    {"$group": {"_id": "$customerId",
                "spent": {"$sum": {"$multiply": ["$items.qty", "$items.price"]}},
                "orders": {"$addToSet": "$_id"}}},
    {"$lookup": {"from": "customers", "localField": "_id", "foreignField": "_id", "as": "c"}},
    {"$project": {"_id": 0, "name": {"$arrayElemAt": ["$c.name", 0]},
                  "city": {"$arrayElemAt": ["$c.city", 0]},
                  "spent": 1, "orderCount": {"$size": "$orders"}}},
    {"$sort": {"spent": -1}},
    {"$limit": 3},
]))

print("\n4) Products that were never part of a DELIVERED order")
show(db.products.aggregate([
    {"$lookup": {"from": "orders", "localField": "_id", "foreignField": "items.productId", "as": "o"}},
    {"$project": {"_id": 0, "name": 1,
                  "delivered": {"$filter": {"input": "$o", "as": "x",
                                            "cond": {"$eq": ["$$x.status", "Delivered"]}}}}},
    {"$match": {"delivered": {"$size": 0}}},
    {"$project": {"name": 1}},
]))
