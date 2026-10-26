"""
Session 5 · Example 1: file access modes and file methods
---------------------------------------------------------
All files are created in a temporary folder that is deleted at the end,
so running the script leaves nothing behind.
Run:  python session-05_file_basics.py
"""
import os
import tempfile
from pathlib import Path

start = os.getcwd()                              # remember where we started
work = tempfile.mkdtemp()
os.chdir(work)                                   # work inside the temp folder

# 'w' write: creates the file, or EMPTIES it if it exists
with open("notes.txt", "w", encoding="utf-8") as f:   # 'with' closes the file automatically
    f.write("Line 1: Python files\n")
    f.writelines(["Line 2: modes r w a x\n", "Line 3: Urdu works too: کراچی\n"])
print("closed after with-block?", f.closed)

# 'r' read (the default): the whole file, one line, or all lines
with open("notes.txt", encoding="utf-8") as f:
    print("read():", repr(f.read(20)), "... first 20 characters")
    print("tell() after 20 chars ->", f.tell(), "bytes")
    f.seek(0)                                    # jump back to the start
    print("readline():", repr(f.readline()))
    print("readlines():", f.readlines())

# Iterate line by line: memory-friendly for huge files
with open("notes.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(f"  {number}: {line.rstrip()}")

# 'a' append: adds to the end, never erases
with open("notes.txt", "a", encoding="utf-8") as f:
    print("Line 4: appended with print(file=f)", file=f)
print("line count now:", sum(1 for _ in open("notes.txt", encoding="utf-8")))

# 'x' exclusive create: fails if the file already exists (safe against overwriting)
try:
    open("notes.txt", "x")
except FileExistsError as e:
    print("mode 'x':", type(e).__name__, "-", e.strerror)

# 'r+' read and write without truncating
with open("notes.txt", "r+", encoding="utf-8") as f:
    f.write("LINE")                              # overwrites the first 4 characters
    f.seek(0)
    print("after r+:", f.readline().rstrip())

# Binary mode 'rb' / 'wb': bytes, not text (images, PDFs, pickles)
with open("pixel.bin", "wb") as f:
    f.write(bytes([255, 107, 26]))               # the RGB colour #FF6B1A
with open("pixel.bin", "rb") as f:
    data = f.read()
print("binary:", data, "->", list(data), "| size", os.path.getsize("pixel.bin"), "bytes")

# pathlib: the modern, object-oriented way to work with paths
p = Path("reports") / "2026" / "october.txt"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("Total: 42\n", encoding="utf-8")
print("pathlib:", p, "| exists:", p.exists(), "| suffix:", p.suffix, "| stem:", p.stem,
      "| text:", p.read_text(encoding="utf-8").strip())
print("all .txt files:", sorted(str(x) for x in Path(".").rglob("*.txt")))

# Rename and delete
os.rename("notes.txt", "notes_old.txt")
os.remove("pixel.bin")
print("folder now:", sorted(os.listdir(".")))

import shutil
os.chdir(start); shutil.rmtree(work)             # go back, then delete the demo folder
print("cleaned up:", not os.path.exists(work))
