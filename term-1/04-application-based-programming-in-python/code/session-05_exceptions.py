"""
Session 5 · Example 3: exception handling
-----------------------------------------
Run:  python session-05_exceptions.py
"""
# 1. Some common built-in exceptions, triggered on purpose
tests = {
    "ZeroDivisionError": lambda: 10 / 0,
    "ValueError": lambda: int("abc"),
    "TypeError": lambda: "5" + 5,
    "IndexError": lambda: [1, 2, 3][10],
    "KeyError": lambda: {"a": 1}["b"],
    "FileNotFoundError": lambda: open("no_such_file.txt"),
    "AttributeError": lambda: "text".push("x"),
    "NameError": lambda: undefined_variable,      # noqa: F821
}
for name, fn in tests.items():
    try:
        fn()
    except Exception as e:                           # catch, then report the class name
        print(f"  {type(e).__name__:18} {e}")

# 2. try / except / else / finally
def read_number(text):
    try:
        value = float(text)
    except ValueError:
        print(f"  {text!r}: not a number")
        return None
    else:                                            # runs only if NO exception happened
        print(f"  {text!r}: ok -> {value}")
        return value
    finally:                                         # ALWAYS runs (cleanup)
        print("    (finally: checked", repr(text) + ")")
for t in ["42.5", "forty"]:
    read_number(t)

# 3. Several except blocks: the first matching one wins, so specific before general
def safe_ratio(a, b):
    try:
        return round(a / b, 2)
    except ZeroDivisionError:
        return "cannot divide by zero"
    except TypeError:
        return "numbers only"
    except Exception as e:                           # last resort
        return f"unexpected: {e}"
print("safe_ratio:", safe_ratio(7, 2), "|", safe_ratio(7, 0), "|", safe_ratio("7", 2))

# 4. Catch several types in one block with a tuple
for raw in ["12", "x", None]:
    try:
        print("  doubled:", int(raw) * 2)
    except (ValueError, TypeError) as e:
        print("  bad input", repr(raw), "->", type(e).__name__)

# 5. raise: signal an error yourself
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be an int")
    if not 0 <= age <= 120:
        raise ValueError(f"age {age} is out of range 0-120")
    return age
for a in [25, 150, "20"]:
    try:
        print("  age set:", set_age(a))
    except (TypeError, ValueError) as e:
        print("  rejected:", e)

# 6. Custom exceptions: a class that inherits from Exception
class InsufficientFundsError(Exception):
    """Raised when a withdrawal is bigger than the balance."""
    def __init__(self, balance, amount):
        super().__init__(f"balance Rs {balance:,} is less than Rs {amount:,}")
        self.shortfall = amount - balance

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount
try:
    withdraw(3_000, 5_000)
except InsufficientFundsError as e:
    print("custom:", e, "| shortfall:", e.shortfall)

# 7. Re-raising with context: 'raise ... from ...' keeps the original cause
def load_price(text):
    try:
        return float(text)
    except ValueError as e:
        raise RuntimeError("price file is corrupt") from e
try:
    load_price("12,50")
except RuntimeError as e:
    print("chained:", e, "| caused by:", repr(e.__cause__))

# 8. assert for internal sanity checks (can be disabled with python -O)
def average(values):
    assert len(values) > 0, "average() needs at least one value"
    return sum(values) / len(values)
try:
    average([])
except AssertionError as e:
    print("assert:", e)

# 9. The exception hierarchy decides what an except clause catches
print("FileNotFoundError is an OSError?", issubclass(FileNotFoundError, OSError))
print("KeyError and IndexError share the base:", KeyError.__mro__[1].__name__)
