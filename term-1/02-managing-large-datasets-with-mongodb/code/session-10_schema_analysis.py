# Session 10 · What Compass's Schema tab shows, computed by hand
from collections import Counter, defaultdict
from store_db import get_db

db = get_db()

def analyse(coll):
    docs = list(coll.find())
    seen, types, values = Counter(), defaultdict(Counter), defaultdict(list)
    def walk(d, prefix=""):
        for k, v in d.items():
            path = prefix + k
            seen[path] += 1
            types[path][type(v).__name__ if v is not None else "null"] += 1
            if isinstance(v, dict):
                walk(v, path + ".")
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                values[path].append(v)
    for d in docs:
        walk(d)
    print(f"{coll.name}: {len(docs)} documents")
    print(f"  {'field':<22}{'present':>8}  types                     range")
    for path in sorted(seen):
        t = ", ".join(f"{k} {v / len(docs):.0%}" for k, v in types[path].items())
        rng = f"{min(values[path]):,} .. {max(values[path]):,}" if values[path] else ""
        print(f"  {path:<22}{seen[path] / len(docs):>8.0%}  {t:<25} {rng}")
    print()

analyse(db.products)
analyse(db.customers)
