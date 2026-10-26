"""
Session 7 · Real-life problem: a student result portal
------------------------------------------------------
PROBLEM
Students keep emailing the office for their marks. Build a small Flask site that
  1. loads results.csv once at start-up,
  2. GET /                 -> a search form,
  3. GET /result?roll=...  -> an HTML result card (grades, percentage, pass/fail)
                              or a friendly 404 page for an unknown roll number,
  4. GET /api/result/<roll>-> the same data as JSON for a mobile app,
  5. GET /api/summary      -> class statistics (average per subject, top student),
  6. validates the roll-number format with a regex (Session 6) before looking it up.
Run:  python session-07_problem_result_portal.py      (add --serve for a real server)
"""
import csv
import re
import sys
from flask import Flask, jsonify, render_template_string, request, abort

ROLL_RE = re.compile(r"AI-202\d-\d{4}")
SUBJECTS = ["programming", "statistics", "databases", "communication"]

def load_results(path="results.csv"):
    """Read the CSV into {roll: record} with marks converted to int."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["roll"]: {**row, **{s: int(row[s]) for s in SUBJECTS}} for row in csv.DictReader(f)}

def grade(mark):
    for cut, g in [(85, "A"), (70, "B"), (55, "C"), (50, "D")]:
        if mark >= cut:
            return g
    return "F"

def card(rec):
    """Turn one raw record into the data shown to the student."""
    marks = {s: rec[s] for s in SUBJECTS}
    pct = sum(marks.values()) / len(marks)
    return {"roll": rec["roll"], "name": rec["name"],
            "subjects": {s: {"mark": m, "grade": grade(m)} for s, m in marks.items()},
            "percentage": round(pct, 1), "passed": all(m >= 50 for m in marks.values())}

PAGE = """<!doctype html><title>Results</title>
<h1>Result portal</h1>
<form action="/result"><input name="roll" placeholder="AI-2026-0001"><button>Check</button></form>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
{% if c %}
<h2>{{ c.name }} ({{ c.roll }})</h2>
<table>{% for s, v in c.subjects.items() %}
<tr><td>{{ s|title }}</td><td>{{ v.mark }}</td><td>{{ v.grade }}</td></tr>{% endfor %}
</table>
<p>Percentage: {{ c.percentage }}% - {{ "PASSED" if c.passed else "NOT PASSED: re-sit required" }}</p>
{% endif %}"""

app = Flask(__name__)
RESULTS = load_results()

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.get("/result")
def result():
    roll = request.args.get("roll", "").strip().upper()
    if not ROLL_RE.fullmatch(roll):
        return render_template_string(PAGE, error=f"'{roll}' is not a valid roll number (format AI-2026-0001)"), 400
    if roll not in RESULTS:
        return render_template_string(PAGE, error=f"No result found for {roll}"), 404
    return render_template_string(PAGE, c=card(RESULTS[roll]))

@app.get("/api/result/<roll>")
def api_result(roll):
    roll = roll.upper()
    if roll not in RESULTS:
        abort(404)
    return jsonify(card(RESULTS[roll]))

@app.get("/api/summary")
def api_summary():
    cards = [card(r) for r in RESULTS.values()]
    averages = {s: round(sum(r[s] for r in RESULTS.values()) / len(RESULTS), 1) for s in SUBJECTS}
    top = max(cards, key=lambda c: c["percentage"])
    return jsonify(students=len(cards), passed=sum(c["passed"] for c in cards),
                   subject_average=averages, top_student={"name": top["name"], "percentage": top["percentage"]})

@app.errorhandler(404)
def nf(e):
    return jsonify(error="not found"), 404

def strip(html):
    """Visible text of a page, minus the repeated header and search form."""
    import html as h
    text = " | ".join(" ".join(l.split()) for l in re.sub(r"<[^>]+>", " ", html).splitlines() if l.strip())
    return h.unescape(text.split("Check", 1)[-1].lstrip(" |"))

if __name__ == "__main__" and "--serve" in sys.argv:
    app.run(debug=True)
else:
    c = app.test_client()
    for url in ["/result?roll=ai-2026-0001", "/result?roll=AI-2026-0003", "/result?roll=AI-2026-0099",
                "/result?roll=12345"]:
        r = c.get(url)
        print(f"GET {url:<28} {r.status_code}\n   {strip(r.get_data(as_text=True))}\n")
    print("GET /api/result/AI-2026-0004 ->", c.get("/api/result/AI-2026-0004").get_json())
    print("GET /api/result/XX           ->", c.get("/api/result/XX").status_code)
    print("GET /api/summary ->", c.get("/api/summary").get_json())
