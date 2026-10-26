"""
Session 3 · Mini project: loan / instalment planner
---------------------------------------------------
A small library of functions that answers real questions about a loan:
  emi()        - fixed monthly instalment (standard reducing-balance formula)
  schedule()   - month-by-month split into interest and principal
  compare()    - total cost of several tenures
Each function does one job, has a docstring and sensible defaults.
Run:  python session-03_project_loan_planner.py
"""
def emi(principal, annual_rate, years):
    """Monthly instalment: P*r*(1+r)^n / ((1+r)^n - 1), r = monthly rate, n = months."""
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    growth = (1 + r) ** n
    return principal * r * growth / (growth - 1)

def schedule(principal, annual_rate, years):
    """Yield (month, interest, principal_paid, balance) for every month."""
    pay = emi(principal, annual_rate, years)
    balance = principal
    for month in range(1, years * 12 + 1):
        interest = balance * annual_rate / 12
        paid = pay - interest
        balance -= paid
        yield month, interest, paid, max(balance, 0)

def compare(principal, annual_rate, tenures=(1, 2, 3, 5)):
    """Return a list of dicts comparing instalment and total interest by tenure."""
    rows = []
    for years in tenures:
        m = emi(principal, annual_rate, years)
        rows.append({"years": years, "emi": m, "total": m * years * 12,
                     "interest": m * years * 12 - principal})
    return rows

LOAN, RATE = 1_500_000, 0.18          # e.g. a used-car loan at 18 % a year
print(f"Loan Rs {LOAN:,} at {RATE:.0%} a year")
print(f"{'Years':>5} {'EMI':>10} {'Total paid':>12} {'Interest':>11}")
for row in compare(LOAN, RATE):
    print(f"{row['years']:>5} {row['emi']:>10,.0f} {row['total']:>12,.0f} {row['interest']:>11,.0f}")

print("\nFirst and last months of the 3-year plan")
rows = list(schedule(LOAN, RATE, 3))
for month, interest, paid, bal in rows[:3] + rows[-2:]:
    print(f"  month {month:>2}: interest {interest:>8,.0f}  principal {paid:>8,.0f}  balance {bal:>10,.0f}")

# Chart: how each instalment is split over time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
months = [r[0] for r in rows]
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.stackplot(months, [r[2] for r in rows], [r[1] for r in rows],
             labels=["Principal part", "Interest part"], colors=["#FF6B1A", "#A78BFA"])
ax.set_xlabel("Month"); ax.set_ylabel("Rs per instalment")
ax.set_title("Same instalment every month, but the interest share shrinks")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout(); fig.savefig("session-03_project_loan_planner.png", dpi=110)
print("Chart saved: session-03_project_loan_planner.png")
