# Session 11 · One client factory for laptop, Colab and Atlas
# Put your Atlas URI in an environment variable (never in code or Git):
#     export MONGODB_URI="mongodb+srv://user:pass@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority"
# In Colab, use the key icon (Secrets) and read it with google.colab.userdata.get("MONGODB_URI").
import os
from store_db import get_db, PRODUCTS

def get_client():
    uri = os.environ.get("MONGODB_URI")
    if uri:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        client = MongoClient(uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
        where = "Atlas"
    else:
        import mongomock
        client = mongomock.MongoClient()
        where = "mongomock (set MONGODB_URI to use Atlas)"
    client.admin.command("ping")                 # fails fast if the URI, password or IP list is wrong
    return client, where

client, where = get_client()
print("Connected to:", where)

db = client["kgs"]
if db.products.count_documents({}) == 0:         # seed once
    db.products.insert_many([dict(p) for p in PRODUCTS])
print("products:", db.products.count_documents({}))

top = db.products.aggregate([{"$group": {"_id": "$category", "stockValue": {"$sum": {"$multiply": ["$price", "$stock"]}}}},
                             {"$sort": {"stockValue": -1}}, {"$limit": 3}])
for row in top:
    print(f"  {row['_id']:<12} Rs {row['stockValue']:>12,}")
