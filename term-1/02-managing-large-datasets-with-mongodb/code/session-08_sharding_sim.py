# Session 8 · How the shard key decides where documents live
# Teaching model of 3 shards, comparing a ranged key on a growing value with a hashed key.
import hashlib
from collections import Counter

SHARDS = ["shardA", "shardB", "shardC"]
order_ids = list(range(1, 30_001))              # monotonically increasing _id values
new_ids = list(range(30_001, 33_001))           # the next 3,000 inserts

# Ranged sharding: chunks own contiguous ranges of the key
ranges = [(1, 10_000, "shardA"), (10_001, 20_000, "shardB"), (20_001, float("inf"), "shardC")]
def ranged(k):
    for lo, hi, s in ranges:
        if lo <= k <= hi: return s

def hashed(k):
    h = int(hashlib.md5(str(k).encode()).hexdigest(), 16)
    return SHARDS[h % len(SHARDS)]

def report(title, fn, keys):
    c = Counter(fn(k) for k in keys)
    print(f"  {title:<34}" + "  ".join(f"{s}={c.get(s, 0):>6,}" for s in SHARDS))

print("Existing 30,000 orders")
report("ranged on _id", ranged, order_ids)
report("hashed on _id", hashed, order_ids)
print("\nNext 3,000 inserts (where does the write load go?)")
report("ranged on _id  (HOT SHARD!)", ranged, new_ids)
report("hashed on _id  (spread out)", hashed, new_ids)

print("\nQuery routing by mongos")
print("  find({_id: 15000})            ranged ->", ranged(15000), "(targeted, 1 shard)")
print("  find({_id: {$gte: 100, $lte: 200}}) ranged ->", sorted({ranged(k) for k in range(100, 201)}), "(targeted)")
print("  same range query, hashed      ->", sorted({hashed(k) for k in range(100, 201)}), "(scatter-gather)")
print("  find({city: 'Lahore'})        -> all shards (field is not the shard key)")

# A low-cardinality key cannot be split further: jumbo chunks
cities = ["Karachi"] * 18_000 + ["Lahore"] * 8_000 + ["Islamabad"] * 4_000
c = Counter(cities)
print("\nShard key {city: 1}: only", len(c), "distinct values ->", dict(c))
print("  The 'Karachi' chunk can never be split, so one shard holds 60% of the data (a jumbo chunk).")
