"""
Session 6 · Example 2: the methods of the re module
---------------------------------------------------
Run:  python session-06_re_methods.py
"""
import re

text = "Invoice INV-2026-0042 issued 2026-10-05 to ali.khan@example.com for Rs 12,500. " \
       "Reminder sent 2026-10-20 to accounts@uni.edu.pk."

# match: only at the START of the string
print("match('Invoice'):", re.match(r"Invoice", text))
print("match('INV'):", re.match(r"INV", text))

# search: first match ANYWHERE; returns a Match object (or None)
m = re.search(r"INV-(\d{4})-(\d{4})", text)
print("search ->", m.group(), "| year:", m.group(1), "| number:", m.group(2), "| span:", m.span())

# Named groups make code self-documenting
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
print("named groups:", m.groupdict())

# findall: list of all matches (strings, or tuples when there are groups)
print("findall dates:", re.findall(r"\d{4}-\d{2}-\d{2}", text))
print("findall emails:", re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text))

# finditer: Match objects one by one, with positions
for mm in re.finditer(r"\d{4}-\d{2}-\d{2}", text):
    print(f"  date {mm.group()} at characters {mm.start()}-{mm.end()}")

# sub: replace; the replacement can use groups or be a function
masked = re.sub(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)", r"***@\1", text)
print("sub mask emails:", re.findall(r"\*\*\*@[\w.-]*\w", masked))
print("sub reorder dates:", re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", "due 2026-10-05"))
def to_dollars(mo):
    rupees = int(mo.group(1).replace(",", ""))
    return f"${rupees / 280:.2f}"                   # illustrative exchange rate
print("sub with a function:", re.sub(r"Rs ([\d,]+)", to_dollars, "Fee Rs 12,500 and Rs 700"))
print("subn counts replacements:", re.subn(r"\s+", " ", "too    many   spaces"))

# split on a pattern (several delimiters at once)
print("split:", re.split(r"[;,|]\s*", "python, sql;git | flask"))
print("split keeping delimiters:", re.split(r"([.!?])", "Hi! How are you? Fine."))

# compile once, reuse many times (faster and cleaner in loops)
phone = re.compile(r"^03\d{2}-?\d{7}$")
for p in ["0300-1234567", "03001234567", "021-1234567", "0300-123456"]:
    print(f"  {p:<14} valid mobile? {bool(phone.match(p))}")

# fullmatch: the WHOLE string must match (great for validation)
print("fullmatch roll:", bool(re.fullmatch(r"AI-\d{4}-\d{4}", "AI-2026-0147")),
      bool(re.fullmatch(r"AI-\d{4}-\d{4}", "AI-2026-0147x")))

# Flags
print("IGNORECASE:", re.findall(r"python", "Python PYTHON python", flags=re.I))
print("MULTILINE ^:", re.findall(r"^\w+", "first line\nsecond line", flags=re.M))
verbose = re.compile(r"""
    (?P<user>[\w.]+)      # user name
    @
    (?P<domain>[\w.]+)    # domain
""", re.VERBOSE)
print("VERBOSE:", verbose.search("write to hamna.k@example.org").groupdict())

# Lookahead: password must contain a digit and a capital, 8+ chars
strong = re.compile(r"^(?=.*\d)(?=.*[A-Z]).{8,}$")
for pw in ["karachi2026", "Karachi2026", "Ka1"]:
    print(f"  {pw:<12} strong? {bool(strong.match(pw))}")
