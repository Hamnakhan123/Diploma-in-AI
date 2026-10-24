# Session 7 · Creating the main index types
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from store_db import get_db

db = get_db()

made = [
    db.products.create_index("category"),                                         # single field
    db.products.create_index([("category", ASCENDING), ("price", DESCENDING)]),    # compound
    db.products.create_index("tags"),                                             # multikey (array field)
    db.products.create_index("specs.brand", name="brand_idx"),                    # embedded field, custom name
    db.orders.create_index([("customerId", 1), ("orderDate", -1)]),               # supports "my latest orders"
    db.customers.create_index("joined", expireAfterSeconds=60 * 60 * 24 * 365),   # TTL (on a date field)
]
print("created:", made)

print("\nproducts indexes:")
for name, info in db.products.index_information().items():
    print(f"  {name:<22} key={info['key']}")

print("\nUnique index on usernames")
db.users.create_index("username", unique=True)
db.users.insert_one({"username": "ayesha.k"})
try:
    db.users.insert_one({"username": "ayesha.k"})
except DuplicateKeyError:
    print("  DuplicateKeyError: username 'ayesha.k' is taken")

print("\nDropping an index")
db.products.drop_index("brand_idx")
print("  remaining:", list(db.products.index_information()))
