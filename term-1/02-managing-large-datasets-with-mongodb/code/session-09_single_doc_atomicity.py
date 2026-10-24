# Session 9 · Single-document atomicity and why multi-document work needs transactions
from store_db import get_db

db = get_db()

print("1) A single-document update is always atomic: conditional stock decrement")
def buy(product_id, qty):
    r = db.products.update_one({"_id": product_id, "stock": {"$gte": qty}},   # check and change in ONE step
                               {"$inc": {"stock": -qty}})
    return "sold" if r.modified_count else "rejected (not enough stock)"
for q in (2, 2, 2):
    print(f"   buy 2 x Gaming Laptop -> {buy(108, q)}; stock now {db.products.find_one({'_id': 108})['stock']}")

print("\n2) Multi-document work WITHOUT a transaction: a crash in the middle")
db.orders.delete_many({"_id": 6001})
def place_order_unsafe(crash):
    db.products.update_one({"_id": 106}, {"$inc": {"stock": -2}})          # step 1: reserve stock
    if crash:
        raise ConnectionError("network dropped before the order was saved")
    db.orders.insert_one({"_id": 6001, "customerId": 2, "status": "Pending",
                          "items": [{"productId": 106, "qty": 2, "price": 6500}]})  # step 2
before = db.products.find_one({"_id": 106})["stock"]
try:
    place_order_unsafe(crash=True)
except ConnectionError as e:
    print("   error:", e)
after = db.products.find_one({"_id": 106})["stock"]
print(f"   speaker stock {before} -> {after}, order 6001 exists: {db.orders.count_documents({'_id': 6001}) == 1}")
print("   => 2 speakers vanished from stock with no order: the data is now inconsistent.")
