# Session 2 · Bulk writes and handling duplicate keys
from pymongo import InsertOne, UpdateOne, DeleteOne
from pymongo.errors import BulkWriteError, DuplicateKeyError
from store_db import get_db

db = get_db()

ops = [
    InsertOne({"_id": 111, "name": "Graphics Tablet", "category": "Accessories", "price": 12000, "stock": 4}),
    UpdateOne({"_id": 102}, {"$set": {"stock": 30}}),
    DeleteOne({"_id": 104}),
]
res = db.products.bulk_write(ops)
print("bulk result -> inserted:", res.inserted_count, "modified:", res.modified_count, "deleted:", res.deleted_count)

# _id must be unique
try:
    db.products.insert_one({"_id": 101, "name": "Duplicate mouse"})
except DuplicateKeyError:
    print("DuplicateKeyError: _id 101 already exists")

# ordered=True (default) stops at the first error; ordered=False carries on
docs = [{"_id": 201}, {"_id": 101}, {"_id": 202}]
for ordered in (True, False):
    db.products.delete_many({"_id": {"$in": [201, 202]}})
    try:
        db.products.insert_many(docs, ordered=ordered)
    except BulkWriteError as e:
        print(f"ordered={ordered}: inserted {e.details['nInserted']} of 3, errors: {len(e.details['writeErrors'])}")
