"""
Session 9 · Mini project: a to-do manager desktop app with saved tasks
----------------------------------------------------------------------
Features: add tasks with a priority, mark done (double-click), delete,
filter (all / pending / done), counts in a status bar, a menu bar with
File > Save / Quit, keyboard shortcut Ctrl+S, and automatic save to a
JSON file so tasks survive restarts (Session 5).
Architecture: TodoStore (data + rules + persistence) / TodoApp (widgets).
Run:  python session-09_project_todo_app.py
"""
import json
import os
from gui_support import gui_available, banner

PRIORITIES = ["high", "normal", "low"]

class TodoStore:
    def __init__(self, path="todo.json"):
        self.path, self.tasks = path, []
        self.load()
    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)
    def add(self, text, priority="normal"):
        text = text.strip()
        if not text:
            raise ValueError("task text is empty")
        if priority not in PRIORITIES:
            raise ValueError(f"priority must be one of {PRIORITIES}")
        if any(t["text"].lower() == text.lower() and not t["done"] for t in self.tasks):
            raise ValueError(f"'{text}' is already on the list")
        self.tasks.append({"text": text, "priority": priority, "done": False})
        self.save()
    def toggle(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]; self.save()
    def delete(self, index):
        del self.tasks[index]; self.save()
    def view(self, show="all"):
        """(original_index, task) pairs, filtered and sorted: pending first, then by priority."""
        rows = [(i, t) for i, t in enumerate(self.tasks)
                if show == "all" or (show == "done") == t["done"]]
        return sorted(rows, key=lambda r: (r[1]["done"], PRIORITIES.index(r[1]["priority"])))
    def counts(self):
        done = sum(t["done"] for t in self.tasks)
        return {"total": len(self.tasks), "done": done, "pending": len(self.tasks) - done}

def label(task):
    mark = "✔" if task["done"] else "•"
    return f"{mark} [{task['priority']:>6}] {task['text']}"

class TodoApp:
    def __init__(self, store):
        import tkinter as tk
        from tkinter import messagebox
        self.tk, self.msg, self.store = tk, messagebox, store
        self.root = tk.Tk(); self.root.title("To-do manager"); self.root.geometry("440x380")
        menu = tk.Menu(self.root)
        filemenu = tk.Menu(menu, tearoff=False)
        filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        filemenu.add_separator(); filemenu.add_command(label="Quit", command=self.root.destroy)
        menu.add_cascade(label="File", menu=filemenu); self.root.config(menu=menu)
        top = tk.Frame(self.root, pady=6); top.pack(fill="x")
        self.entry = tk.Entry(top, width=28); self.entry.pack(side="left", padx=6)
        self.prio = tk.StringVar(value="normal")
        tk.OptionMenu(top, self.prio, *PRIORITIES).pack(side="left")
        tk.Button(top, text="Add", command=self.add).pack(side="left", padx=4)
        self.show = tk.StringVar(value="all")
        filt = tk.Frame(self.root); filt.pack(fill="x", padx=6)
        for s in ("all", "pending", "done"):
            tk.Radiobutton(filt, text=s, value=s, variable=self.show, command=self.refresh).pack(side="left")
        self.listbox = tk.Listbox(self.root, font=("Segoe UI", 11)); self.listbox.pack(fill="both", expand=True, padx=6)
        self.listbox.bind("<Double-Button-1>", lambda e: self.toggle())
        tk.Button(self.root, text="Delete selected", command=self.delete).pack(pady=4)
        self.status = tk.Label(self.root, anchor="w", relief="sunken"); self.status.pack(fill="x", side="bottom")
        self.root.bind("<Return>", lambda e: self.add())
        self.root.bind("<Control-s>", lambda e: self.save())
        self.rows = []; self.refresh()
    def refresh(self):
        self.listbox.delete(0, "end")
        self.rows = self.store.view(self.show.get())
        for _, t in self.rows:
            self.listbox.insert("end", label(t))
        c = self.store.counts()
        self.status.config(text=f"{c['pending']} pending | {c['done']} done | {c['total']} total")
    def selected_index(self):
        sel = self.listbox.curselection()
        return self.rows[sel[0]][0] if sel else None
    def add(self):
        try:
            self.store.add(self.entry.get(), self.prio.get()); self.entry.delete(0, "end"); self.refresh()
        except ValueError as e:
            self.msg.showwarning("To-do", str(e))
    def toggle(self):
        i = self.selected_index()
        if i is not None: self.store.toggle(i); self.refresh()
    def delete(self):
        i = self.selected_index()
        if i is not None and self.msg.askyesno("Delete", "Delete this task?"):
            self.store.delete(i); self.refresh()
    def save(self):
        self.store.save(); self.status.config(text="Saved.")

if gui_available():
    TodoApp(TodoStore()).root.mainloop()
else:
    banner("todo_app")
    path = "todo_demo.json"
    if os.path.exists(path): os.remove(path)
    store = TodoStore(path)
    for text, prio in [("Prepare Python lab 9", "high"), ("Mark quizzes", "normal"),
                       ("Buy whiteboard markers", "low"), ("  ", "normal"), ("mark quizzes", "normal"),
                       ("Email the timetable", "urgent"), ("Book projector", "high")]:
        try:
            store.add(text, prio); print(f"add {text!r:<26} ok")
        except ValueError as e:
            print(f"add {text!r:<26} warning: {e}")
    store.toggle(1)                       # double-click on "Mark quizzes"
    print("\nList (pending first, high priority first):")
    for _, t in store.view():
        print("  " + label(t))
    print("\nFilter 'done':", [t["text"] for _, t in store.view("done")])
    print("Status bar:", store.counts())
    reopened = TodoStore(path)            # simulate closing and reopening the app
    print("After restart, tasks loaded from file:", len(reopened.tasks))
    reopened.delete(0); print("After deleting the first task:", reopened.counts())
    os.remove(path)
