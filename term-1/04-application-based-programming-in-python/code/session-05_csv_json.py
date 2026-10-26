"""
Session 5 · Example 2: structured files - CSV and JSON
------------------------------------------------------
Run:  python session-05_csv_json.py
"""
import csv
import json
import os
import shutil
import tempfile

start, work = os.getcwd(), tempfile.mkdtemp()
os.chdir(work)                      # demo files go to a temporary folder

students = [
    {"roll": "AI-01", "name": "Ali Khan", "city": "Karachi", "marks": 78},
    {"roll": "AI-02", "name": "Sana Tariq", "city": "Lahore", "marks": 91},
    {"roll": "AI-03", "name": "Bilal, Jr.", "city": "Karachi", "marks": 64},   # comma inside a value!
]

# --- CSV: write with DictWriter (handles quoting of commas for you) ---
with open("students.csv", "w", newline="", encoding="utf-8") as f:   # newline="" avoids blank lines on Windows
    writer = csv.DictWriter(f, fieldnames=["roll", "name", "city", "marks"])
    writer.writeheader()
    writer.writerows(students)
print("raw CSV text:\n" + open("students.csv", encoding="utf-8").read())

# --- CSV: read rows as dicts. Every value comes back as TEXT ---
with open("students.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print("first row:", rows[0])
print("type of marks:", type(rows[0]["marks"]).__name__, "-> convert before maths")
avg = sum(int(r["marks"]) for r in rows) / len(rows)
print(f"average marks: {avg:.2f}")

# csv.reader gives plain lists
with open("students.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    karachi = [row[1] for row in reader if row[2] == "Karachi"]
print("header:", header, "| Karachi students:", karachi)

# --- JSON: nested data (dicts, lists, numbers, strings, bools, null) ---
config = {
    "course": "Diploma in AI",
    "term": 1,
    "modules": ["T-SQL", "MongoDB", "Statistics", "Python"],
    "lab": {"room": "B-204", "pcs": 30, "projector": True},
    "coordinator": None,
}
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)              # pretty-printed file

with open("config.json", encoding="utf-8") as f:
    loaded = json.load(f)
print("\nJSON round trip equal?", loaded == config)
print("lab room:", loaded["lab"]["room"], "| modules:", len(loaded["modules"]))

# dumps / loads work with strings (used for web APIs in Sessions 7-8)
text = json.dumps({"ok": True, "items": [1, 2]})
print("dumps ->", text, "| loads ->", json.loads(text))
print("Python None/True become JSON:", json.dumps([None, True, False]))
try:
    json.loads("{'single': 'quotes'}")            # not valid JSON
except json.JSONDecodeError as e:
    print("JSONDecodeError:", e.msg)

os.chdir(start); shutil.rmtree(work)   # tidy up
