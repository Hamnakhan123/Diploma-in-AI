"""
Session 9 · Real-life problem: a point-of-sale (billing) desktop app
--------------------------------------------------------------------
PROBLEM
A campus stationery shop wants a simple billing screen:
  - pick an item from a list and a quantity (Spinbox), press "Add"
  - the cart (a ttk.Treeview table) shows item, qty, price, line total
  - "Remove" deletes the selected line; a discount code can be applied
  - totals show subtotal, discount, 16 % sales tax and grand total
  - "Print receipt" writes a text receipt file
Design: a Cart class holds ALL the rules (testable without a screen);
the Tkinter layer only displays the cart and forwards button clicks.
Run:  python session-09_problem_pos_billing.py
"""
from datetime import datetime
from gui_support import gui_available, banner

CATALOGUE = {"A4 register": 180, "Ball pen (blue)": 30, "Gel pen": 60, "Highlighter": 90,
             "Geometry box": 450, "Scientific calculator": 3200, "USB drive 32GB": 1150}
CODES = {"STUDENT10": 0.10, "EID20": 0.20}
TAX = 0.16

class Cart:
    def __init__(self):
        self.lines, self.discount_code = {}, None
    def add(self, item, qty):
        if item not in CATALOGUE:
            raise ValueError(f"unknown item {item!r}")
        if not 1 <= qty <= 100:
            raise ValueError("quantity must be 1-100")
        self.lines[item] = self.lines.get(item, 0) + qty
    def remove(self, item):
        self.lines.pop(item, None)
    def apply_code(self, code):
        code = code.strip().upper()
        if code not in CODES:
            raise ValueError(f"invalid code {code!r}")
        self.discount_code = code
    def totals(self):
        sub = sum(CATALOGUE[i] * q for i, q in self.lines.items())
        disc = sub * CODES.get(self.discount_code, 0)
        tax = (sub - disc) * TAX
        return {"subtotal": sub, "discount": disc, "tax": tax, "total": round(sub - disc + tax)}
    def receipt(self, when):
        t = self.totals()
        rows = [f"{'CAMPUS STATIONERS':^40}", f"{when:%d %b %Y %H:%M}".center(40), "-" * 40]
        rows += [f"{i[:22]:<22}{q:>4} x{CATALOGUE[i]:>5} {CATALOGUE[i] * q:>7,}" for i, q in self.lines.items()]
        rows += ["-" * 40, f"{'Subtotal':<30}{t['subtotal']:>10,.0f}"]
        if t["discount"]:
            rows.append(f"{'Discount (' + self.discount_code + ')':<30}{-t['discount']:>10,.0f}")
        rows += [f"{'Sales tax 16%':<30}{t['tax']:>10,.0f}", f"{'TOTAL Rs':<30}{t['total']:>10,}", "-" * 40,
                 f"{'Thank you!':^40}"]
        return "\n".join(rows)

def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    cart = Cart()
    root = tk.Tk(); root.title("Campus Stationers - POS")
    left = tk.Frame(root, padx=8, pady=8); left.pack(side="left", fill="y")
    items = tk.Listbox(left, height=8, exportselection=False)
    for name, price in CATALOGUE.items():
        items.insert("end", name)
    items.pack()
    qty = tk.Spinbox(left, from_=1, to=100, width=5); qty.pack(pady=4)
    code = tk.Entry(left, width=12); code.pack(pady=(10, 2))
    right = tk.Frame(root, padx=8, pady=8); right.pack(side="right", fill="both", expand=True)
    table = ttk.Treeview(right, columns=("qty", "price", "line"), height=8)
    for col, text in [("#0", "Item"), ("qty", "Qty"), ("price", "Price"), ("line", "Total")]:
        table.heading(col, text=text)
    table.pack(fill="both", expand=True)
    totals = tk.Label(right, justify="right", font=("Consolas", 11)); totals.pack(anchor="e")

    def refresh():
        table.delete(*table.get_children())
        for i, q in cart.lines.items():
            table.insert("", "end", iid=i, text=i, values=(q, CATALOGUE[i], CATALOGUE[i] * q))
        t = cart.totals()
        totals.config(text=f"Subtotal {t['subtotal']:>8,.0f}\nDiscount {-t['discount']:>8,.0f}\n"
                           f"Tax 16%  {t['tax']:>8,.0f}\nTOTAL    {t['total']:>8,}")
    def add():
        sel = items.curselection()
        try:
            cart.add(items.get(sel[0]) if sel else "", int(qty.get())); refresh()
        except ValueError as e:
            messagebox.showwarning("Cannot add", str(e))
    def remove():
        for iid in table.selection():
            cart.remove(iid)
        refresh()
    def apply():
        try:
            cart.apply_code(code.get()); refresh()
        except ValueError as e:
            messagebox.showerror("Discount", str(e))
    def print_receipt():
        with open("receipt.txt", "w", encoding="utf-8") as f:
            f.write(cart.receipt(datetime.now()))
        messagebox.showinfo("Receipt", "Saved to receipt.txt")
    for text, cmd in [("Add", add), ("Apply code", apply), ("Remove line", remove), ("Print receipt", print_receipt)]:
        tk.Button(left, text=text, width=14, command=cmd).pack(pady=2)
    refresh(); root.mainloop()

if gui_available():
    run_gui()
else:
    banner("pos_billing")
    cart = Cart()
    actions = [("add", "A4 register", 3), ("add", "Gel pen", 4), ("add", "Scientific calculator", 1),
               ("add", "Gel pen", 2), ("add", "Stapler", 1), ("add", "Highlighter", 0),
               ("code", "student10", None), ("code", "FREE100", None), ("remove", "A4 register", None),
               ("add", "A4 register", 2)]
    for act, arg, n in actions:
        try:
            if act == "add": cart.add(arg, n)
            elif act == "code": cart.apply_code(arg)
            else: cart.remove(arg)
            print(f"{act:<6} {arg:<22} ok      -> total Rs {cart.totals()['total']:,}")
        except ValueError as e:
            print(f"{act:<6} {arg:<22} warning -> {e}")
    print()
    print(cart.receipt(datetime(2026, 10, 26, 11, 45)))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = list(cart.lines)
    amounts = [CATALOGUE[i] * q for i, q in cart.lines.items()]
    fig, ax = plt.subplots(figsize=(6.5, 3))
    ax.barh(names, amounts, color="#FF6B1A")
    for y, a in enumerate(amounts):
        ax.text(a + 30, y, f"Rs {a:,}", va="center", fontsize=9)
    ax.set_xlim(0, max(amounts) * 1.3); ax.set_xlabel("Line total before discount and tax (Rs)")
    ax.set_title("What the customer is paying for")
    fig.tight_layout(); fig.savefig("session-09_problem_pos_billing.png", dpi=110)
    print("\nChart saved: session-09_problem_pos_billing.png")
