"""
Session 2 · Example 1: Python's built-in data types and conversions
-------------------------------------------------------------------
Run:  python session-02_data_types.py
"""
samples = {
    "int": 42,
    "float": 3.75,
    "complex": 2 + 3j,
    "bool": True,
    "str": "Karachi",
    "list": [85, 90, 78],
    "tuple": (24.86, 67.01),          # latitude, longitude
    "set": {"python", "sql", "python"},
    "dict": {"name": "Ali", "cgpa": 3.4},
    "NoneType": None,
}
print(f"{'type':9} {'value':28} {'mutable?':9} {'ordered?':9}")
mutable = {"list", "set", "dict"}
ordered = {"str", "list", "tuple", "dict"}
for name, value in samples.items():
    shown = "{" + ", ".join(map(repr, sorted(value))) + "}" if isinstance(value, set) else str(value)  # sets have no order: sort for a stable display
    print(f"{type(value).__name__:9} {shown:28} {str(name in mutable):9} {str(name in ordered):9}")

# Numbers
print("\n7 / 2 =", 7 / 2, "| 7 // 2 =", 7 // 2, "| 2 ** 100 has", len(str(2 ** 100)), "digits")
print("0.1 + 0.2 =", 0.1 + 0.2, "-> use round() or decimal for money:", round(0.1 + 0.2, 2))
print("complex parts:", samples["complex"].real, samples["complex"].imag)

# bool is a subclass of int; 'truthiness' of values
print("True + True =", True + True)
for v in [0, 1, "", "0", [], [0], None, 0.0]:
    print(f"  bool({v!r:5}) = {bool(v)}")

# Strings are sequences
s = "Diploma in AI"
print("\nindex/slice:", s[0], s[-2:], s[:7], "| upper:", s.upper(), "| words:", s.split())

# Explicit conversion (casting)
print("\nint('42') + 1 =", int("42") + 1)
print("float('3.5') * 2 =", float("3.5") * 2)
print("int(9.99) =", int(9.99), "(truncates, does not round)")
print("str(2026) + '!' =", str(2026) + "!")
print("list('abc') =", list("abc"), "| tuple([1, 2]) =", tuple([1, 2]), "| set([1, 1, 2]) =", set([1, 1, 2]))
print("dict([('a', 1), ('b', 2)]) =", dict([("a", 1), ("b", 2)]))
try:
    int("12.5")
except ValueError as e:
    print("int('12.5') fails:", e)
