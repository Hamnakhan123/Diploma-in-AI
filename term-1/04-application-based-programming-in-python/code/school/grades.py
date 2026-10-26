"""school.grades: grading rules."""
POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

def letter(mark):
    """Letter grade for a mark out of 100."""
    for cut, g in [(85, "A"), (70, "B"), (55, "C"), (50, "D")]:
        if mark >= cut:
            return g
    return "F"

def gpa(results):
    """Credit-weighted GPA from a list of (mark, credit_hours)."""
    total_credits = sum(c for _, c in results)
    points = sum(POINTS[letter(m)] * c for m, c in results)
    return round(points / total_credits, 2)
