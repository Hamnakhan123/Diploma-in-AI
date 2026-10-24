# Session 6 · Collection methods beyond basic CRUD
from pymongo import ReturnDocument
from store_db import get_db, show

db = get_db()

print("1) findOneAndDelete: take the oldest open (Pending/Shipped) order off a queue")
show(db.orders.find_one_and_delete({"status": {"$in": ["Pending", "Shipped"]}}, sort=[("orderDate", 1)],
                                   projection={"status": 1, "orderDate": 1}))

print("\n2) findOneAndReplace returning the new document")
show(db.customers.find_one_and_replace({"_id": 3}, {"name": "Sana Malik", "city": "Karachi", "loyalty": "Silver"},
                                       return_document=ReturnDocument.AFTER))

print("\n3) distinct with a filter")
print("   brands of products under Rs 10,000:", sorted(db.products.distinct("specs.brand", {"price": {"$lt": 10000}})))

print("\n4) createIndex / getIndexes / dropIndex")
db.products.create_index([("category", 1), ("price", -1)], name="cat_price")
print("   indexes:", list(db.products.index_information()))
db.products.drop_index("cat_price")
print("   after drop:", list(db.products.index_information()))

print("\n5) renameCollection and drop")
db.orders.aggregate([{"$match": {"status": "Cancelled"}}, {"$out": "tmp_cancelled"}])
db.tmp_cancelled.rename("cancelled_2025")
print("   collections:", sorted(db.list_collection_names()))
db.cancelled_2025.drop()
print("   after drop :", sorted(db.list_collection_names()))
