# Session 3 · Comparison, logical, element and evaluation operators
from store_db import get_db, show

db = get_db()
P = {"_id": 0, "name": 1, "price": 1, "stock": 1}

print("1) $gt / $lte: price above 15,000 and at most 60,000")
show(db.products.find({"price": {"$gt": 15000, "$lte": 60000}}, P))

print("\n2) $in / $nin: categories Audio or Storage")
show(db.products.find({"category": {"$in": ["Audio", "Storage"]}}, P))

print("\n3) $ne: products that are not out of stock (count)")
print(db.products.count_documents({"stock": {"$ne": 0}}))

print("\n4) $or: cheap (< 2,000) OR nearly sold out (stock <= 3)")
show(db.products.find({"$or": [{"price": {"$lt": 2000}}, {"stock": {"$lte": 3}}]}, P))

print("\n5) $and on the same field (two conditions on price)")
show(db.products.find({"$and": [{"price": {"$gte": 4000}}, {"price": {"$lte": 7000}}]}, P))

print("\n6) $nor: neither Accessories nor priced over 100,000")
show(db.products.find({"$nor": [{"category": "Accessories"}, {"price": {"$gt": 100000}}]}, P))

print("\n7) $not: name does NOT start with a capital M")
print([d["name"] for d in db.products.find({"name": {"$not": {"$regex": "^M"}}})])

print("\n8) $exists vs null: customers with no usable email")
print("field missing   :", [c["name"] for c in db.customers.find({"email": {"$exists": False}})])
print("missing OR null :", [c["name"] for c in db.customers.find({"email": None})])

print("\n9) $type: documents where price is stored as an int")
print(db.products.count_documents({"price": {"$type": "int"}}), "of", db.products.count_documents({}))

print("\n10) $regex (case-insensitive) on name")
print([d["name"] for d in db.products.find({"name": {"$regex": "phone", "$options": "i"}})])

print("\n11) $expr compares two fields of the same document: stock value over 200,000")
show(db.products.find({"$expr": {"$gt": [{"$multiply": ["$price", "$stock"]}, 200000]}}, P))

print("\n12) $mod inside $expr: even product ids")
print([d["_id"] for d in db.products.find({"$expr": {"$eq": [{"$mod": ["$_id", 2]}, 0]}})])
