[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Diploma-in-AI/blob/main/term-1/02-managing-large-datasets-with-mongodb/code/session-11-mongodb-cloud-atlas.ipynb) &nbsp; 📓 [Notebook](code/session-11-mongodb-cloud-atlas.ipynb)

# Session 11: MongoDB in the Cloud with Atlas

> 🧭 [Diploma in AI](../../README.md) › [Term 1](../README.md) › [Managing Large Datasets with MongoDB](README.md) › **Session 11**
>
> ⏱️ **Estimated time:** 2.5 hours (1 h concepts + 1.5 h lab) &nbsp;|&nbsp; 📋 **Prerequisites:** Sessions 8 and 10
>
> Prepared by **Hamna Zahid Khan**, Junior Lecturer

[⬅ Previous: Session 10](session-10-mongodb-tools.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Next: Session 12 ➡](session-12-python-connectivity-pymongo.md)

---

## 🎯 Learning objectives

- Explain what **MongoDB Atlas** is and how its cluster tiers differ.
- Create a free **M0** cluster, a database user and an IP access-list entry.
- Build and protect an Atlas **connection string** (`mongodb+srv://`), and connect from mongosh, Compass and Python.
- Load sample data, and use Atlas features: **Data Explorer, Charts, Search, Vector Search, Triggers, backups, monitoring**.
- Apply cloud security basics: least-privilege users, secrets out of code, network access.

## 📖 Concepts

### 1. What Atlas gives you

**MongoDB Atlas** is MongoDB as a managed service on **AWS, Google Cloud or Azure**. Atlas handles installation, replica sets (every cluster is a 3-node replica set), patching, backups, monitoring and scaling; you handle data, indexes, users and queries.

| Tier | For | Notes |
|---|---|---|
| **M0 Free** | learning, prototypes | shared, 512 MB storage, limited operations, no backups |
| **Flex** | small apps, variable traffic | pay-as-you-go, capped monthly price |
| **Dedicated (M10 and up)** | production | dedicated RAM/CPU, backups, auto-scaling, sharding (M30+), BI Connector |

Regions near Pakistan include AWS **Mumbai (ap-south-1)**, **Bahrain (me-south-1)** and Azure **UAE North**; closer regions mean lower latency.

### 2. Getting started (about 10 minutes)

1. Sign up at **cloud.mongodb.com** (Google sign-in works) → create an **Organization** and **Project**.
2. **Create cluster** → *M0 Free* → provider and region → name `Cluster0`.
3. **Database Access** → add a database user (e.g. `hamna_app`) with a strong password and role *Read and write to any database* (or a custom role on `kgs` only).
4. **Network Access** → add your current IP. `0.0.0.0/0` (anywhere) is convenient for Colab but should be temporary.
5. **Connect** → *Drivers* → Python → copy the `mongodb+srv://…` string. *Compass* and *Shell* options give the same URI.
6. Optional: **… → Load Sample Dataset** adds `sample_mflix`, `sample_airbnb`, `sample_supplies` and more.

### 3. The connection string

```
mongodb+srv://<user>:<password>@cluster0.ab1cd.mongodb.net/<db>?retryWrites=true&w=majority&appName=<app>
```

| Part | Meaning |
|---|---|
| `+srv` | look up the replica-set member hosts in DNS (one name instead of three hosts); TLS is on by default |
| user / password | the **database user**, not your Atlas login; URL-encode special characters (`@` → `%40`) |
| `/<db>` | default database for authentication and commands |
| `retryWrites=true` | retry a write once after a failover |
| `w=majority` | durable write concern |

**Keep secrets out of code:** environment variables (`MONGODB_URI`), a `.env` file listed in `.gitignore`, or **Colab Secrets** (`google.colab.userdata.get("MONGODB_URI")`). Never commit a URI with a password to GitHub; leaked credentials are scraped by bots within minutes.

### 4. Atlas features worth knowing

| Feature | What it does |
|---|---|
| **Data Explorer** | Compass-like browsing, queries and aggregations in the browser |
| **Performance Advisor** | suggests indexes from slow queries |
| **Real-Time Panel / Metrics** | operations, connections, latency |
| **Atlas Charts** | dashboards straight from collections; embed in web pages |
| **Atlas Search** | Lucene full-text search via `$search` (fuzzy matching, autocomplete, facets) |
| **Atlas Vector Search** | similarity search on embeddings via `$vectorSearch`: the database side of RAG and semantic search |
| **Triggers** | run a function when documents change or on a schedule |
| **Backups** | continuous cloud backups with point-in-time restore (dedicated tiers) |
| **Online Archive / Data Federation** | move cold data to cheap object storage; query S3 and Atlas together |
| **Atlas CLI** | `atlas setup`, `atlas clusters create`, scripted management |

> The older Atlas **Data API** (HTTPS endpoints) has been retired; new projects use a driver from their own back end.

## 🧭 Diagrams

```mermaid
flowchart LR
    subgraph Atlas["MongoDB Atlas project"]
      direction TB
      NA["Network access list"] --> CL
      DU["Database users"] --> CL
      CL["Cluster0 (M0)<br/>3-node replica set"]
      CL --> CH["Charts"]
      CL --> SE["Search / Vector Search"]
      CL --> TR["Triggers"]
    end
    Py["Python / Colab<br/>PyMongo"] -->|"mongodb+srv:// TLS"| NA
    Co["Compass"] --> NA
    Sh["mongosh"] --> NA
```

```mermaid
flowchart LR
    T["user question"] --> E["embedding model<br/>→ vector"]
    E --> V["$vectorSearch on Atlas<br/>nearest product vectors"]
    V --> R["top-k documents"]
    R --> L["LLM writes the answer<br/>(Term 2)"]
```

## 💻 Worked examples

### Example 1: Building and reading a connection string

📄 [`code/session-11_connection_strings.py`](code/session-11_connection_strings.py)

```python
# Session 11 · Atlas connection strings: build them safely and read them back
from urllib.parse import quote_plus, urlsplit, parse_qs

user = "hamna_app"
password = "K@rachi#2025"                  # special characters MUST be URL-encoded
cluster = "cluster0.ab1cd.mongodb.net"     # copied from Atlas > Connect > Drivers (example host)

uri = (f"mongodb+srv://{quote_plus(user)}:{quote_plus(password)}@{cluster}/kgs"
       "?retryWrites=true&w=majority&appName=KGSAnalytics")
print("Connection string:\n ", uri.replace(quote_plus(password), "<password>"))
print("\nEncoded password:", quote_plus(password), " (@ -> %40, # -> %23)")

parts = urlsplit(uri)
print("\nParsed back:")
print("  scheme   :", parts.scheme, "(+srv = look up the replica-set hosts in DNS)")
print("  user     :", parts.username)
print("  host     :", parts.hostname)
print("  database :", parts.path.lstrip("/"))
for k, v in parse_qs(parts.query).items():
    print(f"  option   : {k} = {v[0]}")

print("\nWhat +srv expands to (illustration): three replica-set members on port 27017")
for i in range(3):
    print(f"  {cluster.replace('cluster0.', f'cluster0-shard-00-0{i}.')}:27017")
```

**Output**

```text
Connection string:
  mongodb+srv://hamna_app:<password>@cluster0.ab1cd.mongodb.net/kgs?retryWrites=true&w=majority&appName=KGSAnalytics

Encoded password: K%40rachi%232025  (@ -> %40, # -> %23)

Parsed back:
  scheme   : mongodb+srv (+srv = look up the replica-set hosts in DNS)
  user     : hamna_app
  host     : cluster0.ab1cd.mongodb.net
  database : kgs
  option   : retryWrites = true
  option   : w = majority
  option   : appName = KGSAnalytics

What +srv expands to (illustration): three replica-set members on port 27017
  cluster0-shard-00-00.ab1cd.mongodb.net:27017
  cluster0-shard-00-01.ab1cd.mongodb.net:27017
  cluster0-shard-00-02.ab1cd.mongodb.net:27017
```


### Example 2: One client factory for laptop, Colab and Atlas


📄 [`code/session-11_atlas_client.py`](code/session-11_atlas_client.py)

```python
# Session 11 · One client factory for laptop, Colab and Atlas
# Put your Atlas URI in an environment variable (never in code or Git):
#     export MONGODB_URI="mongodb+srv://user:pass@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority"
# In Colab, use the key icon (Secrets) and read it with google.colab.userdata.get("MONGODB_URI").
import os
from store_db import get_db, PRODUCTS

def get_client():
    uri = os.environ.get("MONGODB_URI")
    if uri:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        client = MongoClient(uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
        where = "Atlas"
    else:
        import mongomock
        client = mongomock.MongoClient()
        where = "mongomock (set MONGODB_URI to use Atlas)"
    client.admin.command("ping")                 # fails fast if the URI, password or IP list is wrong
    return client, where

client, where = get_client()
print("Connected to:", where)

db = client["kgs"]
if db.products.count_documents({}) == 0:         # seed once
    db.products.insert_many([dict(p) for p in PRODUCTS])
print("products:", db.products.count_documents({}))

top = db.products.aggregate([{"$group": {"_id": "$category", "stockValue": {"$sum": {"$multiply": ["$price", "$stock"]}}}},
                             {"$sort": {"stockValue": -1}}, {"$limit": 3}])
for row in top:
    print(f"  {row['_id']:<12} Rs {row['stockValue']:>12,}")
```

**Output**

```text
Connected to: mongomock (set MONGODB_URI to use Atlas)
products: 10
  Computers    Rs    1,905,000
  Displays     Rs      312,000
  Audio        Rs      309,500
```


Run it once without `MONGODB_URI` (mongomock), then set the variable to your Atlas URI and run it again: the same code now talks to the cloud.

**mongosh / Compass equivalent**

```bash
mongosh "mongodb+srv://cluster0.ab1cd.mongodb.net/kgs" --apiVersion 1 --username hamna_app
```

```javascript
db.products.aggregate([
  { $group: { _id: "$category", stockValue: { $sum: { $multiply: ["$price", "$stock"] } } } },
  { $sort: { stockValue: -1 } }, { $limit: 3 } ])
```

In Compass: *New connection* → paste the URI → *Connect*.

### Example 3: The idea behind Atlas Vector Search

📄 [`code/session-11_vector_search_demo.py`](code/session-11_vector_search_demo.py)

```python
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
```

**Output**

```text
Query: 'something to listen to music on a trip'
   0.994  Bluetooth Speaker
   0.975  Noise-Cancelling Headphones
   0.591  Portable SSD 1TB

Query: 'gear for a gamer'
   0.971  Gaming Laptop
   0.850  Mechanical Keyboard
   0.505  Wireless Mouse
```


**On Atlas** you create a vector index on the `embedding` field (Atlas UI → *Search & Vector Search* → *Create index* → JSON editor):

```json
{ "fields": [ { "type": "vector", "path": "embedding", "numDimensions": 4, "similarity": "cosine" } ] }
```

and query it with:

```javascript
db.products.aggregate([
  { $vectorSearch: { index: "vector_index", path: "embedding",
                     queryVector: [0.1, 0.0, 1.0, 0.9], numCandidates: 50, limit: 3 } },
  { $project: { name: 1, score: { $meta: "vectorSearchScore" } } } ])
```

Real embeddings come from a model (hundreds or thousands of numbers each); Term 2 builds on this.

## 🧪 Lab / practice tasks

**1. 🟢 Easy:** Create a free Atlas account and an M0 cluster in the region closest to you. Add a database user and your IP address.

<details><summary>💡 Hint</summary>

Write down the user name; the password is shown only once.

</details>

**2. 🟢 Easy:** Load the sample dataset and, in Data Explorer, find movies in `sample_mflix.movies` released in 2015 with an IMDb rating above 8.

<details><summary>💡 Hint</summary>

Filter `{year: 2015, "imdb.rating": {$gt: 8}}`.

</details>

**3. 🟡 Medium:** Store your URI in Colab Secrets, run `session-11_atlas_client.py` against Atlas, and confirm the `kgs` database appears in Data Explorer.

<details><summary>💡 Hint</summary>

`os.environ["MONGODB_URI"] = userdata.get("MONGODB_URI")`

</details>

**4. 🟡 Medium:** Build an Atlas Chart: bar chart of total stock value per category from `kgs.products`.

<details><summary>💡 Hint</summary>

Charts → Add dashboard → data source `kgs.products`, aggregate `price * stock` with a calculated field.

</details>

**5. 🟠 Hard:** Create an Atlas Search index on `products.name` and run a fuzzy `$search` for "hedphones".

<details><summary>💡 Hint</summary>

`{text: {query: "hedphones", path: "name", fuzzy: {}}}`

</details>

**6. 🔴 Challenge:** Replace the 4-number vectors in `session-11_vector_search_demo.py` with your own feature scores for 10 university courses and build a "find similar courses" search. Then create the same data with a `$vectorSearch` index on Atlas.

<details><summary>💡 Hint</summary>

Keep `numDimensions` equal to your vector length.

</details>


## ✅ Quick quiz

**Q1.** Every Atlas cluster, even M0, runs as…

- A) a standalone server
- B) a 3-node replica set
- C) a sharded cluster
- D) a single container without replication

**Q2.** What does `+srv` in a connection string do?

- A) disables TLS
- B) looks up the cluster's hosts in DNS
- C) selects the server API version
- D) enables sharding

**Q3.** Your password is `P@ss#1`. What must you do before putting it in the URI?

- A) nothing
- B) URL-encode it
- C) base64-encode it
- D) wrap it in quotes

**Q4.** Which Atlas feature finds documents whose embeddings are closest to a query vector?

- A) Atlas Charts
- B) Atlas Triggers
- C) Atlas Vector Search
- D) Online Archive

**Q5.** Where should an Atlas URI with a password live in a project?

- A) hard-coded in the notebook
- B) in a public GitHub README
- C) in an environment variable or secrets manager
- D) in the database itself

<details><summary>✅ Show answers</summary>

1. **B**
2. **B**
3. **B**
4. **C**
5. **C**

</details>


## 📝 Summary

- Atlas runs MongoDB as a managed service on AWS, Google Cloud and Azure; M0 is free for learning.
- Setup: cluster → database user → network access → copy the `mongodb+srv://` URI.
- Encode special characters, keep the URI in environment variables or secrets, and use least-privilege users.
- Atlas adds Data Explorer, Performance Advisor, Charts, Search, **Vector Search**, Triggers and backups.
- The same PyMongo code runs against mongomock, a local server or Atlas; only the URI changes.

### 🎤 Interview / viva questions

1. What does Atlas manage for you, and what remains your responsibility?
2. Why is `0.0.0.0/0` in the access list risky?
3. Difference between your Atlas login and a database user?
4. How does Vector Search support a retrieval-augmented chatbot?
5. Which tier would you choose for a final-year project demo, and why?

---

[⬅ Previous: Session 10](session-10-mongodb-tools.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Next: Session 12 ➡](session-12-python-connectivity-pymongo.md)

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
