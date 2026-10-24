# Session 10 · What the BI Connector does: present documents as SQL tables
# The BI Connector (and the newer Atlas SQL Interface) maps each collection to a table,
# flattens sub-documents into columns and turns arrays into child tables, so tools such as
# Power BI, Tableau or Excel can query MongoDB with SQL. This file performs the same mapping
# into SQLite and runs the kind of SQL a BI tool would send.
import sqlite3
from store_db import get_db

db = get_db()
sql = sqlite3.connect(":memory:")

sql.execute("CREATE TABLE products (_id INT, name TEXT, category TEXT, price INT, stock INT, `specs.brand` TEXT)")
sql.execute("CREATE TABLE orders (_id INT, customerId INT, orderDate TEXT, status TEXT, payment TEXT)")
sql.execute("CREATE TABLE orders_items (_id INT, items_idx INT, `items.productId` INT, `items.qty` INT, `items.price` INT)")
sql.execute("CREATE TABLE customers (_id INT, name TEXT, city TEXT, loyalty TEXT)")

for p in db.products.find():
    sql.execute("INSERT INTO products VALUES (?,?,?,?,?,?)", (p["_id"], p["name"], p["category"], p["price"], p["stock"], p["specs"]["brand"]))
for o in db.orders.find():
    sql.execute("INSERT INTO orders VALUES (?,?,?,?,?)", (o["_id"], o["customerId"], o["orderDate"].date().isoformat(), o["status"], o["payment"]))
    for i, it in enumerate(o["items"]):                  # array -> child table with an index column
        sql.execute("INSERT INTO orders_items VALUES (?,?,?,?,?)", (o["_id"], i, it["productId"], it["qty"], it["price"]))
for c in db.customers.find():
    sql.execute("INSERT INTO customers VALUES (?,?,?,?)", (c["_id"], c["name"], c["city"], c["loyalty"]))

print("Tables a BI tool would see:", [r[0] for r in sql.execute("SELECT name FROM sqlite_master")])

query = """
SELECT c.city,
       COUNT(DISTINCT o._id)                      AS orders,
       SUM(i.`items.qty` * i.`items.price`)       AS revenue
FROM orders o
JOIN orders_items i ON i._id = o._id
JOIN customers   c ON c._id = o.customerId
WHERE o.status = 'Delivered'
GROUP BY c.city
ORDER BY revenue DESC;
"""
print("\nSQL sent by a dashboard:\n" + query.strip())
print("\n{:<10} {:>6} {:>10}".format("city", "orders", "revenue"))
for city, n, rev in sql.execute(query):
    print("{:<10} {:>6} {:>10,}".format(city, n, rev))
