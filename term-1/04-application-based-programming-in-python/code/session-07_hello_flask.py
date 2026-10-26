"""
Session 7 · Example 1: a first Flask application - routes and URLs
------------------------------------------------------------------
Flask maps URLs to Python functions ("view functions").
This script tests the app with Flask's built-in test client, so it runs
anywhere (terminal, notebook, Colab) without opening a browser.
To serve it for real:  python session-07_hello_flask.py --serve
then open http://127.0.0.1:5000/ in a browser.
"""
import sys
from flask import Flask, request, url_for, redirect, abort

app = Flask(__name__)          # __name__ tells Flask where to find templates/static files

@app.route("/")                # the home page
def home():
    return "<h1>Welcome to the Diploma in AI portal</h1>"

@app.route("/about")
def about():
    return "This site is built with Flask, a Python micro web framework."

# Dynamic segments: <name> is passed to the function as an argument
@app.route("/hello/<name>")
def hello(name):
    return f"Assalam-o-Alaikum, {name.title()}!"

# Converters check and convert the type: int, float, path, uuid
@app.route("/square/<int:n>")
def square(n):
    return {"n": n, "square": n * n}      # returning a dict sends JSON automatically

# Query strings: /search?q=python&page=2
@app.route("/search")
def search():
    q = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    return f"Searching for '{q}' (page {page})"

# Allowing more HTTP methods than the default GET
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return f"Thanks {request.form.get('name', 'friend')}, message received.", 201
    return "Contact form goes here"

@app.route("/old-courses")
def old_courses():
    return redirect(url_for("hello", name="visitor"))   # build URLs from function names

@app.route("/admin")
def admin():
    abort(403)                               # stop with an HTTP error status

@app.errorhandler(404)
def not_found(error):
    return "Sorry, that page does not exist.", 404

if __name__ == "__main__" and "--serve" in sys.argv:
    app.run(debug=True)                      # development server only
else:
    client = app.test_client()               # a fake browser for testing
    for method, url, data in [("GET", "/", None), ("GET", "/about", None),
                              ("GET", "/hello/ayesha", None), ("GET", "/square/12", None),
                              ("GET", "/square/abc", None), ("GET", "/search?q=flask&page=2", None),
                              ("POST", "/contact", {"name": "Bilal"}), ("GET", "/old-courses", None),
                              ("GET", "/admin", None), ("GET", "/nowhere", None)]:
        resp = client.open(url, method=method, data=data)
        body = resp.get_data(as_text=True).strip().replace("\n", " ")
        extra = f" -> Location: {resp.headers['Location']}" if resp.status_code in (301, 302) else ""
        print(f"{method:4} {url:<24} {resp.status_code}  {body[:60]}{extra}")
    with app.test_request_context():
        print("\nurl_for examples:", url_for("home"), url_for("hello", name="sana"),
              url_for("search", q="ai", page=3))
    print("registered routes:", sorted(r.rule for r in app.url_map.iter_rules() if r.endpoint != "static"))
