"""
Session 2 · Real-life problem: slab-based electricity bill
-----------------------------------------------------------
PROBLEM
Electricity in many cities is billed in SLABS: the first units are cheap and
each extra block costs more. Using the ILLUSTRATIVE tariff below (made-up
rates for practice, not an official tariff), write a program that:
  1. computes the energy charge slab by slab,
  2. adds a fixed meter rent and 17 % tax on the energy charge,
  3. applies a 5 % late surcharge if paid after the due date,
  4. prints an itemised bill for several households and draws a chart of
     bill amount against units used.

SOLUTION: data types, operators, if/elif/else, for and while loops.
Run:  python session-02_problem_electricity_bill.py
"""
SLABS = [            # (units in this slab, rate per unit in Rs); None = no upper limit
    (100, 22.0),
    (100, 28.5),
    (100, 34.0),
    (None, 42.0),
]
METER_RENT = 150
TAX = 0.17
LATE = 0.05

def energy_charge(units, verbose=False):
    """Walk through the slabs, charging each block at its own rate."""
    remaining, charge, start = units, 0.0, 0
    for size, rate in SLABS:
        if remaining <= 0:
            break
        used = remaining if size is None else min(remaining, size)
        if verbose:
            print(f"    units {start + 1:>3}-{start + used:<3} x Rs {rate:5.2f} = Rs {used * rate:9,.2f}")
        charge += used * rate
        remaining -= used
        start += used
    return charge

def bill(units, late=False, verbose=False):
    energy = energy_charge(units, verbose)
    total = energy + energy * TAX + METER_RENT
    if late:
        total *= 1 + LATE
    return energy, total

households = [("Flat A-12", 85, False), ("House 47", 260, False), ("Shop 3", 410, True)]
for name, units, late in households:
    print(f"{name}: {units} units{' (paid late)' if late else ''}")
    energy, total = bill(units, late, verbose=True)
    print(f"    energy Rs {energy:,.2f} + tax Rs {energy * TAX:,.2f} + rent Rs {METER_RENT}"
          f"{' + 5% late' if late else ''} = Rs {total:,.0f}\n")

# How many units can a family use if the budget is Rs 8,000? (while loop search)
units = 0
while bill(units + 1)[1] <= 8_000:
    units += 1
print(f"Max units within a Rs 8,000 budget: {units} (bill Rs {bill(units)[1]:,.0f})")

# Chart: the bill is piecewise linear and gets steeper at each slab boundary
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
xs = list(range(0, 501, 5))
ys = [bill(u)[1] for u in xs]
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(xs, ys, color="#FF6B1A", lw=2.5)
for edge in (100, 200, 300):
    ax.axvline(edge, color="#A78BFA", ls="--", lw=1)
ax.set_xlabel("Units used in the month"); ax.set_ylabel("Total bill (Rs)")
ax.set_title("Slab tariff: each extra unit costs more after every boundary")
fig.tight_layout(); fig.savefig("session-02_problem_electricity_bill.png", dpi=110)
print("Chart saved: session-02_problem_electricity_bill.png")
