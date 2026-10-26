"""
Session 1 · Example 1: keywords and identifiers
-----------------------------------------------
Shows the reserved words of the running Python version and tests a list of
candidate variable names against Python's naming rules.
Run:  python session-01_keywords_identifiers.py
"""
import keyword

# 1. Keywords: words with a fixed meaning that you can never use as names
print("Python has", len(keyword.kwlist), "keywords:")
for i in range(0, len(keyword.kwlist), 9):          # print 9 per line
    print("  ", ", ".join(keyword.kwlist[i:i + 9]))

# Soft keywords (match, case, type, _) are reserved only in certain places
print("Soft keywords:", keyword.softkwlist)

# 2. Identifier rules: start with a letter or _, then letters, digits or _,
#    no spaces or symbols, not a keyword. Python is case-sensitive.
def check_name(name):
    """Return (is_valid, reason) for a proposed variable name."""
    if keyword.iskeyword(name):
        return False, "is a keyword"
    if not name.isidentifier():
        if name[:1].isdigit():
            return False, "starts with a digit"
        return False, "contains a space or symbol"
    if name.startswith("__") and name.endswith("__"):
        return True, "valid, but dunder names are reserved for Python itself"
    return True, "valid"

candidates = ["student_name", "Marks2025", "_total", "2nd_place", "first name",
              "class", "price$", "StudentName", "__init__", "cgpa"]
print("\nName check")
for c in candidates:
    ok, why = check_name(c)
    print(f"  {c!r:16} {'OK ' if ok else 'BAD'}  {why}")

# 3. Case sensitivity: three different variables
total, Total, TOTAL = 1, 2, 3
print("\ntotal, Total, TOTAL ->", total, Total, TOTAL)
