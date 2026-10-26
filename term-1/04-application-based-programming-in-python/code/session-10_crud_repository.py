"""
Session 10 · Example 2: a data-access layer with CRUD functions and transactions
--------------------------------------------------------------------------------
Wrapping all SQL in one class (a "repository") keeps the rest of the program
free of SQL and makes it easy to switch from SQLite to MySQL later.
Run:  python session-10_crud_repository.py
"""
import sqlite3
from contextlib import closing

class StudentRepository:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                roll TEXT PRIMARY KEY, name TEXT NOT NULL, phone TEXT, cgpa REAL CHECK (cgpa BETWEEN 0 AND 4));
            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY, roll TEXT NOT NULL REFERENCES students(roll) ON DELETE CASCADE,
                amount INTEGER NOT NULL CHECK (amount > 0), paid_on TEXT NOT NULL);
        """)

    # ----- Create -----
    def add(self, roll, name, phone=None, cgpa=None):
        with self.conn:                                   # commits on success, rolls back on error
            self.conn.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (roll, name, phone, cgpa))

    # ----- Read -----
    def get(self, roll):
        row = self.conn.execute("SELECT * FROM students WHERE roll = ?", (roll,)).fetchone()
        return dict(row) if row else None

    def search(self, text="", min_cgpa=0.0):
        sql = "SELECT * FROM students WHERE name LIKE ? AND IFNULL(cgpa, 0) >= ? ORDER BY name"
        return [dict(r) for r in self.conn.execute(sql, (f"%{text}%", min_cgpa))]

    # ----- Update -----
    def update(self, roll, /, **fields):          # '/' lets 'roll' also appear in **fields
        allowed = {"name", "phone", "cgpa"}
        if not fields or not set(fields) <= allowed:      # e.g. changing the primary key is refused
            raise ValueError(f"can only update {sorted(allowed)}")
        sets = ", ".join(f"{k} = ?" for k in fields)          # column names come from our whitelist
        with self.conn:
            cur = self.conn.execute(f"UPDATE students SET {sets} WHERE roll = ?", (*fields.values(), roll))
        return cur.rowcount

    # ----- Delete -----
    def delete(self, roll):
        with self.conn:
            return self.conn.execute("DELETE FROM students WHERE roll = ?", (roll,)).rowcount

    # ----- A transaction across two tables -----
    def pay_fee_instalments(self, roll, amounts, day):
        """All instalments are recorded, or none are (atomicity)."""
        with self.conn:
            for amt in amounts:
                self.conn.execute("INSERT INTO fees (roll, amount, paid_on) VALUES (?, ?, ?)", (roll, amt, day))

    def fee_report(self):
        sql = """SELECT s.roll, s.name, COUNT(f.id) AS payments, IFNULL(SUM(f.amount), 0) AS total
                 FROM students s LEFT JOIN fees f ON f.roll = s.roll GROUP BY s.roll ORDER BY total DESC"""
        return [dict(r) for r in self.conn.execute(sql)]

repo = StudentRepository()
for r in [("AI-01", "Ali Khan", "0300-1111111", 3.1), ("AI-02", "Sana Tariq", "0321-2222222", 3.8),
          ("AI-03", "Bilal Ahmed", None, 2.7), ("AI-04", "Hira Shah", "0333-4444444", 3.5)]:
    repo.add(*r)
print("get AI-02     :", repo.get("AI-02"))
print("search 'a', cgpa>=3.2:", [s["name"] for s in repo.search("a", 3.2)])
print("update phone  :", repo.update("AI-03", phone="0345-3333333"), "row(s)")
try:
    repo.update("AI-03", roll="AI-99")
except ValueError as e:
    print("update refused:", e)
try:
    repo.add("AI-01", "Someone Else")
except sqlite3.IntegrityError as e:
    print("add refused   :", e)

repo.pay_fee_instalments("AI-01", [25_000, 25_000], "2026-10-01")
try:
    repo.pay_fee_instalments("AI-02", [30_000, -5], "2026-10-02")    # second amount breaks the CHECK
except sqlite3.IntegrityError as e:
    print("transaction rolled back:", e)
print("fee report    :", repo.fee_report())
print("delete AI-01  :", repo.delete("AI-01"), "row(s); its fee rows cascade ->",
      repo.conn.execute("SELECT COUNT(*) FROM fees").fetchone()[0], "fee rows left")
with closing(repo.conn):
    print("students left :", [s["roll"] for s in repo.search()])
