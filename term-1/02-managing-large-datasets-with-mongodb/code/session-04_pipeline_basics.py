# Session 4 · Pipeline basics: $match, $group, $sort, $project, $limit, $count
from store_db import get_db, show

db = get_db()

print("1) Products per category with average and max price")
show(db.products.aggregate([
    {"$group": {"_id": "$category",
                "products": {"$sum": 1},
                "avgPrice": {"$avg": "$price"},
                "maxPrice": {"$max": "$price"}}},
    {"$sort": {"products": -1, "_id": 1}},
]))

print("\n2) Orders per status, but only non-cancelled ones ($match first)")
show(db.orders.aggregate([
    {"$match": {"status": {"$ne": "Cancelled"}}},
    {"$group": {"_id": "$status", "orders": {"$sum": 1}}},
    {"$sort": {"orders": -1, "_id": 1}},
]))

print("\n3) $project with computed fields: stock value, in whole thousands")
show(db.products.aggregate([
    {"$project": {"_id": 0, "name": 1,
                  "stockValue": {"$multiply": ["$price", "$stock"]},
                  "inThousands": {"$floor": {"$divide": [{"$multiply": ["$price", "$stock"]}, 1000]}}}},
    {"$sort": {"stockValue": -1}},
    {"$limit": 3},
]))

print("\n4) $count: how many Karachi customers")
show(db.customers.aggregate([{"$match": {"city": "Karachi"}}, {"$count": "karachiCustomers"}]))

print("\n5) $push / $addToSet collect values per group")
show(db.customers.aggregate([
    {"$group": {"_id": "$city", "names": {"$push": "$name"}, "tiers": {"$addToSet": "$loyalty"}}},
    {"$sort": {"_id": 1}},
]))
