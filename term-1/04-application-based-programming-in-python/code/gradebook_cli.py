"""
gradebook_cli: a command-line tool built on the `school` package (Session 4 mini project).

Usage examples (run from the code/ folder):
    python gradebook_cli.py report Hira 88:4 72:3 64:3
    python gradebook_cli.py fee 15 --scholarship 50 --late
    python gradebook_cli.py grade 49 70 85
"""
import argparse
import sys

from school import fee_due, gpa, letter   # names re-exported by school/__init__.py


def parse_results(pairs):
    """Turn ['88:4', '72:3'] into [(88, 4), (72, 3)]."""
    results = []
    for p in pairs:
        mark, credits = p.split(":")
        results.append((int(mark), int(credits)))
    return results


def build_parser():
    parser = argparse.ArgumentParser(prog="gradebook", description="Grades, GPA and fees")
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("grade", help="letter grade for each mark")
    g.add_argument("marks", nargs="+", type=int)

    r = sub.add_parser("report", help="GPA from mark:credit pairs")
    r.add_argument("name")
    r.add_argument("results", nargs="+", help="e.g. 88:4 72:3")

    f = sub.add_parser("fee", help="semester fee")
    f.add_argument("credits", type=int)
    f.add_argument("--scholarship", type=float, default=0)
    f.add_argument("--late", action="store_true")
    return parser


def main(argv=None):
    """Entry point. `argv` lets tests (and notebooks) pass arguments directly."""
    args = build_parser().parse_args(argv)
    if args.command == "grade":
        for m in args.marks:
            print(f"{m:>3} -> {letter(m)}")
    elif args.command == "report":
        res = parse_results(args.results)
        print(f"{args.name}: {len(res)} courses, {sum(c for _, c in res)} credits, GPA {gpa(res):.2f}")
    elif args.command == "fee":
        print(f"Fee for {args.credits} credits: Rs {fee_due(args.credits, args.scholarship, args.late):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
