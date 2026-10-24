# Session 9 · All-or-nothing with a transaction (simulated)
# mongomock has no sessions, so this file builds a small Transaction helper that
# snapshots the collections it touches and restores them on error. It follows the
# same shape as PyMongo's  session.with_transaction(callback)  so the code you write
# inside the callback is the code you would write against a real replica set.
import copy
from store_db import get_db

db = get_db()

class TransientTransactionError(Exception):
    """Stands in for errors labelled TransientTransactionError (e.g. a write conflict)."""

class Transaction:
    def __init__(self, db, collections):
        self.db, self.names = db, collections
    def __enter__(self):
        self.snapshot = {n: copy.deepcopy(list(self.db[n].find())) for n in self.names}
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type:                                  # abortTransaction: restore every touched collection
            for n, docs in self.snapshot.items():
                self.db[n].delete_many({})
                if docs: self.db[n].insert_many(docs)
            print(f"   abortTransaction -> rolled back ({exc_type.__name__}: {exc})")
        else:
            print("   commitTransaction -> all changes visible together")
        return False

def with_transaction(callback, retries=3):
    """Retry the whole callback on transient errors, like session.with_transaction()."""
    for attempt in range(1, retries + 1):
        try:
            with Transaction(db, ["products", "orders"]):
                return callback(attempt)
        except TransientTransactionError:
            print(f"   attempt {attempt} hit a transient error, retrying")
    raise RuntimeError("gave up after retries")

def place_order(order_id, product_id, qty, crash=False):
    def callback(attempt):
        p = db.products.find_one({"_id": product_id})
        if p["stock"] < qty:
            raise ValueError(f"only {p['stock']} in stock")
        db.products.update_one({"_id": product_id}, {"$inc": {"stock": -qty}})
        if crash:
            raise ConnectionError("network dropped before the order was saved")
        db.orders.insert_one({"_id": order_id, "customerId": 2, "status": "Pending",
                              "items": [{"productId": product_id, "qty": qty, "price": p["price"]}]})
        return order_id
    return callback

def state(pid, oid):
    return f"stock={db.products.find_one({'_id': pid})['stock']}, order {oid} exists={db.orders.count_documents({'_id': oid}) == 1}"

print("1) Successful order")
print("   before:", state(106, 6001)); with_transaction(place_order(6001, 106, 2)); print("   after :", state(106, 6001))

print("\n2) Crash between the two writes")
try:
    with_transaction(place_order(6002, 106, 2, crash=True))
except ConnectionError:
    pass
print("   after :", state(106, 6002))

print("\n3) Business rule fails (not enough stock)")
try:
    with_transaction(place_order(6003, 108, 5))
except ValueError:
    pass
print("   after :", state(108, 6003))

print("\n4) Transient write conflict on the first attempt, success on the retry")
calls = {"n": 0}
def flaky(attempt):
    calls["n"] += 1
    db.products.update_one({"_id": 110}, {"$inc": {"stock": -1}})
    if attempt == 1:
        raise TransientTransactionError("WriteConflict")
    db.orders.insert_one({"_id": 6004, "customerId": 5, "status": "Pending", "items": [{"productId": 110, "qty": 1, "price": 16000}]})
print("   before:", state(110, 6004)); with_transaction(flaky); print("   after :", state(110, 6004), f"(callback ran {calls['n']} times, stock fell by 1 only)")
