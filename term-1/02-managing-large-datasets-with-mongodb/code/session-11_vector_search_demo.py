# Session 11 · The idea behind Atlas Vector Search, on a laptop
# Atlas Vector Search stores an embedding (a list of numbers) in each document and finds
# the documents whose vectors are closest to a query vector. Here the "embeddings" are
# tiny hand-made 4-number vectors: [office, gaming, audio, portable].
import math
import mongomock

db = mongomock.MongoClient().kgs
db.products.insert_many([
    {"_id": 101, "name": "Wireless Mouse",              "embedding": [0.9, 0.3, 0.0, 0.6]},
    {"_id": 102, "name": "Mechanical Keyboard",         "embedding": [0.7, 0.8, 0.0, 0.1]},
    {"_id": 105, "name": "Noise-Cancelling Headphones", "embedding": [0.3, 0.2, 1.0, 0.8]},
    {"_id": 106, "name": "Bluetooth Speaker",           "embedding": [0.1, 0.1, 0.9, 0.7]},
    {"_id": 108, "name": "Gaming Laptop",               "embedding": [0.4, 1.0, 0.3, 0.4]},
    {"_id": 110, "name": "Portable SSD 1TB",            "embedding": [0.6, 0.3, 0.0, 1.0]},
])

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def vector_search(query_vector, limit=3):
    scored = [(cosine(query_vector, d["embedding"]), d["name"]) for d in db.products.find()]
    return sorted(scored, reverse=True)[:limit]

queries = {"something to listen to music on a trip": [0.1, 0.0, 1.0, 0.9],
           "gear for a gamer":                      [0.2, 1.0, 0.2, 0.2]}
for text, vec in queries.items():
    print(f"Query: '{text}'")
    for score, name in vector_search(vec):
        print(f"   {score:.3f}  {name}")
    print()
