"""
Session 1 · Mini project: student profile card generator
--------------------------------------------------------
Builds a formatted ID-style card from raw form data. Practises variables,
type conversion, string methods, f-string alignment and simple validation.
Run:  python session-01_project_student_card.py
"""
import keyword

WIDTH = 44   # inner width of the card

# Raw form data exactly as a web form would send it: everything is text
form = {
    "full_name": "  hamza   ali RAZA ",
    "roll_no": "ai-2026-0147",
    "program": "diploma in ai",
    "semester": "1",
    "cgpa": "3.456",
    "email": "Hamza.Raza@Example.com ",
    "username": "hamza_raza",
}

def clean_name(raw):
    """Collapse extra spaces and use Title Case."""
    return " ".join(raw.split()).title()

def valid_username(u):
    """A username follows the identifier rules from this session."""
    return u.isidentifier() and not keyword.iskeyword(u) and u.islower()

def line(text=""):
    return "| " + text.ljust(WIDTH) + " |"

# --- convert and clean ---
name = clean_name(form["full_name"])
roll = form["roll_no"].upper()
program = form["program"].title().replace(" In ", " in ").replace("Ai", "AI")
semester = int(form["semester"])
cgpa = round(float(form["cgpa"]), 2)
email = form["email"].strip().lower()
user = form["username"]

# --- validate ---
problems = []
if not 0 <= cgpa <= 4:
    problems.append("CGPA must be between 0 and 4")
if "@" not in email or email.startswith("@"):
    problems.append("email looks wrong")
if not valid_username(user):
    problems.append("username must be a lowercase identifier")

# --- print the card ---
border = "+" + "-" * (WIDTH + 2) + "+"
print(border)
print(line("STUDENT PROFILE".center(WIDTH)))
print(border)
print(line(f"{'Name':<10}: {name}"))
print(line(f"{'Roll no':<10}: {roll}"))
print(line(f"{'Program':<10}: {program}"))
print(line(f"{'Semester':<10}: {semester}"))
print(line(f"{'CGPA':<10}: {cgpa:.2f}  {'*' * round(cgpa)}"))
print(line(f"{'Email':<10}: {email}"))
print(line(f"{'Username':<10}: @{user}"))
print(border)
print("Validation:", "all fields OK" if not problems else "; ".join(problems))
print("Types after conversion:", {k: type(v).__name__ for k, v in
      {"name": name, "semester": semester, "cgpa": cgpa}.items()})
