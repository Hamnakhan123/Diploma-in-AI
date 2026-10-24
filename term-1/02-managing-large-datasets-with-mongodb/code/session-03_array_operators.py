# Session 3 · Array query, update and projection operators
from store_db import get_db, show

db = get_db()

print("1) $all: tagged BOTH wireless and office")
print([d["name"] for d in db.products.find({"tags": {"$all": ["wireless", "office"]}})])

print("\n2) $size: exactly one tag")
print([d["name"] for d in db.products.find({"tags": {"$size": 1}})])

print("\n3) $elemMatch: orders with ONE item that has qty >= 2 AND price >= 4000")
print([o["_id"] for o in db.orders.find({"items": {"$elemMatch": {"qty": {"$gte": 2}, "price": {"$gte": 4000}}}})])
print("   without $elemMatch the two conditions may match different items:")
print([o["_id"] for o in db.orders.find({"items.qty": {"$gte": 2}, "items.price": {"$gte": 4000}})])

print("\n4) $push with $each and $slice: keep only the 3 newest tags")
db.products.update_one({"_id": 101}, {"$push": {"tags": {"$each": ["ergonomic", "sale"], "$slice": -3}}})
print(db.products.find_one({"_id": 101})["tags"])

print("\n5) $addToSet adds only if missing")
db.products.update_one({"_id": 101}, {"$addToSet": {"tags": {"$each": ["sale", "bestseller"]}}})
print(db.products.find_one({"_id": 101})["tags"])

print("\n6) $pull removes matching elements; $pop removes first (-1) or last (1)")
db.products.update_one({"_id": 101}, {"$pull": {"tags": "sale"}})
db.products.update_one({"_id": 101}, {"$pop": {"tags": -1}})
print(db.products.find_one({"_id": 101})["tags"])

print("\n7) positional $: change the price of product 101 inside order 5001 only")
db.orders.update_one({"_id": 5001, "items.productId": 101}, {"$set": {"items.$.price": 1400}})
show(db.orders.find({"_id": 5001}, {"items": 1}))

print("\n8) projection $slice: first item of each delivered order")
show(db.orders.find({"status": "Delivered"}, {"items": {"$slice": 1}, "customerId": 1}).limit(3))
