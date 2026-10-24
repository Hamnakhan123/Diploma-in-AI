# 📝 Practice Test: Managing Large Datasets with MongoDB

> 🧭 [Diploma in AI](../../README.md) › [Term 1](../README.md) › [Managing Large Datasets with MongoDB](README.md) › **Practice test**
>
> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Attempt every question before opening the answers. Aim for 16/20 or better on Part A, then try the scenarios in Part B.

---

## Part A · 20 multiple-choice questions

**Q1.** Which NoSQL family does MongoDB belong to?

- A) Key-value
- B) Document
- C) Wide-column
- D) Graph

**Q2.** What is the maximum size of one BSON document?

- A) 1 MB
- B) 16 MB
- C) 100 MB
- D) unlimited

**Q3.** You should **reference** rather than embed a child when it…

- A) is always read with the parent
- B) has a small, fixed size
- C) is shared by many parents or grows without limit
- D) belongs to only one parent

**Q4.** `db.products.find({}, {name: 1, _id: 0})` returns…

- A) every field except name
- B) only the name field
- C) name and _id
- D) an error

**Q5.** Which call inserts a document if no match is found, otherwise updates it?

- A) updateOne(f, u, {multi: true})
- B) updateOne(f, u, {upsert: true})
- C) insertOne(doc, {replace: true})
- D) replaceOne(f, doc, {create: true})

**Q6.** Which filter finds customers whose `email` field is **missing** (not just null)?

- A) {email: null}
- B) {email: {$exists: false}}
- C) {email: ""}
- D) {email: {$type: "null"}}

**Q7.** Which operator ensures that several conditions are met by the **same** array element?

- A) $all
- B) $elemMatch
- C) $in
- D) $size

**Q8.** Which update adds a value to an array only if it is not already present?

- A) $push
- B) $addToSet
- C) $set
- D) $inc

**Q9.** In an aggregation, which stage behaves like a SQL LEFT OUTER JOIN?

- A) $unwind
- B) $lookup
- C) $merge
- D) $facet

**Q10.** In `$group`, what does `{n: {$sum: 1}}` compute?

- A) the sum of field n
- B) the number of documents in each group
- C) always 1
- D) the first document

**Q11.** Why should `$match` normally come at the start of a pipeline?

- A) it is required syntax
- B) it shrinks the stream early and can use an index
- C) it formats the output
- D) it enables $out

**Q12.** Which command reply means failure?

- A) {ok: 1}
- B) {ok: 0, errmsg: "...", code: 59}
- C) {n: 0, ok: 1}
- D) {cursor: {firstBatch: []}, ok: 1}

**Q13.** Which method removes the oldest queued job and returns it in one atomic step?

- A) deleteOne
- B) findOneAndDelete with a sort
- C) remove
- D) distinct

**Q14.** For `find({status: "Delivered", amount: {$gt: 1000}}).sort({orderDate: -1})`, which index follows the ESR rule?

- A) {amount: 1, status: 1, orderDate: -1}
- B) {orderDate: -1, amount: 1, status: 1}
- C) {status: 1, orderDate: -1, amount: 1}
- D) {status: 1, amount: 1}

**Q15.** In `explain("executionStats")`, which stage name means a full collection scan?

- A) IXSCAN
- B) FETCH
- C) COLLSCAN
- D) PROJECTION

**Q16.** In a replica set, which member accepts writes?

- A) every member
- B) the primary
- C) the arbiter
- D) the hidden member

**Q17.** Why is an ever-increasing `_id` a poor **ranged** shard key?

- A) it cannot be indexed
- B) every new insert goes to the same shard
- C) it has too few values
- D) mongos cannot route it

**Q18.** Multi-document transactions are **not** available on…

- A) a 3-member replica set
- B) an Atlas M0 cluster
- C) a standalone mongod
- D) a sharded cluster on 4.2+

**Q19.** Which tool creates a binary backup that keeps all BSON types and index definitions?

- A) mongoexport
- B) mongodump
- C) mongoimport
- D) bsondump

**Q20.** Your Atlas password is `Lab@2025`. In a connection string you must…

- A) write it as is
- B) URL-encode `@` as `%40`
- C) base64-encode it
- D) remove the `@`

<details><summary>✅ Show answers</summary>

1. **B**
2. **B**
3. **C**
4. **B**
5. **B**
6. **B**
7. **B**
8. **B**
9. **B**
10. **B**
11. **B**
12. **B**
13. **B**
14. **C**
15. **C**
16. **B**
17. **B**
18. **C**
19. **B**
20. **B**

</details>


## Part B · Practical / scenario questions

Use the sample database built by [`code/store_db.py`](code/store_db.py) (`get_db()`), or load the same data into your own server.

**Scenario 1 · Payment report.** Finance wants, for **delivered** orders only, the number of orders, total revenue and average order value **per payment method**, highest revenue first.

<details><summary>✅ Solution</summary>

```javascript
db.orders.aggregate([
  { $match: { status: "Delivered" } },
  { $unwind: "$items" },
  { $group: { _id: "$_id", payment: { $first: "$payment" },                  // rebuild order totals
              total: { $sum: { $multiply: ["$items.qty", "$items.price"] } } } },
  { $group: { _id: "$payment", orders: { $sum: 1 },
              revenue: { $sum: "$total" }, avgOrder: { $avg: "$total" } } },
  { $sort: { revenue: -1 } }
])
```

Result on the sample data:

```text
{ _id: "Card", orders: 4, revenue: 310500, avgOrder: 77625 }
{ _id: "COD",  orders: 2, revenue: 61000,  avgOrder: 30500 }
```

Check: Card = 7,500 + 32,000 + 211,500 + 59,500 = 310,500. The two `$group` stages are needed because an order total must be computed before averaging per payment method; averaging item lines directly would give a different (wrong) "average order value".

</details>

**Scenario 2 · Slow customer page.** The "My orders" page runs `db.orders.find({customerId: 4242, status: {$ne: "Cancelled"}}).sort({orderDate: -1}).limit(10)` on 5 million orders and takes 3 seconds. `explain()` shows `COLLSCAN` and an in-memory `SORT`. Propose an index, show how you would verify it, and say what you would expect in the new plan.

<details><summary>✅ Solution</summary>

```javascript
db.orders.createIndex({ customerId: 1, orderDate: -1 })     // E: customerId, S: orderDate
db.orders.find({ customerId: 4242, status: { $ne: "Cancelled" } })
         .sort({ orderDate: -1 }).limit(10)
         .explain("executionStats")
```

- **Equality** on `customerId` first, then the **sort** field `orderDate`, so the index returns that customer's orders already newest-first: no in-memory `SORT` stage.
- `status: {$ne: …}` is a poor index field (it matches almost everything); it is applied as a filter on the few fetched documents. Adding it as a third field (`{customerId: 1, orderDate: -1, status: 1}`) lets the server reject cancelled orders while scanning index keys, which helps only if cancellations are common.
- Expected plan: `LIMIT → FETCH (filter status) → IXSCAN {customerId: 1, orderDate: -1}`, `totalKeysExamined` and `totalDocsExamined` around 10-12, `executionTimeMillis` in single digits.
- In PyMongo: `db.orders.create_index([("customerId", 1), ("orderDate", -1)])`.

</details>

**Scenario 3 · Never oversell.** Two cashiers sometimes sell the last unit of a product at the same moment, and occasionally the stock is reduced but the order is never saved because the app crashes in between. Write PyMongo code that (a) never lets stock go below zero and (b) saves the stock change and the order together or not at all. State what deployment this needs.

<details><summary>✅ Solution</summary>

```python
import os
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

client = MongoClient(os.environ["MONGODB_URI"])        # replica set or Atlas (not a standalone server)
db = client.kgs

def place_order(order_id, customer_id, product_id, qty):
    def callback(session):
        # (a) conditional update: check and decrement in ONE atomic step
        p = db.products.find_one_and_update(
            {"_id": product_id, "stock": {"$gte": qty}},
            {"$inc": {"stock": -qty}},
            projection={"price": 1}, session=session)
        if p is None:
            raise ValueError("not enough stock")         # aborts the transaction
        # (b) the order is written in the same transaction
        db.orders.insert_one({"_id": order_id, "customerId": customer_id, "status": "Pending",
                              "items": [{"productId": product_id, "qty": qty, "price": p["price"]}]},
                             session=session)
    with client.start_session() as s:
        s.with_transaction(callback, write_concern=WriteConcern(w="majority"))
```

- The filter `stock: {$gte: qty}` makes the decrement conditional, so two cashiers can never both take the last unit: the second update matches nothing.
- `with_transaction` commits both writes together, aborts both on any exception (including a crash before commit), and retries automatically on `TransientTransactionError` such as a write conflict.
- Needs a **replica set** or sharded cluster (a free **Atlas M0** cluster works); a standalone `mongod` does not support transactions. `w: "majority"` makes the commit survive a failover.

</details>

---

[⬅ Last session](session-12-python-connectivity-pymongo.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Term 1 overview](../README.md)

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
