# Session 6 · Cursor methods (mongosh -> PyMongo)
from store_db import get_db

db = get_db()

cur = db.products.find({"stock": {"$gt": 0}}, {"name": 1, "price": 1}).sort([("price", -1)]).skip(1).limit(4)
print("1) sort + skip + limit, iterated like cursor.forEach():")
for d in cur:                                  # mongosh: .forEach(d => print(d.name))
    print("  ", d["name"], d["price"])

print("\n2) next() and hasNext()-style iteration")
cur = db.customers.find({}, {"name": 1}).sort("name", 1)
first = next(cur)                              # mongosh: cur.next()
print("   first:", first["name"])
print("   remaining:", [c["name"] for c in cur])  # mongosh: while (cur.hasNext()) ...

print("\n3) map(): build a list of strings from a cursor")
labels = [f"{d['name']} - Rs {d['price']:,}" for d in db.products.find({"category": "Audio"})]
print("  ", labels)                            # mongosh: .map(d => d.name + " - Rs " + d.price)

print("\n4) toArray() + length versus count methods")
arr = list(db.orders.find({"payment": "COD"}))  # mongosh: .toArray()
print("   COD orders (toArray().length):", len(arr))
print("   countDocuments:", db.orders.count_documents({"payment": "COD"}))
print("   estimatedDocumentCount (metadata, whole collection):", db.orders.estimated_document_count())

print("\n5) batch_size(): how many documents travel per network round trip")
cur = db.orders.find().batch_size(3)           # mongosh: .batchSize(3)
print("   documents fetched:", sum(1 for _ in cur), "(4 batches of up to 3 on a real server)")

print("\n6) hint() forces a particular index")
db.products.create_index("price")
print("  ", [d["name"] for d in db.products.find({"price": {"$lt": 5000}}).hint("price_1")])
