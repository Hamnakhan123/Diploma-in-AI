"""
Session 7 · Mini project: campus notice board (HTML pages + JSON API + tests)
-----------------------------------------------------------------------------
Features
  - an application factory create_app() (the pattern used by real Flask projects)
  - HTML home page listing notices, newest first, filterable by category
  - JSON API: GET /api/notices, POST /api/notices (needs an API token),
    DELETE /api/notices/<id> (needs the token)
  - notices saved to a JSON file so they survive restarts (Session 5)
  - a set of automated checks using the test client, like a mini test suite
Run:  python session-07_project_notice_board.py     (add --serve to browse it)
"""
import json
import os
import sys
import tempfile
from datetime import date
from flask import Flask, abort, jsonify, render_template_string, request

PAGE = """<!doctype html><title>Notice board</title>
<h1>Campus notice board</h1>
<p>Filter: <a href="/">all</a>{% for c in categories %} | <a href="/?category={{ c }}">{{ c }}</a>{% endfor %}</p>
{% for n in notices %}
<article><h3>[{{ n.category }}] {{ n.title }}</h3><small>{{ n.date }}</small><p>{{ n.body }}</p></article>
{% else %}<p>No notices.</p>{% endfor %}"""
CATEGORIES = ["exam", "event", "holiday", "general"]

def create_app(data_file, api_token):
    """Build and configure a Flask app. Tests can create as many as they like."""
    app = Flask(__name__)
    app.config.update(DATA_FILE=data_file, API_TOKEN=api_token)

    def load():
        try:
            with open(app.config["DATA_FILE"], encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(notices):
        with open(app.config["DATA_FILE"], "w", encoding="utf-8") as f:
            json.dump(notices, f, indent=2)

    def require_token():
        sent = request.headers.get("Authorization", "")
        if sent != f"Bearer {app.config['API_TOKEN']}":
            abort(401)

    def visible(category=None):
        items = sorted(load(), key=lambda n: (n["date"], n["id"]), reverse=True)
        return [n for n in items if category in (None, n["category"])]

    @app.get("/")
    def home():
        cat = request.args.get("category")
        return render_template_string(PAGE, notices=visible(cat), categories=CATEGORIES)

    @app.get("/api/notices")
    def list_notices():
        return jsonify(visible(request.args.get("category")))

    @app.post("/api/notices")
    def add_notice():
        require_token()
        data = request.get_json(silent=True) or {}
        errors = [f"{f} is required" for f in ("title", "body") if not str(data.get(f, "")).strip()]
        if data.get("category", "general") not in CATEGORIES:
            errors.append(f"category must be one of {CATEGORIES}")
        if errors:
            return jsonify(errors=errors), 400
        notices = load()
        notice = {"id": max((n["id"] for n in notices), default=0) + 1,
                  "title": data["title"].strip(), "body": data["body"].strip(),
                  "category": data.get("category", "general"),
                  "date": data.get("date", date.today().isoformat())}
        notices.append(notice)
        save(notices)
        return jsonify(notice), 201

    @app.delete("/api/notices/<int:nid>")
    def delete_notice(nid):
        require_token()
        notices = load()
        remaining = [n for n in notices if n["id"] != nid]
        if len(remaining) == len(notices):
            abort(404)
        save(remaining)
        return "", 204

    @app.errorhandler(401)
    def unauthorised(e):
        return jsonify(error="missing or wrong API token"), 401

    @app.errorhandler(404)
    def missing(e):
        return jsonify(error="not found"), 404

    return app

# ---------------------------------------------------------------------------
if __name__ == "__main__" and "--serve" in sys.argv:
    create_app("notices.json", os.environ.get("NOTICE_TOKEN", "change-me")).run(debug=True)
else:
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
    os.remove(tmp)                                   # start with no file at all
    app = create_app(tmp, api_token="s3cret")
    client = app.test_client()
    auth = {"Authorization": "Bearer s3cret"}
    passed = failed = 0

    def check(label, condition):
        """A tiny assertion helper that reports instead of stopping."""
        global passed, failed
        passed, failed = passed + bool(condition), failed + (not condition)
        print(f"  [{'PASS' if condition else 'FAIL'}] {label}")

    print("Automated checks")
    check("empty board shows 'No notices'", "No notices" in client.get("/").get_data(as_text=True))
    r = client.post("/api/notices", json={"title": "Mid-term exams", "body": "Start 10 Nov"})
    check("POST without token is rejected with 401", r.status_code == 401)
    seed = [
        {"title": "Mid-term exams", "body": "Start 10 Nov in Hall A.", "category": "exam", "date": "2026-10-20"},
        {"title": "AI hackathon", "body": "Teams of 3, register by Friday.", "category": "event", "date": "2026-10-22"},
        {"title": "Iqbal Day", "body": "Campus closed on 9 November.", "category": "holiday", "date": "2026-10-25"},
    ]
    for n in seed:
        r = client.post("/api/notices", json=n, headers=auth)
    check("POST with token returns 201 and an id", r.status_code == 201 and r.get_json()["id"] == 3)
    r = client.post("/api/notices", json={"title": "", "category": "party"}, headers=auth)
    check("invalid notice returns 400 with 3 errors", r.status_code == 400 and len(r.get_json()["errors"]) == 3)
    items = client.get("/api/notices").get_json()
    check("list is newest first", [n["title"] for n in items] == ["Iqbal Day", "AI hackathon", "Mid-term exams"])
    check("category filter works", [n["title"] for n in client.get("/api/notices?category=exam").get_json()] == ["Mid-term exams"])
    check("HTML page shows the hackathon", "AI hackathon" in client.get("/").get_data(as_text=True))
    check("data survives a 'restart' (new app, same file)",
          len(create_app(tmp, "s3cret").test_client().get("/api/notices").get_json()) == 3)
    check("DELETE removes a notice (204)", client.delete("/api/notices/2", headers=auth).status_code == 204)
    check("DELETE of a missing id gives 404", client.delete("/api/notices/99", headers=auth).status_code == 404)
    print(f"\n{passed} passed, {failed} failed")
    print("final board:", [(n["id"], n["category"], n["title"]) for n in client.get("/api/notices").get_json()])
    os.remove(tmp)
