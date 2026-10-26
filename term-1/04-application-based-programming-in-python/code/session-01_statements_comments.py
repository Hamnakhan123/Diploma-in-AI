"""
Session 1 · Example 2: statements, comments and indentation
------------------------------------------------------------
Run:  python session-01_statements_comments.py
"""
# A comment starts with # and runs to the end of the line. Python ignores it.

# --- Simple statements: one per line (a ; joins two, but avoid it) ---
city = "Karachi"
population_m = 20.4          # inline comment: millions, rough figure for the demo
a = 1; b = 2                 # legal, but harder to read

# --- A long statement split over lines ---
# Implicit continuation inside (), [] or {} is the preferred style
fee_breakdown = [
    "tuition",
    "lab",
    "library",
]
total_fee = (45_000      # underscores make big numbers readable
             + 5_000
             + 1_500)
# Explicit continuation with a backslash also works, but breaks easily
message = "Fees for " + city + \
          " campus"

# --- Compound statements: a header ending in ':' and an indented block ---
def describe(fee):
    """Docstring: the first string in a function documents it."""
    if fee > 50_000:
        level = "high"           # 4 spaces = one level
    else:
        level = "normal"
    return level

print(message, "->", total_fee, describe(total_fee))
print("Items:", fee_breakdown, "| a + b =", a + b)
print("Docstring of describe():", describe.__doc__)

# --- Indentation errors are caught before the program runs ---
bad_code = "if True:\nprint('no indent')"
try:
    compile(bad_code, "<demo>", "exec")
except IndentationError as e:
    print("IndentationError:", e.msg, "on line", e.lineno)

mixed = "if True:\n    x = 1\n  y = 2"      # inconsistent dedent
try:
    compile(mixed, "<demo>", "exec")
except IndentationError as e:
    print("IndentationError:", e.msg, "on line", e.lineno)
