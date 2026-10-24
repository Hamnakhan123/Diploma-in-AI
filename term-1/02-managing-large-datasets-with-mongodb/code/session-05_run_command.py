# Session 5 · What a database command looks like
# Every helper (count, distinct, create, drop…) is sent to the server as a COMMAND DOCUMENT:
# the first key is the command name, its value is usually the collection.
# mongomock implements only a few raw commands, so this file includes a tiny dispatcher
# that maps command documents to driver calls. On a real server you would simply call
#     db.command(cmd)            (PyMongo)      or      db.runCommand(cmd)   (mongosh)
from store_db import get_db

db = get_db()

def run_command(cmd):
    name, target = next(iter(cmd.items()))
    if name == "count":
        return {"n": db[target].count_documents(cmd.get("query", {})), "ok": 1}
    if name == "distinct":
        return {"values": sorted(db[target].distinct(cmd["key"], cmd.get("query", {}))), "ok": 1}
    if name == "create":
        db.create_collection(target); return {"ok": 1}
    if name == "drop":
        db.drop_collection(target); return {"ns": f"{db.name}.{target}", "ok": 1}
    if name == "listCollections":
        return {"cursor": {"firstBatch": [{"name": n} for n in sorted(db.list_collection_names())]}, "ok": 1}
    if name == "createIndexes":
        made = [db[target].create_index(list(ix["key"].items()), name=ix["name"]) for ix in cmd["indexes"]]
        return {"createdIndexes": made, "ok": 1}
    if name == "find":
        docs = list(db[target].find(cmd.get("filter", {}), cmd.get("projection")).limit(cmd.get("limit", 0)))
        return {"cursor": {"firstBatch": docs, "ns": f"{db.name}.{target}"}, "ok": 1}
    return {"ok": 0, "errmsg": f"no such command: '{name}'", "code": 59}

commands = [
    {"count": "products", "query": {"category": "Accessories"}},
    {"distinct": "customers", "key": "city", "query": {"loyalty": {"$ne": "Bronze"}}},
    {"create": "wishlists"},
    {"listCollections": 1},
    {"createIndexes": "products", "indexes": [{"key": {"category": 1, "price": -1}, "name": "cat_price"}]},
    {"find": "products", "filter": {"stock": 0}, "projection": {"name": 1}, "limit": 1},
    {"drop": "wishlists"},
    {"fsyncUnlockEverything": 1},
]
for c in commands:
    print("db.runCommand(", c, ")")
    print("   ->", run_command(c), "\n")
