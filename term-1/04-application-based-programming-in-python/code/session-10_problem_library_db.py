"""
Session 10 · Real-life problem: a library management database
-------------------------------------------------------------
PROBLEM
The department library tracks books on paper. Design and code a database that
  1. has three related tables: books, members, loans (with foreign keys),
  2. lets a member BORROW a book only if a copy is available and they have
     fewer than 3 active loans - inside a transaction,
  3. RETURNS books and charges Rs 20 per late day (14-day loan period),
  4. reports overdue loans (JOIN) and the most borrowed categories, with a chart.
Run:  python session-10_problem_library_db.py
"""
import sqlite3
from datetime import date, timedelta

LOAN_DAYS, FINE_PER_DAY, MAX_LOANS = 14, 20, 3

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE books   (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL,
                      copies INTEGER NOT NULL CHECK (copies >= 0));
CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT NOT NULL, kind TEXT CHECK (kind IN ('student','staff')));
CREATE TABLE loans   (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id),
                      member_id INTEGER NOT NULL REFERENCES members(id),
                      borrowed TEXT NOT NULL, due TEXT NOT NULL, returned TEXT, fine INTEGER DEFAULT 0);
""")
db.executemany("INSERT INTO books VALUES (?, ?, ?, ?)", [
    (1, "Python Crash Course", "programming", 2), (2, "Think Stats", "statistics", 1),
    (3, "Hands-On Machine Learning", "ai", 2), (4, "Database System Concepts", "databases", 1),
    (5, "Automate the Boring Stuff", "programming", 1)])
db.executemany("INSERT INTO members VALUES (?, ?, ?)", [
    (1, "Ayesha", "student"), (2, "Omar", "student"), (3, "Mr Kamran", "staff")])
db.commit()

class LibraryError(Exception):
    pass

def borrow(member_id, book_id, day):
    """Check the rules and record a loan atomically."""
    with db:                                             # one transaction
        book = db.execute("SELECT title, copies FROM books WHERE id = ?", (book_id,)).fetchone()
        if book is None:
            raise LibraryError(f"no book with id {book_id}")
        active = db.execute("SELECT COUNT(*) FROM loans WHERE member_id = ? AND returned IS NULL",
                            (member_id,)).fetchone()[0]
        if active >= MAX_LOANS:
            raise LibraryError(f"member {member_id} already has {active} books")
        if book["copies"] == 0:
            raise LibraryError(f"'{book['title']}' is not available")
        db.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (book_id,))
        db.execute("INSERT INTO loans (book_id, member_id, borrowed, due) VALUES (?, ?, ?, ?)",
                   (book_id, member_id, day.isoformat(), (day + timedelta(days=LOAN_DAYS)).isoformat()))
    return book["title"]

def give_back(loan_id, day):
    with db:
        loan = db.execute("SELECT * FROM loans WHERE id = ? AND returned IS NULL", (loan_id,)).fetchone()
        if loan is None:
            raise LibraryError(f"loan {loan_id} is not open")
        late = max(0, (day - date.fromisoformat(loan["due"])).days)
        db.execute("UPDATE loans SET returned = ?, fine = ? WHERE id = ?", (day.isoformat(), late * FINE_PER_DAY, loan_id))
        db.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (loan["book_id"],))
    return late * FINE_PER_DAY

d = date(2026, 9, 1)
events = [("borrow", 1, 1, d), ("borrow", 1, 2, d), ("borrow", 2, 2, d + timedelta(1)),
          ("borrow", 1, 3, d + timedelta(2)), ("borrow", 1, 4, d + timedelta(2)), ("borrow", 3, 3, d + timedelta(3)),
          ("borrow", 2, 1, d + timedelta(5)), ("borrow", 3, 5, d + timedelta(6)), ("borrow", 2, 9, d + timedelta(6))]
for kind, member, book, day in events:
    try:
        print(f"{day} member {member} borrows '{borrow(member, book, day)}'")
    except LibraryError as e:
        print(f"{day} member {member} REFUSED: {e}")

for loan_id, day in [(1, date(2026, 9, 10)), (2, date(2026, 9, 20)), (2, date(2026, 9, 21))]:
    try:
        print(f"{day} loan {loan_id} returned, fine Rs {give_back(loan_id, day)}")
    except LibraryError as e:
        print(f"{day} REFUSED: {e}")

today = date(2026, 9, 25)
print(f"\nOverdue on {today}:")
sql = """SELECT m.name, b.title, l.due, julianday(?) - julianday(l.due) AS days_late
         FROM loans l JOIN members m ON m.id = l.member_id JOIN books b ON b.id = l.book_id
         WHERE l.returned IS NULL AND l.due < ? ORDER BY days_late DESC"""
for r in db.execute(sql, (today.isoformat(), today.isoformat())):
    print(f"  {r['name']:<9} {r['title']:<28} due {r['due']}  {int(r['days_late'])} days late "
          f"(fine so far Rs {int(r['days_late']) * FINE_PER_DAY})")

print("\nAvailability:", [(r["title"][:22], r["copies"]) for r in db.execute("SELECT title, copies FROM books")])
cats = db.execute("""SELECT b.category, COUNT(*) AS loans FROM loans l JOIN books b ON b.id = l.book_id
                     GROUP BY b.category ORDER BY loans DESC, b.category""").fetchall()
print("Loans by category:", [(c["category"], c["loans"]) for c in cats])
print("Fines collected: Rs", db.execute("SELECT SUM(fine) FROM loans").fetchone()[0])

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.bar([c["category"] for c in cats], [c["loans"] for c in cats], color="#A78BFA")
ax.set_ylabel("loans"); ax.set_title("Which subjects do members borrow most?")
fig.tight_layout(); fig.savefig("session-10_problem_library_db.png", dpi=110)
print("Chart saved: session-10_problem_library_db.png")
