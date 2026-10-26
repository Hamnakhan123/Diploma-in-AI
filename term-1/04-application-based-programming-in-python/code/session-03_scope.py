"""
Session 3 · Example 2: variable scope (LEGB) with global and nonlocal
---------------------------------------------------------------------
Run:  python session-03_scope.py
"""
course = "Diploma in AI"            # Global scope: defined at module level

def show_course():
    print("inside, reading the global:", course)      # reading is allowed

def local_demo():
    course = "local copy"           # Local: a NEW variable, hides the global
    print("inside, local:", course)

show_course(); local_demo()
print("outside, global unchanged:", course)

# Assigning to a name anywhere in a function makes it local for the WHOLE function
def broken():
    try:
        print(counter)              # Python already decided 'counter' is local
        counter = 1
    except UnboundLocalError as e:
        print("UnboundLocalError:", e)
counter = 0
broken()

# global lets a function rebind a module-level name (use sparingly)
visits = 0
def record_visit():
    global visits
    visits += 1
for _ in range(3):
    record_visit()
print("visits after 3 calls:", visits)

# Enclosing scope and nonlocal: a closure that remembers state
def make_counter(start=0):
    count = start                   # Enclosing scope for the inner function
    def increment(step=1):
        nonlocal count              # rebind the enclosing variable
        count += step
        return count
    return increment

ticket = make_counter(100)
print("tickets:", ticket(), ticket(), ticket(5))
other = make_counter()
print("independent counter:", other(), "| first counter still at:", ticket(0))

# Built-in scope: names like len and print live here; shadowing them is legal but risky
def shadow_demo():
    len = 5                         # local 'len' hides the built-in
    return len
print("shadow_demo():", shadow_demo(), "| built-in len still works outside:", len("abc"))

# LEGB lookup order demonstrated with one name defined at three levels
x = "global x"
def outer():
    x = "enclosing x"
    def inner():
        x = "local x"
        return x
    return inner(), x
print("LEGB:", outer(), "|", x)
