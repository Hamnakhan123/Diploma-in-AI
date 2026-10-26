"""
gui_support: decides whether a Tkinter window can be shown (Session 9).

Tkinter needs a screen. On your laptop the examples open real windows.
In Google Colab, on servers, inside notebooks or with --test, there is no
screen to draw on, so the examples run their application LOGIC in a text
"test mode" instead. Keeping logic separate from widgets is good design anyway.
"""
import sys

def gui_available():
    """True when a Tk window can actually be created."""
    if "--test" in sys.argv or "ipykernel" in sys.modules:   # notebooks and test runs: no window
        return False
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:                 # no display, or Tk libraries not installed
        return False

def banner(name):
    print(f"[{name}] no screen available here -> running the app logic in test mode.")
    print("Run this file on your own computer (python <file>.py) to see the window.\n")
