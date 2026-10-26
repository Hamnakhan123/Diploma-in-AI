"""
campus_utils: a small MODULE used in Session 4.

A module is simply a .py file. Anything defined here (functions, constants,
classes) can be imported by another file in the same folder.
"""
PASS_MARK = 50
GRADE_CUTS = [(85, "A"), (70, "B"), (55, "C"), (PASS_MARK, "D")]

def grade(mark):
    """Return the letter grade for a mark out of 100."""
    for cut, letter in GRADE_CUTS:
        if mark >= cut:
            return letter
    return "F"

def percentage(obtained, total):
    """Return a percentage rounded to one decimal place."""
    return round(obtained / total * 100, 1)

def _internal_helper():
    """A leading underscore means 'private': not imported by 'from ... import *'."""
    return "hidden"

# This block runs ONLY when the file is executed directly (python campus_utils.py),
# not when it is imported. Use it for quick self-tests.
if __name__ == "__main__":
    print("Self-test:", grade(91), grade(49), percentage(45, 60))
