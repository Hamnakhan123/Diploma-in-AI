"""
Session 4 · Mini project: a gradebook command-line tool built from a package
---------------------------------------------------------------------------
Files involved (all in code/):
  school/__init__.py, grades.py, fees.py, report.py   <- the package
  gradebook_cli.py                                    <- the CLI module with main()
This script imports the CLI module and calls main() with different argument
lists, exactly as if you had typed the commands in a terminal.
Run:  python session-04_project_gradebook.py
"""
import contextlib
import sys

import gradebook_cli

commands = [
    ["grade", "49", "70", "85", "93"],
    ["report", "Hira", "88:4", "72:3", "64:3", "91:2"],
    ["fee", "15"],
    ["fee", "15", "--scholarship", "50", "--late"],
]
for argv in commands:
    print("$ python gradebook_cli.py", " ".join(argv))
    gradebook_cli.main(argv)
    print()

# argparse also generates help text and error messages for free
print("$ python gradebook_cli.py fee --help")
try:
    gradebook_cli.main(["fee", "--help"])
except SystemExit:
    pass                      # argparse exits after printing help
print("\n$ python gradebook_cli.py fee lots")
try:
    with contextlib.redirect_stderr(sys.stdout):   # show argparse's error message in normal output
        gradebook_cli.main(["fee", "lots"])
except SystemExit as e:
    print("(exit code", e.code, ")")
