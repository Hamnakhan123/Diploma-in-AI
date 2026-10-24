# Session 12 · A small ETL job: extract CSV, clean, load in batches with upserts
import csv, io, random
from itertools import islice
from pymongo import UpdateOne
from store_db import get_db

db = get_db()
random.seed(12)

# Extract: pretend this CSV arrived from a point-of-sale system (with some dirty rows)
raw = io.StringIO()
w = csv.writer(raw); w.writerow(["sku", "name", "price", "stock", "city"])
for i in range(1, 2501):
    price = random.choice([str(random.randint(500, 90000)), "", "N/A"]) if i % 50 == 0 else str(random.randint(500, 90000))
    w.writerow([f"SKU{i:05d}", f"Item {i}", price, random.randint(0, 100), random.choice(["karachi", "Karachi ", "LAHORE", "Islamabad"])])
raw.seek(0)

def clean(rows):
    """Transform: fix types and casing, skip rows that cannot be repaired."""
    for r in rows:
        try:
            price = int(r["price"])
        except ValueError:
            clean.skipped += 1
            continue
        yield {"_id": r["sku"], "name": r["name"].strip(), "price": price,
               "stock": int(r["stock"]), "city": r["city"].strip().title()}
clean.skipped = 0

def batches(it, size):
    it = iter(it)
    while chunk := list(islice(it, size)):
        yield chunk

loaded = 0
for n, chunk in enumerate(batches(clean(csv.DictReader(raw)), 1000), 1):
    ops = [UpdateOne({"_id": d["_id"]}, {"$set": d}, upsert=True) for d in chunk]   # idempotent: safe to rerun
    res = db.pos_items.bulk_write(ops, ordered=False)
    loaded += res.upserted_count + res.modified_count
    print(f"batch {n}: {len(chunk)} rows -> upserted {res.upserted_count}, modified {res.modified_count}")

print(f"\nloaded {loaded}, skipped {clean.skipped} dirty rows")

# Rerun the first batch: upserts make the job idempotent (nothing is duplicated)
raw.seek(0)
first = next(batches(clean(csv.DictReader(raw)), 1000))
res = db.pos_items.bulk_write([UpdateOne({"_id": d["_id"]}, {"$set": d}, upsert=True) for d in first])
print(f"rerun batch 1: upserted {res.upserted_count}, modified {res.modified_count}, total docs {db.pos_items.count_documents({})}")
db.pos_items.create_index("city")
print("rows per city:", {r["_id"]: r["n"] for r in db.pos_items.aggregate(
    [{"$group": {"_id": "$city", "n": {"$sum": 1}}}, {"$sort": {"_id": 1}}])})
