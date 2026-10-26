"""
Session 1 · Example 3: variables, assignment and dynamic typing
---------------------------------------------------------------
Run:  python session-01_variables.py
"""
# 1. A variable is a name bound to an object
marks = 78
print("marks =", marks, "| type:", type(marks).__name__, "| isinstance int:", isinstance(marks, int))

# 2. Dynamic typing: the same name can later point to another type
marks = "seventy-eight"
print("marks =", marks, "| type:", type(marks).__name__)

# 3. Multiple assignment and unpacking
x = y = z = 0                         # one object, three names
name, age, cgpa = "Ayesha", 21, 3.62  # tuple unpacking
print("x, y, z =", x, y, z, "|", name, age, cgpa)

# 4. Swapping without a temporary variable
left, right = "tea", "coffee"
left, right = right, left
print("after swap:", left, right)

# 5. Augmented assignment
balance = 1_000
balance += 250        # balance = balance + 250
balance -= 100
balance *= 2
print("balance:", balance)

# 6. Names are labels, not boxes: two names can share one list
a = [1, 2, 3]
b = a                 # b is another label on the SAME list
b.append(4)
print("a:", a, "| a is b:", a is b)
c = a.copy()          # a new list
c.append(5)
print("a:", a, "| c:", c, "| a is c:", a is c)

# 7. Constants are a naming convention (ALL_CAPS); Python does not enforce them
GST_RATE = 0.18
price = 2_500
print(f"price with GST: Rs {price * (1 + GST_RATE):,.2f}")

# 8. del removes the name, not necessarily the object
temp = 42
del temp
print("'temp' still defined?", "temp" in dir())

# 9. Reading input safely (simulated here so the script runs unattended)
def ask(prompt, default):
    """Use input() in real programs; this demo returns a fixed answer."""
    print(prompt + default)
    return default

age_text = ask("Enter your age: ", "21")
age = int(age_text)               # input() always returns a str: convert it
print("Next year you will be", age + 1)
