# Session 10 · Doing what mongoexport / mongoimport do, from Python
import csv, json, os, tempfile
from datetime import datetime
from bson import json_util
from store_db import get_db

def ext_json(v):
    """Encode BSON types the way mongoexport writes Extended JSON (relaxed mode)."""
    if isinstance(v, datetime):
        return {"$date": v.strftime("%Y-%m-%dT%H:%M:%S.000Z")}
    raise TypeError(type(v))

db = get_db()
HOME = os.getcwd()
os.chdir(tempfile.mkdtemp())                     # work in a scratch folder
os.makedirs("exports", exist_ok=True)

# mongoexport --db kgs --collection customers --out exports/customers.json   (one JSON doc per line)
with open("exports/customers.json", "w") as f:
    for d in db.customers.find():
        f.write(json.dumps(d, default=ext_json) + "\n")   # Extended JSON keeps BSON types like dates
print("customers.json (first 2 lines):")
print("".join(open("exports/customers.json").readlines()[:2]))

# mongoexport --type=csv --fields name,category,price,specs.brand --out exports/products.csv
fields = ["_id", "name", "category", "price", "specs.brand"]
with open("exports/products.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(fields)
    for d in db.products.find():
        w.writerow([d["_id"], d["name"], d["category"], d["price"], d["specs"]["brand"]])
print("products.csv (first 4 lines):")
print("".join(open("exports/products.csv").readlines()[:4]))

# mongoimport --type=csv --headerline --columnsHaveTypes  (types must be converted on import)
with open("exports/new_products.csv", "w") as f:
    f.write("_id,name,category,price,stock\n112,Smart Watch,Wearables,24000,7\n113,Fitness Band,Wearables,6500,15\n")
with open("exports/new_products.csv") as f:
    rows = [{**r, "_id": int(r["_id"]), "price": int(r["price"]), "stock": int(r["stock"])} for r in csv.DictReader(f)]
db.products.insert_many(rows)
print("imported", len(rows), "rows; Wearables now:",
      [d["name"] for d in db.products.find({"category": "Wearables"})])

# Round trip: re-import the JSON export into a new collection (mongoimport --collection customers_copy)
with open("exports/customers.json") as f:
    db.customers_copy.insert_many([json_util.loads(line) for line in f])
c = db.customers_copy.find_one({"_id": 1})
print("round-trip check: joined is still a", type(c["joined"]).__name__)
os.chdir(HOME)
