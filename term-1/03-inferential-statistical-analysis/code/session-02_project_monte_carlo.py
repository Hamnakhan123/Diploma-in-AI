"""
Session 2 · Mini project: Monte Carlo profit simulator for a food stall
----------------------------------------------------------------------
A student plans a weekend biryani stall at a university fest and must decide
how many plates to cook. Uncertainty everywhere:
  * visitors per day          ~ Poisson(mean 220)
  * each visitor buys a plate  with probability 0.35   (Binomial)
  * price 350 PKR, cost 180 PKR per cooked plate, unsold plates are wasted
Goal: simulate 20,000 days for several cooking quantities, report the expected
profit, the 5th-95th percentile range and P(loss), pick the best quantity, and
save a chart: session-02_project_monte_carlo.png

This is the 'newsvendor problem', a classic in operations research.
Run:  python session-02_project_monte_carlo.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PRICE, COST = 350, 180
DAYS = 20_000
rng = np.random.default_rng(11)

# Demand is simulated ONCE and reused for every option (common random numbers),
# so differences between options are not caused by luck.
visitors = rng.poisson(220, size=DAYS)
demand = rng.binomial(visitors, 0.35)
print(f"Demand per day: mean {demand.mean():.1f}, sd {demand.std(ddof=1):.1f}, "
      f"min {demand.min()}, max {demand.max()}")

def profit_for(cooked):
    sold = np.minimum(demand, cooked)
    return sold * PRICE - cooked * COST

options = range(50, 111, 5)
results = []
print(f"\n{'cooked':>6} {'E[profit]':>10} {'5th pct':>8} {'95th pct':>9} {'P(loss)':>8} {'P(sold out)':>11}")
for q in options:
    pr = profit_for(q)
    results.append((q, pr.mean()))
    print(f"{q:>6} {pr.mean():>10,.0f} {np.percentile(pr, 5):>8,.0f} {np.percentile(pr, 95):>9,.0f} "
          f"{np.mean(pr < 0):>8.3f} {np.mean(demand >= q):>11.3f}")

best_q, best_p = max(results, key=lambda t: t[1])
# Theory check: the optimal quantity is the demand quantile at (price - cost) / price
critical = (PRICE - COST) / PRICE
print(f"\nBest quantity by simulation: {best_q} plates (expected profit {best_p:,.0f} PKR)")
print(f"Newsvendor theory: cook the {critical:.3f} quantile of demand = {np.quantile(demand, critical):.0f} plates")

qs, ps = zip(*results)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(qs, ps, marker="o", color="#FF6B1A")
ax.axvline(best_q, color="#A78BFA", ls="--", label=f"best = {best_q}")
ax.set_xlabel("plates cooked"); ax.set_ylabel("expected profit (PKR)")
ax.set_title("Expected daily profit vs quantity cooked (20,000 simulated days)")
ax.grid(alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig("session-02_project_monte_carlo.png", dpi=100)
print("Saved chart: session-02_project_monte_carlo.png")
