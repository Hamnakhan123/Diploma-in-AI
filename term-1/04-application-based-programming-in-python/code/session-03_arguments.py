"""
Session 3 · Example 3: parameters and every kind of argument
------------------------------------------------------------
Run:  python session-03_arguments.py
"""
# Parameters are the names in the definition; arguments are the values in the call.
def order(item, qty, price):
    return f"{qty} x {item} @ Rs {price} = Rs {qty * price:,}"

print("positional:", order("biryani", 2, 450))                 # matched by position
print("keyword:   ", order(price=450, item="biryani", qty=2))  # matched by name
print("mixed:     ", order("chai", price=80, qty=3))           # positional first

# Default values make a parameter optional
def ticket_price(base, child=False, discount=0.0):
    price = base * (0.5 if child else 1)
    return round(price * (1 - discount))
print("defaults:", ticket_price(1200), ticket_price(1200, child=True), ticket_price(1200, discount=0.1))

# *args collects extra positional arguments into a tuple
def total(*amounts):
    print("  args tuple:", amounts)
    return sum(amounts)
print("*args:", total(100, 250, 75))

# **kwargs collects extra keyword arguments into a dict
def profile(name, **details):
    extras = ", ".join(f"{k}={v}" for k, v in details.items())
    return f"{name} ({extras})"
print("**kwargs:", profile("Hira", city="Karachi", cgpa=3.7, semester=2))

# Keyword-only (after *) and positional-only (before /) parameters
def transfer(amount, /, *, to_account, note=""):
    return f"Sent Rs {amount:,} to {to_account} {note}".strip()
print("kw-only:", transfer(5000, to_account="PK36-XXXX-0042", note="(rent)"))
try:
    transfer(5000, "PK36")                          # to_account must be given by name
except TypeError as e:
    print("  TypeError:", e)
try:
    transfer(amount=5000, to_account="PK36")        # amount must be given by position
except TypeError as e:
    print("  TypeError:", e)

# Unpacking a list/dict INTO arguments with * and **
args = ["samosa", 6, 40]
kwargs = {"item": "jalebi", "qty": 1, "price": 300}
print("unpack *:", order(*args), "| unpack **:", order(**kwargs))

# The mutable-default trap and its fix
def add_bad(item, basket=[]):          # the SAME list is reused on every call
    basket.append(item); return basket
def add_good(item, basket=None):
    if basket is None:
        basket = []                     # a fresh list each call
    basket.append(item); return basket
print("bad :", add_bad("milk"), add_bad("eggs"))
print("good:", add_good("milk"), add_good("eggs"))

# Arguments are passed by object reference: mutating a list inside is visible outside
def give_bonus(marks):
    for i in range(len(marks)):
        marks[i] += 5
scores = [60, 70]
give_bonus(scores)
print("after give_bonus:", scores)
