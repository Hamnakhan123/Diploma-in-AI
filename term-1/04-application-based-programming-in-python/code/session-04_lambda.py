"""
Session 4 · Example 2: lambda functions with sorted, map, filter and reduce
---------------------------------------------------------------------------
lambda arguments: expression   -> a small anonymous function of ONE expression
Run:  python session-04_lambda.py
"""
from functools import reduce

square = lambda x: x * x          # works, but a def is clearer for named functions
print("square(7) =", square(7))
add = lambda a, b=10: a + b
print("add(5) =", add(5), "| add(5, 1) =", add(5, 1))

students = [
    {"name": "Ali", "cgpa": 3.1, "city": "Karachi"},
    {"name": "Sana", "cgpa": 3.8, "city": "Lahore"},
    {"name": "Bilal", "cgpa": 2.7, "city": "Karachi"},
    {"name": "Hira", "cgpa": 3.8, "city": "Quetta"},
]

# 1. sorted / max / min with key=lambda: the most common real use
by_cgpa = sorted(students, key=lambda s: s["cgpa"], reverse=True)
print("by cgpa:", [s["name"] for s in by_cgpa])
by_cgpa_then_name = sorted(students, key=lambda s: (-s["cgpa"], s["name"]))
print("tie-break by name:", [s["name"] for s in by_cgpa_then_name])
print("top student:", max(students, key=lambda s: s["cgpa"])["name"])

# 2. map applies a function to every item (returns an iterator)
prices = [1200, 850, 3400]
with_tax = list(map(lambda p: round(p * 1.16), prices))
print("map with tax:", with_tax)

# 3. filter keeps items where the function returns True
karachi = list(filter(lambda s: s["city"] == "Karachi", students))
print("filter Karachi:", [s["name"] for s in karachi])

# 4. reduce folds a sequence into one value
total = reduce(lambda acc, p: acc + p, prices, 0)
longest = reduce(lambda a, b: a if len(a) >= len(b) else b, [s["name"] for s in students])
print("reduce total:", total, "| longest name:", longest)

# Comprehensions often read better than map/filter
print("comprehension:", [round(p * 1.16) for p in prices if p > 1000])

# 5. Lambdas as small callbacks: a dispatch table of operations
ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "*": lambda a, b: a * b, "/": lambda a, b: a / b if b else float("nan")}
for sym in ops:
    print(f"  12 {sym} 4 = {ops[sym](12, 4)}")

# 6. A function that RETURNS a lambda (a function factory)
def make_discount(pct):
    return lambda price: round(price * (1 - pct / 100))
eid_sale, clearance = make_discount(20), make_discount(50)
print("Eid sale:", eid_sale(5000), "| clearance:", clearance(5000))

# 7. The late-binding trap in loops
fns = [lambda: i for i in range(3)]
print("late binding:", [f() for f in fns], "-> fix with a default:", [f() for f in [lambda i=i: i for i in range(3)]])
