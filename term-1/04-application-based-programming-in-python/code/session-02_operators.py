"""
Session 2 · Example 2: every family of operators, plus precedence
-----------------------------------------------------------------
Run:  python session-02_operators.py
"""
a, b = 17, 5
print("Arithmetic")
for sym, val in [("+", a + b), ("-", a - b), ("*", a * b), ("/", a / b),
                 ("//", a // b), ("%", a % b), ("**", a ** b)]:
    print(f"  {a} {sym:2} {b} = {val}")
print("  negative floor division: -17 // 5 =", -17 // 5, "and -17 % 5 =", -17 % 5)

print("\nComparison (always give a bool)")
print("  17 > 5:", a > b, "| 17 == 17.0:", 17 == 17.0, "| 'apple' < 'banana':", "apple" < "banana")
print("  chained: 0 <= 72 <= 100 ->", 0 <= 72 <= 100)

print("\nLogical (short-circuit)")
age, has_cnic = 19, False
print("  age >= 18 and has_cnic:", age >= 18 and has_cnic)
print("  age >= 18 or has_cnic:", age >= 18 or has_cnic)
print("  not has_cnic:", not has_cnic)
print("  'and'/'or' return an operand: '' or 'guest' ->", "" or "guest", "| 0 and 1/0 ->", 0 and 1 / 0)

print("\nAssignment operators")
x = 10
x += 5;  print("  x += 5  ->", x)
x -= 3;  print("  x -= 3  ->", x)
x *= 2;  print("  x *= 2  ->", x)
x //= 4; print("  x //= 4 ->", x)
x **= 2; print("  x **= 2 ->", x)
x %= 7;  print("  x %= 7  ->", x)

print("\nBitwise (on the binary form)")
p, q = 12, 10          # 1100 and 1010
print(f"  {p:04b} & {q:04b} = {p & q:04b} ({p & q})")
print(f"  {p:04b} | {q:04b} = {p | q:04b} ({p | q})")
print(f"  {p:04b} ^ {q:04b} = {p ^ q:04b} ({p ^ q})")
print(f"  {p} << 1 = {p << 1}, {p} >> 2 = {p >> 2}, ~{p} = {~p}")

print("\nMembership and identity")
skills = ["python", "sql", "git"]
print("  'sql' in skills:", "sql" in skills, "| 'java' not in skills:", "java" not in skills)
print("  'AI' in 'Diploma in AI':", "AI" in "Diploma in AI", "| key in dict:", "cgpa" in {"cgpa": 3.1})
m1 = [1, 2]; m2 = [1, 2]
print("  m1 == m2:", m1 == m2, "| m1 is m2:", m1 is m2, "| x is None:", x is None)

print("\nPrecedence: ** > unary - > * / // % > + - > comparisons > not > and > or")
print("  2 + 3 * 4 ** 2 =", 2 + 3 * 4 ** 2)
print("  -3 ** 2 =", -3 ** 2, " vs (-3) ** 2 =", (-3) ** 2)
print("  not True or True =", not True or True, " vs not (True or True) =", not (True or True))
print("  2 ** 3 ** 2 =", 2 ** 3 ** 2, "(right-to-left)")
