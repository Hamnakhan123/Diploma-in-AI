"""
Session 2 · Real-life problem: how many agents does the help-line need?
----------------------------------------------------------------------
PROBLEM
A bank's help-line receives on average 18 calls per hour between 9 and 10 am.
Each agent can handle 4 calls per hour. Management asks:
  1. What is the probability of more than 25 calls in that hour?
  2. How many agents are needed so that the chance of more calls than the team
     can handle is at most 5 %?
  3. A quality check finds 6 % of calls are complaints. Out of 18 calls,
     what is P(at least 3 complaints)? What is the expected number?
  4. Verify the answers with a Monte Carlo simulation of 100,000 mornings.

MODEL
Calls in an hour  ~ Poisson(lambda = 18)    (random, independent arrivals)
Complaints        ~ Binomial(n = 18, p = 0.06)

Run:  python session-02_problem_call_centre.py
"""
import math
import numpy as np
from scipy import stats

lam, per_agent = 18, 4
calls = stats.poisson(lam)

# 1. Tail probability
print(f"1. P(calls > 25) = {calls.sf(25):.4f}")

# 2. Smallest team whose capacity covers demand at least 95 % of the time
for agents in range(1, 15):
    capacity = agents * per_agent
    p_overload = calls.sf(capacity)          # P(calls > capacity)
    print(f"   {agents} agents -> capacity {capacity:>2} calls, P(overload) = {p_overload:.4f}")
    if p_overload <= 0.05:
        break
print(f"2. Hire {agents} agents (the 95th percentile of demand is {calls.ppf(0.95):.0f} calls).")

# 3. Complaints
comp = stats.binom(18, 0.06)
print(f"3. P(>= 3 complaints) = {comp.sf(2):.4f}, expected complaints = {comp.mean():.2f}")
# The same answer from the formula, to show there is no magic:
p_le2 = sum(math.comb(18, k) * 0.06 ** k * 0.94 ** (18 - k) for k in range(3))
print(f"   by formula: 1 - P(X <= 2) = {1 - p_le2:.4f}")

# 4. Monte Carlo check
rng = np.random.default_rng(2026)
mornings = rng.poisson(lam, size=100_000)
print(f"4. Simulated P(calls > 25)        = {np.mean(mornings > 25):.4f}")
print(f"   Simulated P(overload, {agents} agents) = {np.mean(mornings > agents * per_agent):.4f}")
complaints = rng.binomial(18, 0.06, size=100_000)
print(f"   Simulated P(>= 3 complaints)    = {np.mean(complaints >= 3):.4f}")
