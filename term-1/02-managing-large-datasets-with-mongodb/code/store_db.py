"""Sample data for the MongoDB module: the "Karachi Gadget Store" as documents.

Every example calls get_db() to get a fresh, identical in-memory database.
It uses mongomock, which mimics a MongoDB server inside Python, so nothing
needs to be installed or running. To use a real server instead, call
get_db(uri="mongodb://localhost:27017") (needs pymongo and a running mongod).
"""
from datetime import datetime
import json

PRODUCTS = [
    {"_id": 101, "name": "Wireless Mouse", "category": "Accessories", "price": 1500, "stock": 40,
     "tags": ["wireless", "office"], "specs": {"brand": "Logi", "warrantyMonths": 12}},
    {"_id": 102, "name": "Mechanical Keyboard", "category": "Accessories", "price": 7500, "stock": 15,
     "tags": ["office", "gaming"], "specs": {"brand": "Redragon", "warrantyMonths": 12}},
    {"_id": 103, "name": "27-inch Monitor", "category": "Displays", "price": 52000, "stock": 6,
     "tags": ["office", "4k"], "specs": {"brand": "Dell", "warrantyMonths": 36}},
    {"_id": 104, "name": "USB-C Hub", "category": "Accessories", "price": 4200, "stock": 0,
     "tags": ["usb-c", "office"], "specs": {"brand": "Anker", "warrantyMonths": 18}},
    {"_id": 105, "name": "Noise-Cancelling Headphones", "category": "Audio", "price": 18500, "stock": 9,
     "tags": ["wireless", "travel"], "specs": {"brand": "Sony", "warrantyMonths": 12}},
    {"_id": 106, "name": "Bluetooth Speaker", "category": "Audio", "price": 6500, "stock": 22,
     "tags": ["wireless", "outdoor"], "specs": {"brand": "JBL", "warrantyMonths": 12}},
    {"_id": 107, "name": "Webcam HD", "category": "Accessories", "price": 4500, "stock": 12,
     "tags": ["office", "video"], "specs": {"brand": "Logi", "warrantyMonths": 12}},
    {"_id": 108, "name": "Gaming Laptop", "category": "Computers", "price": 285000, "stock": 3,
     "tags": ["gaming"], "specs": {"brand": "ASUS", "warrantyMonths": 24, "ramGB": 16}},
    {"_id": 109, "name": "Ultrabook", "category": "Computers", "price": 210000, "stock": 5,
     "tags": ["office", "travel"], "specs": {"brand": "Lenovo", "warrantyMonths": 24, "ramGB": 16}},
    {"_id": 110, "name": "Portable SSD 1TB", "category": "Storage", "price": 16000, "stock": 18,
     "tags": ["usb-c", "travel"], "specs": {"brand": "Samsung", "warrantyMonths": 36}},
]

CUSTOMERS = [
    {"_id": 1, "name": "Ayesha Khan", "city": "Karachi", "email": "ayesha@example.pk", "joined": datetime(2025, 1, 12), "loyalty": "Gold"},
    {"_id": 2, "name": "Bilal Ahmed", "city": "Lahore", "email": "bilal@example.pk", "joined": datetime(2025, 2, 3), "loyalty": "Silver"},
    {"_id": 3, "name": "Sana Malik", "city": "Karachi", "email": None, "joined": datetime(2025, 3, 20), "loyalty": "Bronze"},
    {"_id": 4, "name": "Usman Tariq", "city": "Islamabad", "email": "usman@example.pk", "joined": datetime(2025, 4, 8), "loyalty": "Silver"},
    {"_id": 5, "name": "Hira Siddiqui", "city": "Karachi", "email": "hira@example.pk", "joined": datetime(2025, 6, 1), "loyalty": "Gold"},
    {"_id": 6, "name": "Fahad Raza", "city": "Lahore", "joined": datetime(2025, 7, 15), "loyalty": "Bronze"},
]

def _o(oid, cust, day, status, items, pay):
    return {"_id": oid, "customerId": cust, "orderDate": datetime(2025, *day), "status": status,
            "payment": pay, "items": [{"productId": p, "qty": q, "price": pr} for p, q, pr in items]}

ORDERS = [
    _o(5001, 1, (3, 2), "Delivered", [(101, 2, 1500), (107, 1, 4500)], "Card"),
    _o(5002, 2, (3, 5), "Delivered", [(103, 1, 52000)], "COD"),
    _o(5003, 1, (3, 18), "Shipped", [(105, 1, 18500), (106, 1, 6500)], "Card"),
    _o(5004, 3, (4, 1), "Delivered", [(102, 1, 7500), (101, 1, 1500)], "COD"),
    _o(5005, 4, (4, 9), "Cancelled", [(108, 1, 285000)], "Card"),
    _o(5006, 5, (4, 22), "Delivered", [(110, 2, 16000)], "Card"),
    _o(5007, 2, (5, 3), "Pending", [(106, 2, 6500)], "COD"),
    _o(5008, 5, (5, 14), "Delivered", [(109, 1, 210000), (101, 1, 1500)], "Card"),
    _o(5009, 6, (5, 20), "Shipped", [(104, 3, 4200)], "COD"),
    _o(5010, 1, (6, 2), "Delivered", [(103, 1, 52000), (102, 1, 7500)], "Card"),
]


def get_db(name="kgs", uri=None):
    """Return a freshly loaded database (mongomock by default)."""
    if uri:
        from pymongo import MongoClient
        client = MongoClient(uri)
    else:
        import mongomock
        client = mongomock.MongoClient()
    db = client[name]
    for coll, docs in (("products", PRODUCTS), ("customers", CUSTOMERS), ("orders", ORDERS)):
        db[coll].drop()
        db[coll].insert_many([dict(d) for d in docs])
    return db


def _plain(v):
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d") if v.hour == v.minute == 0 else v.isoformat(timespec="minutes")
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if type(v).__name__ == "ObjectId":
        return f"ObjectId('{v}')"
    return v


def show(docs, limit=20):
    """Print documents as compact JSON, one per line."""
    docs = [docs] if isinstance(docs, dict) else list(docs)
    for d in docs[:limit]:
        print(json.dumps(_plain(d), ensure_ascii=False, default=str))
    if len(docs) > limit:
        print(f"... ({len(docs) - limit} more)")
    print(f"({len(docs)} document{'s' if len(docs) != 1 else ''})")
