"""
Session 7 · Example 3: a JSON REST API with full CRUD
-----------------------------------------------------
REST maps HTTP methods to actions on a resource:
  GET /api/books        list       POST   /api/books       create
  GET /api/books/<id>   read one   PUT    /api/books/<id>  update
                                   DELETE /api/books/<id>  delete
Run:  python session-07_json_api.py      (add --serve to run a real server)
"""
import sys
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
books = {1: {"id": 1, "title": "Python Crash Course", "year": 2019, "available": True},
         2: {"id": 2, "title": "Hands-On Machine Learning", "year": 2022, "available": False}}
next_id = 3

def validate(data, partial=False):
    """Return a list of problems with the submitted JSON."""
    problems = []
    if not partial or "title" in data:
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            problems.append("title is required")
    if "year" in data and not (isinstance(data["year"], int) and 1450 <= data["year"] <= 2100):
        problems.append("year must be an integer between 1450 and 2100")
    return problems

@app.get("/api/books")                       # shortcut for @app.route(..., methods=["GET"])
def list_books():
    only_available = request.args.get("available") == "true"
    items = [b for b in books.values() if b["available"] or not only_available]
    return jsonify(count=len(items), books=items)

@app.get("/api/books/<int:book_id>")
def get_book(book_id):
    if book_id not in books:
        abort(404, description=f"book {book_id} not found")
    return jsonify(books[book_id])

@app.post("/api/books")
def create_book():
    global next_id
    data = request.get_json(silent=True) or {}
    problems = validate(data)
    if problems:
        return jsonify(errors=problems), 400                 # 400 Bad Request
    book = {"id": next_id, "title": data["title"].strip(), "year": data.get("year"),
            "available": data.get("available", True)}
    books[next_id] = book
    next_id += 1
    return jsonify(book), 201, {"Location": f"/api/books/{book['id']}"}   # 201 Created

@app.put("/api/books/<int:book_id>")
def update_book(book_id):
    if book_id not in books:
        abort(404, description=f"book {book_id} not found")
    data = request.get_json(silent=True) or {}
    problems = validate(data, partial=True)
    if problems:
        return jsonify(errors=problems), 400
    books[book_id].update({k: v for k, v in data.items() if k in ("title", "year", "available")})
    return jsonify(books[book_id])

@app.delete("/api/books/<int:book_id>")
def delete_book(book_id):
    if books.pop(book_id, None) is None:
        abort(404, description=f"book {book_id} not found")
    return "", 204                                           # 204 No Content

@app.errorhandler(404)
def handle_404(e):
    return jsonify(error=e.description), 404                 # JSON errors for an API

if __name__ == "__main__" and "--serve" in sys.argv:
    app.run(debug=True)
else:
    c = app.test_client()
    def call(method, url, json=None):
        r = c.open(url, method=method, json=json)
        body = r.get_json(silent=True)
        print(f"{method:6} {url:<28} {r.status_code}  {body if body is not None else '(empty)'}")
    call("GET", "/api/books")
    call("GET", "/api/books?available=true")
    call("POST", "/api/books", {"title": "Fluent Python", "year": 2022})
    call("POST", "/api/books", {"title": "  ", "year": 3000})
    call("PUT", "/api/books/2", {"available": True})
    call("DELETE", "/api/books/1")
    call("GET", "/api/books/1")
    call("GET", "/api/books")
