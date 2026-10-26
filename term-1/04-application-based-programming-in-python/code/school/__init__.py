"""
school: a small PACKAGE (a folder of modules with an __init__.py).

The __init__.py runs once when the package is first imported. Here it
re-exports the most useful names so users can write `from school import report_card`.
"""
from .grades import letter, gpa
from .fees import fee_due
from .report import report_card

__all__ = ["letter", "gpa", "fee_due", "report_card"]
__version__ = "1.0.0"
