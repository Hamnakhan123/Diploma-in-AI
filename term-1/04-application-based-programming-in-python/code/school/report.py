"""school.report: builds a text report card using the sibling modules."""
from .grades import letter, gpa        # relative import: '.' means 'this package'
from .fees import fee_due

def report_card(name, results, scholarship_pct=0):
    """Return a multi-line report card string."""
    lines = [f"Report card: {name}"]
    for course, (mark, credits) in results.items():
        lines.append(f"  {course:<26} {mark:>3}  {letter(mark)}  ({credits} cr)")
    credits = sum(c for _, c in results.values())
    lines.append(f"  GPA {gpa(list(results.values())):.2f} | fee due Rs {fee_due(credits, scholarship_pct):,}")
    return "\n".join(lines)
