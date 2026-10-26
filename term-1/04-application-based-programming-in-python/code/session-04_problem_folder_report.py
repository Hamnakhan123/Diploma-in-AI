"""
Session 4 · Real-life problem: recursive folder-size report
-----------------------------------------------------------
PROBLEM
A lab's shared drive is full. The admin wants a report that
  1. walks a folder and ALL its sub-folders,
  2. prints an indented tree with each folder's total size,
  3. lists the 3 largest files and the size per file type.
Folders contain folders, so the natural solution is RECURSIVE: the size of a
folder = sizes of its files + sizes of its sub-folders (same problem, smaller).

To keep the output identical on every machine, the script first builds a small
demo tree with known file sizes inside a temporary directory.
Run:  python session-04_problem_folder_report.py
"""
import os
import tempfile
from collections import defaultdict

def make_demo_tree(root):
    """Create folders and files of fixed sizes (bytes) for the demo."""
    layout = {
        "lectures/week1/slides.pdf": 2_400_000, "lectures/week1/notes.md": 18_000,
        "lectures/week2/slides.pdf": 3_100_000, "lectures/week2/demo.py": 6_500,
        "datasets/students.csv": 950_000, "datasets/raw/survey_2025.csv": 4_800_000,
        "datasets/raw/images/cat.png": 1_200_000, "datasets/raw/images/dog.png": 1_350_000,
        "submissions/ali.py": 4_200, "submissions/sana.py": 5_100, "README.md": 2_000,
    }
    for rel, size in layout.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(b"\0" * size)

def human(n):
    """Readable size: 1_234_567 -> '1.2 MB'."""
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1000:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1000
    return f"{n:.1f} TB"

def folder_size(path, depth=0, lines=None, files=None):
    """RECURSIVE: return total bytes under `path`, recording tree lines and files."""
    total = 0
    child_lines = []
    for entry in sorted(os.scandir(path), key=lambda e: (e.is_file(), e.name)):
        if entry.is_dir():
            total += folder_size(entry.path, depth + 1, child_lines, files)   # recursive case
        else:                                                               # base case: a file
            size = entry.stat().st_size
            total += size
            files.append((entry.name, size))
    lines.append(("    " * depth + os.path.basename(path) + "/", total))
    lines.extend(child_lines)
    return total

with tempfile.TemporaryDirectory() as tmp:
    root = os.path.join(tmp, "shared_drive")
    make_demo_tree(root)
    lines, files = [], []
    grand = folder_size(root, 0, lines, files)

print("Folder tree (total size of each folder)")
for text, size in lines:
    print(f"  {text:<28} {human(size):>9}")

print("\nThree largest files")
for name, size in sorted(files, key=lambda f: f[1], reverse=True)[:3]:
    print(f"  {name:<18} {human(size):>9}  ({size / grand:.0%} of the drive)")

by_type = defaultdict(int)
for name, size in files:
    by_type[os.path.splitext(name)[1]] += size
print("\nSize by file type")
for ext, size in sorted(by_type.items(), key=lambda kv: -kv[1]):
    print(f"  {ext:<5} {human(size):>9} {'#' * round(size / grand * 40)}")
print(f"\n{len(files)} files, {human(grand)} in total")
