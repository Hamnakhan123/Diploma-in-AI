"""
Session 7 · Example 2: Jinja2 templates, template inheritance and HTML forms
----------------------------------------------------------------------------
Real projects keep templates as files in a templates/ folder. To keep this
example in ONE file, the templates are stored in a dictionary and loaded with
Jinja's DictLoader - the template syntax is exactly the same.
Run:  python session-07_templates_forms.py        (add --serve to open it in a browser)
"""
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from jinja2 import DictLoader

TEMPLATES = {
    "base.html": """<!doctype html>
<html><head><title>{% block title %}Portal{% endblock %}</title></head>
<body>
  <nav><a href="{{ url_for('courses') }}">Courses</a> | <a href="{{ url_for('enrol') }}">Enrol</a></nav>
  {% for msg in get_flashed_messages() %}<p class="flash">{{ msg }}</p>{% endfor %}
  {% block content %}{% endblock %}
</body></html>""",
    "courses.html": """{% extends "base.html" %}
{% block title %}Courses{% endblock %}
{% block content %}
<h1>{{ heading }}</h1>
<ul>
{% for c in courses %}
  <li>{{ loop.index }}. {{ c.title }} - {{ c.hours }} h{% if c.hours >= 36 %} <b>(long)</b>{% endif %}</li>
{% else %}
  <li>No courses yet</li>
{% endfor %}
</ul>
<p>Total: {{ courses | sum(attribute='hours') }} hours, {{ courses | length }} courses</p>
{% endblock %}""",
    "enrol.html": """{% extends "base.html" %}
{% block content %}
<h1>Enrol</h1>
{% if errors %}<ul>{% for e in errors %}
  <li class="error">{{ e }}</li>{% endfor %}
</ul>{% endif %}
<form method="post">
  <input name="name" value="{{ form.name or '' }}">
  <input name="email" value="{{ form.email or '' }}">
  <button>Submit</button>
</form>
{% endblock %}""",
}

app = Flask(__name__)
app.secret_key = "dev-only-change-me"        # needed for flash() messages (signed cookies)
app.jinja_loader = DictLoader(TEMPLATES)

COURSES = [{"title": "T-SQL", "hours": 16}, {"title": "MongoDB", "hours": 32},
           {"title": "Python Applications", "hours": 36}]
ENROLLED = []

@app.route("/")
def courses():
    return render_template("courses.html", heading="Term 1 courses", courses=COURSES)

@app.route("/enrol", methods=["GET", "POST"])
def enrol():
    errors, form = [], request.form
    if request.method == "POST":
        if len(form.get("name", "").strip()) < 3:
            errors.append("Name must have at least 3 characters")
        if "@" not in form.get("email", ""):
            errors.append("Enter a valid email")
        if not errors:
            ENROLLED.append({"name": form["name"].strip(), "email": form["email"]})
            flash(f"Welcome aboard, {form['name'].strip()}!")
            return redirect(url_for("courses"))   # Post/Redirect/Get pattern
    return render_template("enrol.html", errors=errors, form=form)

def text_only(html):
    """Strip tags and blank lines so the test output is easy to read."""
    import re
    return " | ".join(l.strip() for l in re.sub(r"<[^>]+>", "", html).splitlines() if l.strip())

if __name__ == "__main__" and "--serve" in sys.argv:
    app.run(debug=True)
else:
    c = app.test_client()
    print("GET / ->", text_only(c.get("/").get_data(as_text=True)))
    r = c.post("/enrol", data={"name": "Al", "email": "no-at-sign"})
    print("\nPOST bad form ->", r.status_code, text_only(r.get_data(as_text=True)))
    r = c.post("/enrol", data={"name": "Alishba", "email": "alishba@example.com"}, follow_redirects=True)
    print("\nPOST good form (redirect followed) ->", r.status_code, text_only(r.get_data(as_text=True))[:110])
    print("enrolled:", ENROLLED)
    # Jinja escapes HTML automatically, which blocks script injection (XSS)
    with app.test_request_context():
        from flask import render_template_string
        print("\nauto-escaping:", render_template_string("<p>{{ v }}</p>", v="<script>alert(1)</script>"))
