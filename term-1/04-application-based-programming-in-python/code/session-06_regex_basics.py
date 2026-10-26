"""
Session 6 · Example 1: the building blocks of regular expressions
-----------------------------------------------------------------
Each line shows a pattern, a test string and every match re.findall finds.
Run:  python session-06_regex_basics.py
"""
import re

def show(pattern, text, note=""):
    found = re.findall(pattern, text)
    print(f"  {pattern:<22} on {text!r:<38} -> {found}  {note}")

print("Literal characters and the dot")
show(r"cat", "cat, concat, Cat")
show(r"c.t", "cat cot c9t ct", ". = any char except newline")

print("Character classes [...]")
show(r"[aeiou]", "Karachi", "any one vowel")
show(r"[A-Z]", "Diploma in AI", "any capital")
show(r"[^0-9 ]", "Room 204 B", "^ inside [] = NOT")
show(r"[0-9a-fA-F]+", "colour #FF6B1A and #fcd34d", "hex digits")

print("Special sequences")
show(r"\d+", "Order 66 costs Rs 1450", "\\d digit")
show(r"\w+", "hello_world, 2026!", "\\w letter/digit/_")
show(r"\s", "a b\tc", "\\s whitespace")
show(r"\bin\b", "in inside within in", "\\b word boundary")
show(r"\D+", "03001234567 ext", "\\D NON-digit")

print("Quantifiers")
show(r"colou?r", "color colour colouur", "? = 0 or 1")
show(r"go*gle", "ggle gogle google", "* = 0 or more")
show(r"go+gle", "ggle gogle google", "+ = 1 or more")
show(r"\d{4}", "PIN 1234, year 2026, 99", "{n} exactly n")
show(r"\d{2,3}", "7 42 314 2718", "{m,n} between m and n")

print("Anchors")
show(r"^Hello", "Hello world. Hello again")
show(r"again$", "Hello world. Hello again")

print("Alternation and groups")
show(r"cat|dog", "cat dog cow")
show(r"(\d+)-(\d+)", "pages 10-15 and 20-24", "groups -> tuples")
show(r"(?:Mr|Ms|Dr)\.? \w+", "Dr. Ali met Ms Sana and Mr Khan", "(?:) non-capturing")

print("Greedy vs lazy")
html = "<b>bold</b> and <i>italic</i>"
show(r"<.+>", html, "greedy grabs as much as possible")
show(r"<.+?>", html, "lazy +? stops early")

print("Escaping metacharacters . ^ $ * + ? { } [ ] \\ | ( )")
show(r"\$\d+\.\d{2}", "price $19.99 or $5.50")
print("  re.escape('1+1=2?') ->", re.escape("1+1=2?"))
print("Raw strings: len('\\n') =", len("\n"), "but len(r'\\n') =", len(r"\n"))
