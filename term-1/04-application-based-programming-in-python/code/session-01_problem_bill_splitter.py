"""
Session 1 · Real-life problem: the dinner bill splitter
-------------------------------------------------------
PROBLEM
Five friends eat at a restaurant in Karachi. The menu prices exclude tax.
Write a program that:
  1. stores each person's items in variables and lists,
  2. adds 16 % sales tax and a 10 % service charge (on the pre-tax subtotal),
  3. splits the shared starter equally,
  4. prints a neat receipt showing what each person owes, rounded to the
     nearest rupee, and checks that the shares add up to the total.

SOLUTION: only variables, arithmetic, lists, a loop and f-strings.
Run:  python session-01_problem_bill_splitter.py
"""
TAX_RATE = 0.16          # constants in ALL_CAPS
SERVICE_RATE = 0.10
shared_starter = 1_800   # one platter of fries and wings for the table

orders = {               # person -> list of (item, price)
    "Ali":    [("Chicken karahi (half)", 1_450), ("Mint lemonade", 350)],
    "Sana":   [("Daal makhni", 850), ("Garlic naan x2", 300)],
    "Bilal":  [("Beef burger", 1_250), ("Soft drink", 200)],
    "Hira":   [("Grilled fish", 1_900)],
    "Usman":  [("Club sandwich", 950), ("Cold coffee", 550)],
}

people = list(orders)                      # the dict keys, in order
starter_share = shared_starter / len(people)

print(f"{'Person':8} {'Food':>8} {'Starter':>8} {'Service':>8} {'Tax':>8} {'Owes':>8}")
print("-" * 54)
grand_total = 0
shares = {}
for person in people:
    food = sum(price for _, price in orders[person])
    subtotal = food + starter_share
    service = subtotal * SERVICE_RATE
    tax = subtotal * TAX_RATE
    owes = subtotal + service + tax
    shares[person] = round(owes)
    grand_total += owes
    print(f"{person:8} {food:8,.0f} {starter_share:8,.0f} {service:8,.0f} {tax:8,.0f} {round(owes):8,}")

print("-" * 54)
bill = (sum(p for items in orders.values() for _, p in items) + shared_starter) * (1 + TAX_RATE + SERVICE_RATE)
print(f"{'Bill':8} {'':35} {bill:8,.0f}")
diff = sum(shares.values()) - round(bill)
print(f"Sum of rounded shares = {sum(shares.values()):,} (difference Rs {diff:+d}, caused by rounding)")
biggest = max(shares, key=shares.get)
print(f"Highest share: {biggest} (Rs {shares[biggest]:,})")

# --- Optional chart: what makes up each share (stacked bars) ---
import matplotlib
matplotlib.use("Agg")                     # draw to a file, no window needed
import matplotlib.pyplot as plt

food = [sum(p for _, p in orders[x]) for x in people]
extra = [starter_share] * len(people)
serv = [(f + starter_share) * SERVICE_RATE for f in food]
taxes = [(f + starter_share) * TAX_RATE for f in food]
fig, ax = plt.subplots(figsize=(7, 3.6))
bottom = [0] * len(people)
for values, label, colour in [(food, "Food", "#FF6B1A"), (extra, "Starter share", "#FCD34D"),
                              (serv, "Service 10%", "#A78BFA"), (taxes, "Tax 16%", "#F43F5E")]:
    ax.bar(people, values, bottom=bottom, label=label, color=colour)
    bottom = [b + v for b, v in zip(bottom, values)]
for i, total in enumerate(bottom):
    ax.text(i, total + 40, f"Rs {round(total):,}", ha="center", fontsize=9)
ax.set_ylabel("Rupees"); ax.set_title("What each friend pays"); ax.set_ylim(0, max(bottom) * 1.15)
ax.legend(ncol=4, fontsize=8, loc="upper center")
fig.tight_layout(); fig.savefig("session-01_problem_bill_splitter.png", dpi=110)
print("Chart saved: session-01_problem_bill_splitter.png")
