# Session 1 · A first look at documents, collections and databases
import mongomock
from store_db import show

client = mongomock.MongoClient()          # real server: pymongo.MongoClient("mongodb://localhost:27017")
db = client["kgs"]                        # mongosh: use kgs
print("Databases before any insert:", client.list_database_names())

# A document is a JSON-like object. Fields can hold arrays and sub-documents.
doc = {
    "name": "Wireless Mouse",
    "category": "Accessories",
    "price": 1500,
    "tags": ["wireless", "office"],          # array
    "specs": {"brand": "Logi", "dpi": 1600}, # embedded document
}
result = db.products.insert_one(doc)      # mongosh: db.products.insertOne({...})
print("Inserted _id:", result.inserted_id, "| type:", type(result.inserted_id).__name__)

# Flexible schema: the next document has different fields and that is allowed.
db.products.insert_one({"name": "Gift Card", "category": "Vouchers", "value": 5000, "expires": "2026-12-31"})

print("Databases after insert:", client.list_database_names())
print("Collections in kgs:", db.list_collection_names())
print("Documents in products:", db.products.count_documents({}))

print("\nAll products (without _id):")
show(db.products.find({}, {"_id": 0}))   # mongosh: db.products.find({}, {_id: 0})

# Read the embedded field with dot notation
print("\nBrand of the mouse:", db.products.find_one({"name": "Wireless Mouse"})["specs"]["brand"])
