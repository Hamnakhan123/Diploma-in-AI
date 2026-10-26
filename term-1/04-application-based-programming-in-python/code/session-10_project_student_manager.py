"""
Session 10 · Mini project: a student records manager (Tkinter + SQLite CRUD)
---------------------------------------------------------------------------
A desktop app to INSERT, UPDATE, DELETE and SEARCH student records stored in
a SQLite database file (students.db).
  - StudentDB   : all SQL (parameterised queries, transactions, validation)
  - StudentApp  : the Tkinter window (form + Treeview table + buttons)
Clicking a row in the table loads it into the form for editing.
Run:  python session-10_project_student_manager.py
(no screen? it runs the same database operations in test mode)
"""
import os
import re
import sqlite3
from gui_support import gui_available, banner

class StudentDB:
    FIELDS = ("roll", "name", "program", "phone", "cgpa")

    def __init__(self, path="students.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY, name TEXT NOT NULL, program TEXT NOT NULL,
            phone TEXT, cgpa REAL CHECK (cgpa BETWEEN 0 AND 4))""")
        self.conn.commit()

    @staticmethod
    def validate(rec):
        errors = []
        if not re.fullmatch(r"AI-\d{2}", rec["roll"]): errors.append("roll must look like AI-07")
        if len(rec["name"].strip()) < 3: errors.append("name is too short")
        if rec["phone"] and not re.fullmatch(r"03\d{2}-\d{7}", rec["phone"]): errors.append("phone must be 03XX-XXXXXXX")
        try:
            if not 0 <= float(rec["cgpa"]) <= 4: errors.append("CGPA must be 0-4")
        except ValueError:
            errors.append("CGPA must be a number")
        if errors:
            raise ValueError("; ".join(errors))
        return {**rec, "name": rec["name"].strip().title(), "cgpa": round(float(rec["cgpa"]), 2)}

    def insert(self, rec):
        rec = self.validate(rec)
        try:
            with self.conn:
                self.conn.execute("INSERT INTO students VALUES (:roll, :name, :program, :phone, :cgpa)", rec)
        except sqlite3.IntegrityError:
            raise ValueError(f"roll {rec['roll']} already exists") from None

    def update(self, rec):
        rec = self.validate(rec)
        with self.conn:
            n = self.conn.execute("""UPDATE students SET name=:name, program=:program, phone=:phone, cgpa=:cgpa
                                     WHERE roll=:roll""", rec).rowcount
        if n == 0:
            raise ValueError(f"roll {rec['roll']} not found")

    def delete(self, roll):
        with self.conn:
            if self.conn.execute("DELETE FROM students WHERE roll = ?", (roll,)).rowcount == 0:
                raise ValueError(f"roll {roll} not found")

    def search(self, text=""):
        like = f"%{text}%"
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM students WHERE roll LIKE ? OR name LIKE ? OR program LIKE ? ORDER BY roll",
            (like, like, like))]

    def stats(self):
        r = self.conn.execute("SELECT COUNT(*) n, ROUND(AVG(cgpa), 2) avg, MAX(cgpa) best FROM students").fetchone()
        return dict(r)

def run_gui(db):
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("Student records")
    form = tk.LabelFrame(root, text="Student", padx=8, pady=6); form.pack(fill="x", padx=8, pady=6)
    vars_ = {f: tk.StringVar() for f in StudentDB.FIELDS}
    for r, f in enumerate(StudentDB.FIELDS):
        tk.Label(form, text=f.title()).grid(row=r, column=0, sticky="w")
        if f == "program":
            ttk.Combobox(form, textvariable=vars_[f], values=["Diploma in AI", "Data Science", "Web Development"],
                         state="readonly", width=27).grid(row=r, column=1, pady=2)
        else:
            tk.Entry(form, textvariable=vars_[f], width=30).grid(row=r, column=1, pady=2)
    buttons = tk.Frame(root); buttons.pack(fill="x", padx=8)
    search = tk.StringVar()
    table = ttk.Treeview(root, columns=StudentDB.FIELDS, show="headings", height=8)
    for f in StudentDB.FIELDS:
        table.heading(f, text=f.title()); table.column(f, width=110)
    table.pack(fill="both", expand=True, padx=8, pady=6)
    status = tk.Label(root, anchor="w", relief="sunken"); status.pack(fill="x", side="bottom")

    def record():
        return {f: v.get().strip() for f, v in vars_.items()}
    def refresh():
        table.delete(*table.get_children())
        for s in db.search(search.get()):
            table.insert("", "end", iid=s["roll"], values=[s[f] for f in StudentDB.FIELDS])
        st = db.stats(); status.config(text=f"{st['n']} students | average CGPA {st['avg']} | best {st['best']}")
    def action(fn, ok_msg):
        try:
            fn(); refresh(); status.config(text=ok_msg)
        except ValueError as e:
            messagebox.showerror("Cannot save", str(e))
    def on_select(_event):
        sel = table.selection()
        if sel:
            for f, value in zip(StudentDB.FIELDS, table.item(sel[0])["values"]):
                vars_[f].set(value)
    def clear():
        for v in vars_.values(): v.set("")
    for text, cmd in [("Insert", lambda: action(lambda: db.insert(record()), "Inserted")),
                      ("Update", lambda: action(lambda: db.update(record()), "Updated")),
                      ("Delete", lambda: messagebox.askyesno("Delete", "Delete this student?")
                                 and action(lambda: db.delete(vars_["roll"].get()), "Deleted")),
                      ("Clear", clear)]:
        tk.Button(buttons, text=text, width=9, command=cmd).pack(side="left", padx=2)
    tk.Entry(buttons, textvariable=search, width=16).pack(side="right")
    tk.Label(buttons, text="Search").pack(side="right")
    search.trace_add("write", lambda *_: refresh())          # live search while typing
    table.bind("<<TreeviewSelect>>", on_select)
    refresh(); root.mainloop()

if gui_available():
    run_gui(StudentDB())
else:
    banner("student_manager")
    path = "students_demo.db"
    if os.path.exists(path): os.remove(path)
    db = StudentDB(path)
    def show(label, fn):
        try:
            fn(); print(f"{label:<44} ok")
        except ValueError as e:
            print(f"{label:<44} error: {e}")
    rec = lambda roll, name, prog, phone, cgpa: dict(roll=roll, name=name, program=prog, phone=phone, cgpa=cgpa)
    show("Insert AI-01 ayesha siddiqui", lambda: db.insert(rec("AI-01", "ayesha siddiqui", "Diploma in AI", "0321-7654321", "3.72")))
    show("Insert AI-02 Omar Farooq", lambda: db.insert(rec("AI-02", "Omar Farooq", "Data Science", "", "3.1")))
    show("Insert AI-03 Hira Shah", lambda: db.insert(rec("AI-03", "Hira Shah", "Diploma in AI", "0333-4444444", "3.45")))
    show("Insert AI-01 again", lambda: db.insert(rec("AI-01", "Someone", "Data Science", "", "2.0")))
    show("Insert bad form", lambda: db.insert(rec("7", "Al", "Diploma in AI", "12345", "five")))
    show("Update AI-02 cgpa -> 3.35", lambda: db.update(rec("AI-02", "Omar Farooq", "Data Science", "0300-1112233", "3.35")))
    show("Update AI-09 (does not exist)", lambda: db.update(rec("AI-09", "Nobody Here", "Data Science", "", "2")))
    print("\nTable (search ''):")
    for s in db.search():
        print(f"  {s['roll']}  {s['name']:<16} {s['program']:<14} {s['phone'] or '-':<13} {s['cgpa']}")
    print("Search 'diploma':", [s["roll"] for s in db.search("diploma")])
    show("Delete AI-03", lambda: db.delete("AI-03"))
    print("Status bar:", db.stats())
    db.conn.close()
    reopened = StudentDB(path)              # data is really on disk
    print("After reopening the database file:", [s["roll"] for s in reopened.search()])
    reopened.conn.close(); os.remove(path)
