# Session 2 · Update and Delete
from pymongo import ReturnDocument
from store_db import get_db, show

db = get_db()

print("1) update_one with $set and $inc")
r = db.products.update_one({"_id": 104}, {"$set": {"stock": 25}, "$inc": {"price": 300}})
print("matched", r.matched_count, "modified", r.modified_count)
show(db.products.find({"_id": 104}, {"name": 1, "price": 1, "stock": 1}))

print("\n2) update_many: Rs 500 off every Audio product")
r = db.products.update_many({"category": "Audio"}, {"$inc": {"price": -500}})
print("modified", r.modified_count)
show(db.products.find({"category": "Audio"}, {"name": 1, "price": 1}))

print("\n3) upsert: update if exists, otherwise insert")
r = db.customers.update_one({"email": "noor@example.pk"},
                            {"$set": {"name": "Noor Fatima", "city": "Hyderabad"}}, upsert=True)
print("matched", r.matched_count, "upserted_id", r.upserted_id is not None)

print("\n4) replace_one swaps the whole document (except _id)")
db.customers.replace_one({"_id": 6}, {"name": "Fahad Raza", "city": "Multan"})
show(db.customers.find_one({"_id": 6}))

print("\n5) find_one_and_update returns the document in one atomic step")
doc = db.products.find_one_and_update({"_id": 101}, {"$inc": {"stock": -1}},
                                      projection={"name": 1, "stock": 1},
                                      return_document=ReturnDocument.AFTER)
show(doc)

print("\n6) delete_one and delete_many")
print("cancelled orders deleted:", db.orders.delete_many({"status": "Cancelled"}).deleted_count)
print("one pending order deleted:", db.orders.delete_one({"status": "Pending"}).deleted_count)
print("orders left:", db.orders.count_documents({}))
