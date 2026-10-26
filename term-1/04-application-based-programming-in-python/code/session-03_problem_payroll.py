"""
Session 3 · Real-life problem: monthly salary slips
---------------------------------------------------
PROBLEM
An HR officer must produce salary slips. For each employee:
  gross = basic + house rent (45 % of basic) + medical (10 % of basic) + overtime
  overtime = hours x (basic / 208) x 1.5          (208 working hours a month)
  income tax uses the ILLUSTRATIVE annual slabs below (practice values only)
  provident fund = 8 % of basic
  net = gross - tax - provident fund
Write it as small, single-purpose functions with docstrings, default
arguments and keyword arguments, then print a slip per employee and a summary.
Run:  python session-03_problem_payroll.py
"""
TAX_SLABS = [        # (annual income up to, fixed tax, rate on the excess above the previous limit)
    (600_000, 0, 0.00),
    (1_200_000, 0, 0.05),
    (2_200_000, 30_000, 0.15),
    (3_200_000, 180_000, 0.25),
    (float("inf"), 430_000, 0.35),
]

def allowances(basic, house_pct=0.45, medical_pct=0.10):
    """Return (house rent, medical) allowances as a tuple."""
    return basic * house_pct, basic * medical_pct

def overtime_pay(basic, hours=0, rate=1.5, monthly_hours=208):
    """Overtime is paid at 1.5x the hourly rate by default."""
    return hours * (basic / monthly_hours) * rate

def annual_tax(income):
    """Apply the slab table to a yearly income."""
    lower = 0
    for upper, fixed, rate in TAX_SLABS:
        if income <= upper:
            return fixed + (income - lower) * rate
        lower = upper

def monthly_slip(name, basic, *, overtime_hours=0, pf_rate=0.08):
    """Build one salary slip as a dict. Keyword-only options avoid mix-ups."""
    house, medical = allowances(basic)
    ot = overtime_pay(basic, overtime_hours)
    gross = basic + house + medical + ot
    tax = annual_tax(gross * 12) / 12
    pf = basic * pf_rate
    return {"name": name, "basic": basic, "house": house, "medical": medical,
            "overtime": ot, "gross": gross, "tax": tax, "pf": pf, "net": gross - tax - pf}

def print_slip(slip):
    print(f"Salary slip: {slip['name']}")
    for key in ["basic", "house", "medical", "overtime", "gross", "tax", "pf", "net"]:
        sign = "-" if key in ("tax", "pf") else " "
        print(f"   {key:<9}{sign} Rs {slip[key]:>10,.0f}")
    print()

staff = [("Ahmed (lab engineer)", 60_000, 0), ("Fatima (lecturer)", 110_000, 0),
         ("Kamran (technician)", 45_000, 22), ("Zara (manager)", 210_000, 0)]
slips = [monthly_slip(n, b, overtime_hours=h) for n, b, h in staff]
for s in slips:
    print_slip(s)

def summary(slips):
    """Payroll totals and the effective tax rate per person."""
    print(f"{'Employee':22} {'Gross':>10} {'Tax':>9} {'Eff. tax':>8}")
    for s in slips:
        print(f"{s['name']:22} {s['gross']:>10,.0f} {s['tax']:>9,.0f} {s['tax'] / s['gross']:>8.1%}")
    print(f"{'TOTAL payroll cost':22} {sum(s['gross'] for s in slips):>10,.0f}")
summary(slips)
