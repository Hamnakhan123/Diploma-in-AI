"""
Session 2 · Example 3: decisions and loops
------------------------------------------
Run:  python session-02_control_flow.py
"""
# 1. if / elif / else : the first true branch wins
def grade(mark):
    if mark >= 85:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 55:
        return "C"
    else:
        return "F"
print("grades:", {m: grade(m) for m in [92, 85, 71, 40]})

# Conditional expression (one-line if)
temp = 38
print("weather:", "hot" if temp > 35 else "pleasant")

# 2. match / case (Python 3.10+): compare a value against patterns
def command(text):
    match text.split():
        case ["add", item]:
            return f"adding {item}"
        case ["remove", item]:
            return f"removing {item}"
        case ["list"]:
            return "listing all items"
        case _:
            return "unknown command"
for c in ["add milk", "remove eggs", "list", "fly away"]:
    print(f"  {c!r:14} -> {command(c)}")

# 3. for loop over a sequence, with enumerate and zip
students = ["Ali", "Sana", "Bilal"]
marks = [78, 91, 64]
for rank, (name, m) in enumerate(sorted(zip(students, marks), key=lambda t: -t[1]), start=1):
    print(f"  #{rank} {name:6} {m}")

# range(start, stop, step): stop is excluded
print("range(1, 11, 3):", list(range(1, 11, 3)), "| countdown:", list(range(5, 0, -1)))

# 4. while loop: repeat until a condition fails
balance, months = 50_000, 0
while balance < 100_000:          # savings grow 2 % per month
    balance *= 1.02
    months += 1
print(f"Rs 50,000 doubles at 2%/month after {months} months (Rs {balance:,.0f})")

# 5. break, continue, pass and the loop 'else'
for n in range(2, 30):
    if n % 2 == 0:
        continue                  # skip even numbers
    for d in range(3, int(n ** 0.5) + 1, 2):
        if n % d == 0:
            break                 # not prime: leave the inner loop
    else:
        print(n, end=" ")         # runs only if the inner loop did NOT break
print("<- odd primes below 30")

def todo():
    pass                          # placeholder: a block cannot be empty

# 6. Nested loops: a multiplication grid
for i in range(1, 4):
    print("  " + " ".join(f"{i * j:3}" for j in range(1, 6)))

# 7. Comprehensions: a loop that builds a collection in one expression
squares = [n * n for n in range(1, 8)]
evens = [n for n in squares if n % 2 == 0]
lengths = {name: len(name) for name in students}
print("squares:", squares, "| even squares:", evens, "| lengths:", lengths)
