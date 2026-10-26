"""
Session 6 · Real-life problem: validating and extracting admission-form data
----------------------------------------------------------------------------
PROBLEM
An admissions office receives (a) structured form fields that must be
VALIDATED, and (b) free-text emails from which details must be EXTRACTED.
Rules (formats used in Pakistan):
  CNIC    : 5 digits - 7 digits - 1 digit        e.g. 42101-1234567-1
  Mobile  : 03XX-XXXXXXX or 03XXXXXXXXX or +923XXXXXXXXX
  Email   : name@domain.tld
  Roll no : AI-YYYY-NNNN with year 2020-2029
  DOB     : DD/MM/YYYY
Write one compiled pattern per rule, validate a batch of applicants, normalise
phone numbers to +92 format, and extract every phone/email/CNIC from emails.
Run:  python session-06_problem_form_validator.py
"""
import re

RULES = {
    "cnic":   re.compile(r"\d{5}-\d{7}-\d"),
    "mobile": re.compile(r"(?:\+92|0)3\d{2}-?\d{7}"),
    "email":  re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}"),
    "roll":   re.compile(r"AI-202\d-\d{4}"),
    "dob":    re.compile(r"(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}"),
}

def validate(applicant):
    """Return a list of field names that FAIL their rule (fullmatch = whole value)."""
    return [field for field, rx in RULES.items() if not rx.fullmatch(applicant.get(field, "").strip())]

def normalise_mobile(raw):
    """0300-1234567 / 03001234567 / +923001234567  ->  +923001234567"""
    if not RULES["mobile"].fullmatch(raw.strip()):
        return None                                   # never 'fix' an invalid number
    digits = re.sub(r"\D", "", raw)                  # keep digits only
    return "+92" + digits[-10:]

applicants = [
    {"name": "Ayesha Siddiqui", "cnic": "42101-1234567-2", "mobile": "0321-7654321",
     "email": "ayesha.s@example.com", "roll": "AI-2026-0001", "dob": "14/12/2004"},
    {"name": "Omar Farooq", "cnic": "4210112345672", "mobile": "+923001112233",
     "email": "omar@mail", "roll": "AI-2026-0002", "dob": "31/02/2005"},
    {"name": "Mehwish Ali", "cnic": "35202-7654321-8", "mobile": "021-34567890",
     "email": "mehwish_ali@uni.edu.pk", "roll": "AI-2019-0003", "dob": "05/13/2003"},
    {"name": "Danish Raza", "cnic": "61101-2223334-5", "mobile": "03451234567",
     "email": "danish.raza+admission@example.org", "roll": "AI-2026-0004", "dob": "01/01/2006"},
]
print("Validation")
for a in applicants:
    bad = validate(a)
    status = "OK" if not bad else "fix: " + ", ".join(bad)
    print(f"  {a['name']:<16} {status:<26} phone -> {normalise_mobile(a['mobile'])}")
print("  note: 31/02/2005 passes the PATTERN; regex checks format, not calendar logic.")
print("        use datetime.strptime for real date validation (Session 5).")

emails = """
From: parent.khan@example.com
Assalam-o-Alaikum, my son's CNIC is 42201-9876543-1 and you can call me on
0333-4445566 or my wife on +923214445566. His friend (CNIC 42101-1112223-3)
also applied; reach him at friend_99@uni.edu.pk. Wrong number 12345-678 ignore.
"""
print("\nExtraction from free text")
for field in ("cnic", "mobile", "email"):
    print(f"  {field:<7}", RULES[field].findall(emails))

masked = RULES["cnic"].sub(lambda m: m.group()[:5] + "-*******-" + m.group()[-1], emails)
print("\nPrivacy-masked text:")
print(masked.strip())
