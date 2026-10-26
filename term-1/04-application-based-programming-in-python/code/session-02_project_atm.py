"""
Session 2 · Mini project: menu-driven ATM simulator
---------------------------------------------------
A classic console program that combines every construct of the session:
data types (dict, list, float), operators, if/elif/else, match/case,
while loops with break/continue, and input validation.
Inputs are scripted so the program runs unattended; replace `next_input`
with `input` to play it yourself.
Run:  python session-02_project_atm.py
"""
PIN = "4321"
DAILY_LIMIT = 50_000
NOTES = [5000, 1000, 500]          # notes the machine can dispense

account = {"holder": "Sana Tariq", "balance": 82_500.0, "withdrawn_today": 0}
history = []

scripted = iter(["1111", "4321",           # wrong PIN, then right PIN
                 "1", "2", "12500", "2", "7300", "3", "5000", "2", "60000", "4", "9", "5"])
def next_input(prompt):
    value = next(scripted)
    print(prompt + value)
    return value

def dispense(amount):
    """Greedy split of an amount into notes; returns dict or None if impossible."""
    plan = {}
    for note in NOTES:
        plan[note], amount = divmod(amount, note)
    return None if amount else {n: c for n, c in plan.items() if c}

# ---- login: three attempts ----
for attempt in range(1, 4):
    if next_input("Enter PIN: ") == PIN:
        print(f"Welcome, {account['holder']}!\n")
        break
    print(f"  wrong PIN ({3 - attempt} attempts left)")
else:
    raise SystemExit("Card retained. Please contact your branch.")

# ---- main menu ----
while True:
    choice = next_input("[1] Balance [2] Withdraw [3] Deposit [4] Mini statement [5] Exit > ")
    match choice:
        case "1":
            print(f"  Balance: Rs {account['balance']:,.2f}")
        case "2":
            amount = int(next_input("  Amount: "))
            if amount % 500:
                print("  Amount must be a multiple of 500"); continue
            if amount > account["balance"]:
                print("  Insufficient balance"); continue
            if account["withdrawn_today"] + amount > DAILY_LIMIT:
                print(f"  Daily limit Rs {DAILY_LIMIT:,} exceeded"); continue
            notes = dispense(amount)
            account["balance"] -= amount
            account["withdrawn_today"] += amount
            history.append(("withdraw", -amount))
            print("  Dispensed:", ", ".join(f"{c} x Rs {n}" for n, c in notes.items()))
        case "3":
            amount = float(next_input("  Deposit amount: "))
            account["balance"] += amount
            history.append(("deposit", amount))
            print(f"  Deposited Rs {amount:,.2f}")
        case "4":
            for kind, amt in history[-5:]:
                print(f"  {kind:9} {amt:+12,.2f}")
            print(f"  {'balance':9} {account['balance']:12,.2f}")
        case "5":
            print("Thank you. Please take your card.")
            break
        case _:
            print("  Invalid option, choose 1-5")
