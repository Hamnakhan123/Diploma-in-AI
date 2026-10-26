"""
Session 4 · Example 1: recursive functions
------------------------------------------
Every recursive function needs (1) a BASE CASE that stops, and (2) a
RECURSIVE CASE that moves closer to the base case.
Run:  python session-04_recursion.py
"""
import sys
from functools import lru_cache

def factorial(n):
    """n! = n x (n-1)!, with 0! = 1."""
    if n <= 1:                 # base case
        return 1
    return n * factorial(n - 1)  # recursive case: a smaller problem

print("5! =", factorial(5), "| 20! =", factorial(20))

# Trace the calls so the 'stack' becomes visible
def factorial_trace(n, depth=0):
    print("  " * depth + f"factorial({n}) called")
    result = 1 if n <= 1 else n * factorial_trace(n - 1, depth + 1)
    print("  " * depth + f"factorial({n}) returns {result}")
    return result
factorial_trace(4)

# Sum of digits and string reversal: recursion on smaller pieces
def digit_sum(n):
    return n if n < 10 else n % 10 + digit_sum(n // 10)
def reverse(s):
    return s if len(s) <= 1 else reverse(s[1:]) + s[0]
print("digit_sum(98765) =", digit_sum(98765), "| reverse('karachi') =", reverse("karachi"))

# Recursion shines on nested (tree-shaped) data
menu = {"Food": {"Desi": ["Biryani", "Nihari"], "Fast food": ["Burger", "Pizza"]},
        "Drinks": ["Chai", "Lassi"]}
def count_items(node):
    if isinstance(node, list):             # base case: a list of dishes
        return len(node)
    return sum(count_items(child) for child in node.values())
print("dishes in nested menu:", count_items(menu))

# Naive Fibonacci repeats work; caching (memoisation) fixes it
calls = 0
def fib(n):
    global calls; calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(25); print("naive fib(25) made", f"{calls:,}", "calls")

@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)
print("fib_memo(25) =", fib_memo(25), "|", fib_memo.cache_info())
print("fib_memo(300) has", len(str(fib_memo(300))), "digits")

# Python limits recursion depth to protect the call stack
print("recursion limit:", sys.getrecursionlimit())
try:
    factorial(5000)
except RecursionError as e:
    print("RecursionError:", str(e)[:40], "... -> use a loop for very deep problems")

def factorial_loop(n):          # the iterative version never hits the limit
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result
print("factorial_loop(1500) has", len(str(factorial_loop(1500))), "digits")

# Chart: calls made by naive vs memoised Fibonacci (exact counts, not timings)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ns, naive_calls, memo_calls = list(range(1, 26)), [], []
for n in ns:
    calls = 0; fib(n); naive_calls.append(calls)
    fib_memo.cache_clear(); fib_memo(n); memo_calls.append(fib_memo.cache_info().misses)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(ns, naive_calls, "o-", color="#F43F5E", label="naive fib(n)")
ax.plot(ns, memo_calls, "s-", color="#FF6B1A", label="fib_memo(n), cached")
ax.set_yscale("log"); ax.set_xlabel("n"); ax.set_ylabel("function calls (log scale)")
ax.set_title("Memoisation turns exponential work into linear work"); ax.legend()
fig.tight_layout(); fig.savefig("session-04_recursion.png", dpi=110)
print("naive calls for n = 10, 20, 25:", naive_calls[9], naive_calls[19], naive_calls[24], "| cached:", memo_calls[24])
print("Chart saved: session-04_recursion.png")
