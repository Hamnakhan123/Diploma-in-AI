# Session 1 · The same order as relational rows and as one MongoDB document
import json

# Relational design: 3 tables, joined by keys
orders      = [{"OrderID": 5001, "CustomerID": 1, "OrderDate": "2025-03-02"}]
order_items = [{"OrderID": 5001, "ProductID": 101, "Qty": 2, "Price": 1500},
               {"OrderID": 5001, "ProductID": 107, "Qty": 1, "Price": 4500}]
customers   = [{"CustomerID": 1, "Name": "Ayesha Khan", "City": "Karachi"}]
print("Relational: rows spread over", 3, "tables ->",
      len(orders) + len(order_items) + len(customers), "rows to read with 2 joins")

# Document design: everything one screen needs lives in one document
cust = customers[0]
document = {
    "_id": orders[0]["OrderID"],
    "orderDate": orders[0]["OrderDate"],
    "customer": {"id": cust["CustomerID"], "name": cust["Name"], "city": cust["City"]},  # embedded copy
    "items": [{"productId": r["ProductID"], "qty": r["Qty"], "price": r["Price"]} for r in order_items],
}
document["total"] = sum(i["qty"] * i["price"] for i in document["items"])
print("Document: 1 read, no joins\n")
print(json.dumps(document, indent=2))

# Terminology map
pairs = [("Database", "Database"), ("Table", "Collection"), ("Row", "Document"),
         ("Column", "Field"), ("Primary key", "_id"), ("JOIN", "Embedding or $lookup"),
         ("Index", "Index")]
print("\n{:<12} | {}".format("RDBMS", "MongoDB"))
print("-" * 13 + "+" + "-" * 22)
for a, b in pairs:
    print("{:<12} | {}".format(a, b))
