# Session 5 · Administrative work through driver helpers
import bson
from store_db import get_db

db = get_db()
client = db.client

print("ping           ->", client.admin.command("ping"))
print("databases      ->", client.list_database_names())
print("collections    ->", sorted(db.list_collection_names()))

db.create_collection("audit_log")
db.audit_log.insert_one({"event": "price_change", "productId": 101})
print("after create   ->", sorted(db.list_collection_names()))

db.audit_log.rename("price_audit")                  # renameCollection
print("after rename   ->", sorted(db.list_collection_names()))

db.drop_collection("price_audit")                   # drop
print("after drop     ->", sorted(db.list_collection_names()))

# A home-made version of dbStats / collStats using BSON sizes
def coll_stats(name):
    docs = list(db[name].find())
    sizes = [len(bson.encode(d)) for d in docs]
    return {"ns": f"{db.name}.{name}", "count": len(docs), "size": sum(sizes),
            "avgObjSize": round(sum(sizes) / len(sizes)), "nindexes": len(db[name].index_information())}

print("\n{:<14} {:>5} {:>7} {:>10} {:>8}".format("collection", "count", "bytes", "avgObjSize", "indexes"))
total = 0
for name in sorted(db.list_collection_names()):
    s = coll_stats(name); total += s["size"]
    print("{:<14} {:>5} {:>7} {:>10} {:>8}".format(name, s["count"], s["size"], s["avgObjSize"], s["nindexes"]))
print("dbStats-style total data size:", total, "bytes")
