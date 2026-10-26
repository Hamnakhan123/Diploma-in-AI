"""
Session 10 · Example 1: connecting Python to a database (SQLite)
----------------------------------------------------------------
The DB-API pattern is the same for SQLite, MySQL, PostgreSQL and SQL Server:
  connect -> cursor -> execute (with parameters) -> fetch / commit -> close
SQLite is built into Python and stores the database in one file (or memory).
Run:  python session-10_connect_sqlite.py
"""
import sqlite3

# 1. Connect (":memory:" = a temporary database in RAM; use "campus.db" for a file)
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
print("SQLite library version:", sqlite3.sqlite_version)

# 2. Create a table (DDL)
cur.execute("""
    CREATE TABLE students (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        roll    TEXT    NOT NULL UNIQUE,
        name    TEXT    NOT NULL,
        city    TEXT    DEFAULT 'Karachi',
        cgpa    REAL    CHECK (cgpa BETWEEN 0 AND 4)
    )""")

# 3. Insert rows with PARAMETERS (? placeholders) - never build SQL with f-strings
cur.execute("INSERT INTO students (roll, name, city, cgpa) VALUES (?, ?, ?, ?)",
            ("AI-01", "Ali Khan", "Karachi", 3.1))
print("first insert got id:", cur.lastrowid)
rows = [("AI-02", "Sana Tariq", "Lahore", 3.8), ("AI-03", "Bilal Ahmed", "Karachi", 2.7),
        ("AI-04", "Hira Shah", "Quetta", 3.5), ("AI-05", "Omar Farooq", "Karachi", 3.3)]
cur.executemany("INSERT INTO students (roll, name, city, cgpa) VALUES (?, ?, ?, ?)", rows)
conn.commit()                                     # make the changes permanent
print("rows inserted by executemany:", cur.rowcount)

# 4. Read: fetchone, fetchmany, fetchall
cur.execute("SELECT roll, name, cgpa FROM students ORDER BY cgpa DESC")
print("fetchone :", cur.fetchone())
print("fetchmany:", cur.fetchmany(2))
print("fetchall :", cur.fetchall())

# 5. Parameters in WHERE clauses; named placeholders also work
cur.execute("SELECT name FROM students WHERE city = :city AND cgpa >= :min", {"city": "Karachi", "min": 3.0})
print("Karachi students with CGPA >= 3:", [r[0] for r in cur.fetchall()])

# 6. Rows as dictionaries with row_factory
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT * FROM students WHERE roll = ?", ("AI-04",)).fetchone()
print("sqlite3.Row:", dict(row), "| access by name:", row["name"])
conn.row_factory = None

# 7. Update and delete report how many rows changed
cur.execute("UPDATE students SET cgpa = cgpa + 0.1 WHERE city = ?", ("Karachi",))
print("updated rows:", cur.rowcount)
cur.execute("DELETE FROM students WHERE roll = ?", ("AI-03",))
print("deleted rows:", cur.rowcount)
conn.commit()

# 8. Constraint violations raise exceptions you can handle
for bad in [("AI-01", "Duplicate Roll", "Karachi", 3.0), ("AI-09", "Too High", "Karachi", 4.7)]:
    try:
        cur.execute("INSERT INTO students (roll, name, city, cgpa) VALUES (?, ?, ?, ?)", bad)
    except sqlite3.IntegrityError as e:
        print("IntegrityError:", e)

# 9. Aggregates
cur.execute("SELECT city, COUNT(*), ROUND(AVG(cgpa), 2) FROM students GROUP BY city ORDER BY 2 DESC, city")
print("by city:", cur.fetchall())

# 10. Why parameters matter: SQL injection
attack = "x' OR '1'='1"
unsafe_sql = f"SELECT COUNT(*) FROM students WHERE name = '{attack}'"      # DON'T do this
print("\nunsafe query text:", unsafe_sql)
print("  rows matched by the UNSAFE query:", cur.execute(unsafe_sql).fetchone()[0], "<- attacker sees everything")
print("  rows matched with a parameter   :", cur.execute("SELECT COUNT(*) FROM students WHERE name = ?", (attack,)).fetchone()[0])

conn.close()
print("connection closed")
