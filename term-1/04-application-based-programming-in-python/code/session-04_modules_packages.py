"""
Session 4 · Example 3: using modules and packages
-------------------------------------------------
Needs campus_utils.py and the school/ folder next to this file (both are in code/).
Run:  python session-04_modules_packages.py
"""
import math                                # 1. whole standard-library module
import random as rnd                       # 2. module with an alias
from datetime import date                  # 3. one name from a module
from statistics import mean, median        # 4. several names

print("math.floor(7.8) =", math.floor(7.8), "| rnd seeded pick:", rnd.Random(1).choice(["red", "green", "blue"]))
print("days until 1 Jan 2027 from 26 Oct 2026:", (date(2027, 1, 1) - date(2026, 10, 26)).days)
print("mean/median:", mean([3, 5, 10]), median([3, 5, 10]))

# Our own module (campus_utils.py in the same folder)
import campus_utils
print("\ncampus_utils.grade(77) =", campus_utils.grade(77), "| PASS_MARK =", campus_utils.PASS_MARK)
print("module __name__ when imported:", campus_utils.__name__)
print("public names:", [n for n in dir(campus_utils) if not n.startswith("_")])

from campus_utils import percentage as pct
print("pct(45, 60) =", pct(45, 60))

# Our own package (school/ folder with __init__.py)
import school
from school import report_card
from school.grades import POINTS            # dotted path into a sub-module
print("\nschool version:", school.__version__, "| exported:", school.__all__)
print("grade points:", POINTS)
results = {"Programming Fundamentals": (88, 4), "Statistics": (72, 3),
           "Database Systems": (64, 3), "Communication Skills": (91, 2)}
print(report_card("Hamza Raza", results, scholarship_pct=25))

# Where Python looks for modules: the script folder first, then sys.path entries
import sys
import os
print("\nsys.path has", "many" if len(sys.path) > 3 else "few", "entries; campus_utils.py found in the current folder:", os.path.exists("campus_utils.py"))
print("modules already loaded include math and school:", "math" in sys.modules, "school" in sys.modules)
print("this file's __name__:", __name__)
