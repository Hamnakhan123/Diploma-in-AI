"""
Session 9 · Example 3: grid layout, events and key bindings - a calculator
--------------------------------------------------------------------------
Shows the grid geometry manager (rows/columns, columnspan, sticky), button
commands built with lambda, and keyboard events bound with root.bind().
Run:  python session-09_layout_and_events.py
"""
from gui_support import gui_available, banner

class CalculatorEngine:
    """All calculator behaviour lives here; the GUI only forwards key presses."""
    ALLOWED = set("0123456789+-*/.()")
    def __init__(self):
        self.expr = ""
    def press(self, key):
        if key == "C":
            self.expr = ""
        elif key == "<-":
            self.expr = self.expr[:-1]
        elif key == "=":
            self.expr = self.evaluate()
        elif key in self.ALLOWED:
            if self.expr == "Error":
                self.expr = ""
            self.expr += key
        return self.expr or "0"
    def evaluate(self):
        if not self.expr or not set(self.expr) <= self.ALLOWED:      # never eval arbitrary text
            return ""
        try:
            value = eval(self.expr, {"__builtins__": {}}, {})          # only digits and operators reach here
            return str(round(value, 10)).rstrip("0").rstrip(".") if isinstance(value, float) else str(value)
        except (SyntaxError, ZeroDivisionError):
            return "Error"

LAYOUT = [["7", "8", "9", "/"],
          ["4", "5", "6", "*"],
          ["1", "2", "3", "-"],
          ["0", ".", "=", "+"],
          ["(", ")", "<-", "C"]]

def run_gui():
    import tkinter as tk
    engine = CalculatorEngine()
    root = tk.Tk(); root.title("Calculator")
    display = tk.StringVar(value="0")
    tk.Label(root, textvariable=display, anchor="e", font=("Consolas", 20), bg="#0A0716", fg="#FCD34D",
             padx=10).grid(row=0, column=0, columnspan=4, sticky="nsew")
    for r, row in enumerate(LAYOUT, start=1):
        for c, key in enumerate(row):
            tk.Button(root, text=key, font=("Segoe UI", 14), width=4,
                      command=lambda k=key: display.set(engine.press(k))   # k=key avoids late binding
                      ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
    for i in range(4):
        root.columnconfigure(i, weight=1)                # columns stretch when resized
    def on_key(event):                                   # event object: .char, .keysym, .x, .y ...
        mapping = {"Return": "=", "BackSpace": "<-", "Escape": "C"}
        key = mapping.get(event.keysym, event.char)
        display.set(engine.press(key))
    root.bind("<Key>", on_key)
    root.mainloop()

if gui_available():
    run_gui()
else:
    banner("calculator")
    eng = CalculatorEngine()
    def type_keys(keys):
        shown = ""
        for k in keys:
            shown = eng.press(k)
        return shown
    for seq in [list("12+7*3") + ["="], ["C"] + list("(12+7)*3") + ["="], ["C"] + list("10/4") + ["="],
                ["C"] + list("9/0") + ["="], ["C"] + list("123") + ["<-", "<-"], ["C"] + list("2**3") + ["="],
                ["C", "a", "b", "5"]]:
        print(f"keys {' '.join(seq):<36} display -> {type_keys(seq)}")
    print("\nGrid plan (row, column) for the buttons:")
    for r, row in enumerate(LAYOUT, start=1):
        print("  " + "  ".join(f"[{k:>2}]({r},{c})" for c, k in enumerate(row)))
