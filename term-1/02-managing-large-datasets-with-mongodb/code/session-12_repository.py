# Session 12 · A small data-access layer with PyMongo
from datetime import datetime
from pymongo import ASCENDING, ReturnDocument
from pymongo.errors import DuplicateKeyError, PyMongoError
from store_db import get_db

class ProductRepo:
    """All product database access in one place: the rest of the app never writes queries."""
    def __init__(self, db):
        self.col = db.products
        self.col.create_index([("category", ASCENDING), ("price", ASCENDING)])

    def add(self, doc):
        try:
            return self.col.insert_one(doc).inserted_id
        except DuplicateKeyError:
            raise ValueError(f"product {doc['_id']} already exists") from None

    def get(self, pid):
        return self.col.find_one({"_id": pid}, {"_id": 1, "name": 1, "price": 1, "stock": 1})

    def search(self, category=None, max_price=None, in_stock=True, page=1, size=2):
        q = {}
        if category: q["category"] = category
        if max_price is not None: q["price"] = {"$lte": max_price}
        if in_stock: q["stock"] = {"$gt": 0}
        cur = self.col.find(q, {"name": 1, "price": 1}).sort("price", 1).skip((page - 1) * size).limit(size)
        return list(cur)

    def sell(self, pid, qty):
        doc = self.col.find_one_and_update({"_id": pid, "stock": {"$gte": qty}},
                                           {"$inc": {"stock": -qty}, "$set": {"lastSold": datetime(2025, 6, 30)}},
                                           projection={"name": 1, "stock": 1},
                                           return_document=ReturnDocument.AFTER)
        if not doc:
            raise ValueError(f"cannot sell {qty} of product {pid}: not enough stock")
        return doc

repo = ProductRepo(get_db())
print("add:", repo.add({"_id": 114, "name": "Laptop Stand", "category": "Accessories", "price": 3500, "stock": 10}))
try:
    repo.add({"_id": 114, "name": "Duplicate"})
except ValueError as e:
    print("add again:", e)
print("get:", repo.get(114))
print("search Accessories <= 5000, page 1:", [p["name"] for p in repo.search("Accessories", 5000)])
print("search Accessories <= 5000, page 2:", [p["name"] for p in repo.search("Accessories", 5000, page=2)])
print("sell 3:", repo.sell(114, 3))
try:
    repo.sell(104, 1)
except ValueError as e:
    print("sell out-of-stock:", e)
except PyMongoError as e:                       # network/server problems land here on a real server
    print("database error:", e)
