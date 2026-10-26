"""
Session 2 · Example 1: Classical vs empirical probability, and the basic rules
------------------------------------------------------------------------------
* Classical probability counts equally likely outcomes in a sample space.
* Empirical probability counts how often something happened in trials.
* The law of large numbers says the second approaches the first as trials grow.
We also check the addition rule, the multiplication rule for independent
events, the complement rule and conditional probability on two dice.

Run:  python session-02_probability_rules.py
"""
from fractions import Fraction
from itertools import product
import numpy as np

rng = np.random.default_rng(seed=7)          # fixed seed -> same output every run

# ---- 1. Sample space of two dice: 36 equally likely ordered pairs ------------------
space = list(product(range(1, 7), repeat=2))
def P(event):
    """Classical probability: favourable outcomes / total outcomes (exact fraction)."""
    fav = [o for o in space if event(o)]
    return Fraction(len(fav), len(space))

sum7 = lambda o: o[0] + o[1] == 7
double = lambda o: o[0] == o[1]
first6 = lambda o: o[0] == 6
print("Sample space size:", len(space))
print("P(sum = 7)            =", P(sum7))
print("P(double)             =", P(double))
print("P(sum=7 or double)    =", P(lambda o: sum7(o) or double(o)),
      "  (addition rule: 1/6 + 1/6 - 0, the events are mutually exclusive)")
print("P(first=6 or double)  =", P(lambda o: first6(o) or double(o)),
      "  (= 1/6 + 1/6 - 1/36 because (6,6) is counted twice)")
print("P(no six at all)      =", P(lambda o: 6 not in o), "  complement of P(at least one six) =",
      1 - P(lambda o: 6 not in o))

# ---- 2. Conditional probability: P(A | B) = P(A and B) / P(B) ----------------------
sum_ge_10 = lambda o: o[0] + o[1] >= 10
print("\nP(sum >= 10)                 =", P(sum_ge_10))
print("P(sum >= 10 | first die = 6) =", P(lambda o: sum_ge_10(o) and first6(o)) / P(first6),
      "  knowing the first die is 6 makes a big sum much more likely")

# ---- 3. Independence: P(A and B) = P(A) * P(B) ---------------------------------------
even_first = lambda o: o[0] % 2 == 0
second_gt4 = lambda o: o[1] > 4
lhs = P(lambda o: even_first(o) and second_gt4(o))
print("\nIndependent? P(A and B) =", lhs, " P(A)*P(B) =", P(even_first) * P(second_gt4),
      "->", lhs == P(even_first) * P(second_gt4))

# ---- 4. Law of large numbers: empirical -> classical --------------------------------
print("\nEmpirical P(sum = 7) as the number of throws grows (true value 0.1667):")
for n in [10, 100, 1_000, 10_000, 100_000]:
    d = rng.integers(1, 7, size=(n, 2))
    print(f"  n = {n:>7,}:  {np.mean(d.sum(axis=1) == 7):.4f}")

# ---- 5. Counting: permutations and combinations -------------------------------------
from math import comb, perm
print("\nWays to choose a 3-person committee from 10 students: C(10,3) =", comb(10, 3))
print("Ways to award gold, silver, bronze among 10 students:  P(10,3) =", perm(10, 3))
print("P(a 4-digit PIN guessed in one try)  =", Fraction(1, 10 ** 4))
