"""
Session 3 · Example 1: defining, calling and returning
------------------------------------------------------
Run:  python session-03_define_call.py
"""
import math

# 1. Built-in functions are always available
marks = [78, 91, 64, 85]
print("built-ins:", len(marks), max(marks), min(marks), sum(marks), round(sum(marks) / len(marks), 1))
# Functions from a module need an import
print("math module:", math.sqrt(144), math.ceil(4.1), round(math.pi, 4))

# 2. A user-defined function: def, name, parameters, colon, indented body
def greet(name):
    """Return a greeting for one person."""
    return f"Assalam-o-Alaikum, {name}!"

print(greet("Ayesha"))            # call it with an argument

# 3. A function with no return statement returns None
def show_line(width):
    print("-" * width)

result = show_line(20)
print("show_line returned:", result)

# 4. Returning several values (really a tuple) and unpacking them
def stats(values):
    """Return mean, min and max of a list of numbers."""
    mean = sum(values) / len(values)
    return mean, min(values), max(values)

avg, low, high = stats(marks)
print(f"mean {avg:.2f}, lowest {low}, highest {high}")
print("raw return value:", stats(marks))

# 5. return ends the function early (guard clauses)
def safe_divide(a, b):
    if b == 0:
        return None               # leave immediately, skip the rest
    return a / b
print("safe_divide:", safe_divide(10, 4), safe_divide(1, 0))

# 6. Functions are objects: store them, pass them, return them
def square(x): return x * x
def cube(x): return x ** 3
operations = {"square": square, "cube": cube}
for name, fn in operations.items():
    print(f"{name}(4) = {fn(4)}")

def apply_to_all(fn, values):
    return [fn(v) for v in values]
print("apply_to_all(square):", apply_to_all(square, [1, 2, 3]))

# 7. Type hints and docstrings document the contract (not enforced at runtime)
def bmi(weight_kg: float, height_m: float) -> float:
    """Body-mass index = weight / height squared, rounded to 1 decimal."""
    return round(weight_kg / height_m ** 2, 1)
print("bmi(68, 1.72) =", bmi(68, 1.72), "| hints:", bmi.__annotations__)
help(bmi)
