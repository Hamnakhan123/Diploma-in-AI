"""
Session 9 · Example 2: a registration form using the common widgets
-------------------------------------------------------------------
Widgets: Label, Entry, Spinbox, Radiobutton, Checkbutton, ttk.Combobox, Listbox,
Scale, Text, Button, LabelFrame, messagebox - with Tk variable classes
(StringVar, IntVar, BooleanVar) linking widgets to Python values.
Run:  python session-09_widget_gallery.py
"""
import re
from gui_support import gui_available, banner

PROGRAMS = ["Diploma in AI", "Data Science", "Web Development"]
SKILLS = ["Python", "SQL", "Statistics", "HTML/CSS", "Git"]

def validate(form):
    """Pure function: return a list of error messages for a form dict."""
    errors = []
    if len(form["name"].strip()) < 3:
        errors.append("Name needs at least 3 characters")
    if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", form["email"]):
        errors.append("Email is not valid")
    if not 16 <= form["age"] <= 60:
        errors.append("Age must be 16-60")
    if form["program"] not in PROGRAMS:
        errors.append("Choose a program")
    if not form["agree"]:
        errors.append("You must accept the rules")
    return errors

def summary(form):
    skills = ", ".join(form["skills"]) or "none yet"
    return (f"{form['name'].strip().title()} ({form['age']}, {form['gender']}) -> {form['program']}, "
            f"{form['shift']} shift | skills: {skills} | confidence {form['confidence']}/10")

def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("Student registration")
    name, email = tk.StringVar(), tk.StringVar()
    age, gender, shift = tk.IntVar(value=20), tk.StringVar(value="female"), tk.StringVar(value="Morning")
    agree, confidence, program = tk.BooleanVar(), tk.IntVar(value=5), tk.StringVar()

    tk.Label(root, text="Name").grid(row=0, column=0, sticky="w", padx=6, pady=3)
    tk.Entry(root, textvariable=name, width=30).grid(row=0, column=1, columnspan=2, sticky="we")
    tk.Label(root, text="Email").grid(row=1, column=0, sticky="w", padx=6)
    tk.Entry(root, textvariable=email, width=30).grid(row=1, column=1, columnspan=2, sticky="we")
    tk.Label(root, text="Age").grid(row=2, column=0, sticky="w", padx=6)
    tk.Spinbox(root, from_=16, to=60, textvariable=age, width=5).grid(row=2, column=1, sticky="w")
    box = tk.LabelFrame(root, text="Gender"); box.grid(row=3, column=0, columnspan=3, sticky="we", padx=6)
    for g in ("female", "male", "prefer not to say"):
        tk.Radiobutton(box, text=g, value=g, variable=gender).pack(side="left")
    tk.Label(root, text="Program").grid(row=4, column=0, sticky="w", padx=6)
    ttk.Combobox(root, values=PROGRAMS, textvariable=program, state="readonly").grid(row=4, column=1, sticky="w")
    tk.Label(root, text="Shift").grid(row=5, column=0, sticky="w", padx=6)
    tk.OptionMenu(root, shift, "Morning", "Evening", "Weekend").grid(row=5, column=1, sticky="w")
    tk.Label(root, text="Skills").grid(row=6, column=0, sticky="nw", padx=6)
    skills = tk.Listbox(root, selectmode="multiple", height=5, exportselection=False)
    for s in SKILLS: skills.insert("end", s)
    skills.grid(row=6, column=1, sticky="w")
    tk.Scale(root, from_=0, to=10, orient="horizontal", label="Confidence", variable=confidence).grid(row=7, column=1, sticky="we")
    notes = tk.Text(root, height=3, width=30); notes.grid(row=8, column=1, columnspan=2, pady=3)
    tk.Checkbutton(root, text="I accept the lab rules", variable=agree).grid(row=9, column=1, sticky="w")

    def submit():
        form = {"name": name.get(), "email": email.get(), "age": age.get(), "gender": gender.get(),
                "program": program.get(), "shift": shift.get(), "agree": agree.get(),
                "skills": [skills.get(i) for i in skills.curselection()], "confidence": confidence.get(),
                "notes": notes.get("1.0", "end").strip()}
        errors = validate(form)
        if errors:
            messagebox.showerror("Please fix", "\n".join(errors))
        else:
            messagebox.showinfo("Registered", summary(form))
    tk.Button(root, text="Submit", bg="#FF6B1A", fg="white", command=submit).grid(row=10, column=1, pady=8)
    root.mainloop()

if gui_available():
    run_gui()
else:
    banner("widget_gallery")
    samples = [
        {"name": "  ayesha khan ", "email": "ayesha@example.com", "age": 21, "gender": "female",
         "program": "Diploma in AI", "shift": "Evening", "agree": True, "skills": ["Python", "SQL"], "confidence": 7},
        {"name": "Al", "email": "al@", "age": 14, "gender": "male", "program": "",
         "shift": "Morning", "agree": False, "skills": [], "confidence": 3},
    ]
    for form in samples:
        errors = validate(form)
        print("Submit pressed with:", {k: form[k] for k in ("name", "email", "age", "program")})
        print("  -> showerror:" if errors else "  -> showinfo:", "; ".join(errors) if errors else summary(form))
    print("\nWidget -> Tk variable used to read it")
    for w, v in [("Entry", "StringVar"), ("Spinbox", "IntVar"), ("Radiobutton", "StringVar (shared)"),
                 ("Checkbutton", "BooleanVar"), ("Combobox/OptionMenu", "StringVar"), ("Scale", "IntVar"),
                 ("Listbox", "curselection()"), ("Text", "get('1.0', 'end')")]:
        print(f"  {w:<20} {v}")
