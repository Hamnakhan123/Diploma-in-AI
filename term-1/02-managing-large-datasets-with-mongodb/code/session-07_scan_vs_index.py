# Session 7 · Why indexes matter: a collection scan versus an index scan
# mongomock has no query planner, so this file models what MongoDB does with
# 200,000 synthetic orders and reports the same counters you see in explain():
# totalDocsExamined, totalKeysExamined and nReturned.
import bisect, random, time

random.seed(7)
N = 200_000
cities = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta", "Multan"]
orders = [{"_id": i, "customerId": random.randint(1, 20_000),
           "city": random.choice(cities), "amount": random.randint(500, 300_000)} for i in range(N)]

def collscan(pred):
    t = time.perf_counter()
    out = [d for d in orders if pred(d)]
    return out, {"stage": "COLLSCAN", "docsExamined": N, "keysExamined": 0,
                 "nReturned": len(out), "ms": round((time.perf_counter() - t) * 1000, 1)}

# Build a B-tree-like index on customerId: sorted (key, position) pairs
index = sorted((d["customerId"], pos) for pos, d in enumerate(orders))
keys = [k for k, _ in index]

def ixscan(value):
    t = time.perf_counter()
    lo, hi = bisect.bisect_left(keys, value), bisect.bisect_right(keys, value)
    out = [orders[index[i][1]] for i in range(lo, hi)]
    return out, {"stage": "IXSCAN -> FETCH", "docsExamined": len(out), "keysExamined": hi - lo,
                 "nReturned": len(out), "ms": round((time.perf_counter() - t) * 1000, 3)}

target = 4242
_, s1 = collscan(lambda d: d["customerId"] == target)
_, s2 = ixscan(target)
print(f"Query: find({{customerId: {target}}}) on {N:,} orders\n")
for s in (s1, s2):
    print(f"  {s['stage']:<16} docsExamined={s['docsExamined']:>7,}  keysExamined={s['keysExamined']:>3}  "
          f"nReturned={s['nReturned']}")
print("\n  Selectivity: the index read", s2["keysExamined"], "keys instead of", f"{N:,}", "documents.")
print("  Timing on this machine: collection scan is roughly",
      max(1, round(s1["ms"] / max(s2["ms"], 0.001))), "times slower (exact numbers vary per run).")

# Covered query: everything needed is in the index, so no FETCH at all
covered = [k for k in keys[bisect.bisect_left(keys, 100):bisect.bisect_right(keys, 105)]]
print(f"\nCovered query find({{customerId: {{$gte: 100, $lte: 105}}}}, {{_id: 0, customerId: 1}}):")
print(f"  keysExamined={len(covered)}  docsExamined=0  (answered from the index alone)")

# Low selectivity: an index on city still touches 1/6 of the collection
per_city = sum(1 for d in orders if d["city"] == "Karachi")
print(f"\nLow-selectivity field: city = 'Karachi' matches {per_city:,} of {N:,} "
      f"({per_city / N:.0%}). An index helps far less here.")
