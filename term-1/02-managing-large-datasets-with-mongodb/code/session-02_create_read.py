# Session 2 · Create and Read
from store_db import get_db, show

db = get_db()
db.drop_collection("staff")                        # start clean

# CREATE ------------------------------------------------------------
r1 = db.staff.insert_one({"_id": "E01", "name": "Zara", "role": "Cashier", "salary": 60000})
print("insert_one ->", r1.inserted_id)
r2 = db.staff.insert_many([
    {"_id": "E02", "name": "Kamran", "role": "Technician", "salary": 85000, "skills": ["laptops", "phones"]},
    {"_id": "E03", "name": "Mehwish", "role": "Manager", "salary": 150000},
    {"_id": "E04", "name": "Danish", "role": "Technician", "salary": 78000, "skills": ["phones"]},
])
print("insert_many ->", r2.inserted_ids)

# READ --------------------------------------------------------------
print("\n1) find_one by _id")
show(db.staff.find_one({"_id": "E03"}))

print("\n2) equality filter + projection (only name and salary)")
show(db.staff.find({"role": "Technician"}, {"_id": 0, "name": 1, "salary": 1}))

print("\n3) products: Accessories, sort by price descending, top 3")
show(db.products.find({"category": "Accessories"}, {"name": 1, "price": 1})
                .sort("price", -1).limit(3))

print("\n4) paging: skip 3, limit 3 (page 2 of products ordered by _id)")
show(db.products.find({}, {"name": 1}).sort("_id", 1).skip(3).limit(3))

print("\n5) query inside an embedded document and an array")
show(db.products.find({"specs.brand": "Logi", "tags": "office"}, {"name": 1, "specs.brand": 1}))

print("\n6) counting")
print("all customers:", db.customers.count_documents({}),
      "| Karachi customers:", db.customers.count_documents({"city": "Karachi"}))
print("distinct cities:", sorted(db.customers.distinct("city")))
