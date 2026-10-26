"""
Session 9 · Example 1: your first Tkinter window
------------------------------------------------
Every Tkinter program follows the same five steps:
  1. import tkinter   2. create the root window   3. create widgets
  4. place them with a geometry manager             5. start the event loop
Run:  python session-09_first_window.py
"""
from gui_support import gui_available, banner

class ClickCounter:
    """The app's logic, kept separate from the widgets so it can be tested."""
    def __init__(self):
        self.count = 0
    def click(self):
        self.count += 1
        return self.message()
    def reset(self):
        self.count = 0
        return self.message()
    def message(self):
        if self.count == 0:
            return "Click the button!"
        return f"Clicked {self.count} time{'s' if self.count != 1 else ''}" + (" - nice!" if self.count >= 5 else "")

def run_gui():
    import tkinter as tk                       # step 1
    counter = ClickCounter()
    root = tk.Tk()                             # step 2: the main window
    root.title("My first Tkinter app")
    root.geometry("320x160")                   # width x height in pixels
    root.resizable(False, False)

    label = tk.Label(root, text=counter.message(), font=("Segoe UI", 14), fg="#FF6B1A")   # step 3
    def on_click():                            # a callback: runs when the button is pressed
        label.config(text=counter.click())     # change a widget property at run time
    button = tk.Button(root, text="Click me", width=12, command=on_click)
    reset = tk.Button(root, text="Reset", command=lambda: label.config(text=counter.reset()))
    quit_btn = tk.Button(root, text="Quit", command=root.destroy)

    label.pack(pady=15)                        # step 4: pack stacks widgets top to bottom
    button.pack()
    reset.pack(side="left", padx=40, pady=10)
    quit_btn.pack(side="right", padx=40, pady=10)
    root.mainloop()                            # step 5: wait for events until the window closes

if gui_available():
    run_gui()
else:
    banner("first_window")
    c = ClickCounter()
    print("start      ->", c.message())
    for _ in range(5):
        print("click      ->", c.click())
    print("reset      ->", c.reset())
    print("\nWidgets this window creates: Tk (root), Label, Button x3")
    print("Geometry manager: pack | Event loop: root.mainloop()")
