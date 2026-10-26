"""
Session 11 · Mini project: an automated class performance report
----------------------------------------------------------------
Inputs (three tables, as a department would really have them):
  students   - roll, name, section
  marks      - long format: one row per (roll, subject, assessment, score)
  attendance - roll, classes_attended (out of 40)
The report:
  1. reshapes marks from long to wide with pivot_table,
  2. computes weighted totals (quiz 20 %, midterm 30 %, final 50 %),
  3. merges attendance, assigns grades with pd.cut, flags students at risk,
  4. summarises by section and subject, and exports report.csv,
  5. draws grade-distribution and section-comparison charts.
Run:  python session-11_project_student_report.py
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
rng = np.random.default_rng(2026)
names = ["Ayesha", "Omar", "Hira", "Bilal", "Zainab", "Danish", "Mehwish", "Usman", "Sara", "Hamza",
         "Iqra", "Fahad", "Noor", "Saad", "Anum", "Taha"]
students = pd.DataFrame({"roll": [f"AI-{i:02d}" for i in range(1, 17)], "name": names,
                         "section": ["A"] * 8 + ["B"] * 8})
subjects, weights = ["Python", "Statistics", "Databases"], {"quiz": 0.2, "midterm": 0.3, "final": 0.5}
ability = dict(zip(students["roll"], rng.normal(70, 12, len(students))))
rows = [(r, s, a, float(np.clip(ability[r] + rng.normal(0, 8), 20, 100)))
        for r in students["roll"] for s in subjects for a in weights]
marks = pd.DataFrame(rows, columns=["roll", "subject", "assessment", "score"]).round(0)
# attendance loosely follows ability (students who attend tend to score better), plus noise
attended = [int(np.clip(round(14 + 0.28 * ability[r] + rng.normal(0, 3)), 20, 40)) for r in students["roll"]]
attendance = pd.DataFrame({"roll": students["roll"], "attended": attended})
print("marks table (long format):", marks.shape, "\n", marks.head(4).to_string(index=False))

# 1. long -> wide: one row per student and subject, assessments as columns
wide = marks.pivot_table(index=["roll", "subject"], columns="assessment", values="score").reset_index()
wide["total"] = sum(wide[a] * w for a, w in weights.items())

# 2. one row per student: subjects as columns + overall average
per_student = wide.pivot_table(index="roll", columns="subject", values="total").round(1)
per_student["average"] = per_student[subjects].mean(axis=1).round(1)

# 3. merge names, sections and attendance
report = (students.merge(per_student.reset_index(), on="roll")
                  .merge(attendance, on="roll"))
report["attendance_%"] = (report["attended"] / 40 * 100).round(0)
report["grade"] = pd.cut(report["average"], bins=[0, 50, 55, 70, 85, 100], labels=["F", "D", "C", "B", "A"], right=False)
report["at_risk"] = (report["average"] < 55) | (report["attendance_%"] < 75)
report = report.sort_values("average", ascending=False).reset_index(drop=True)
report.index += 1                                            # rank starting at 1
print("\nClass report (ranked):\n", report.drop(columns=["attended"]).to_string())

# 4. summaries
print("\nSection summary:\n", report.groupby("section").agg(students=("roll", "count"),
      mean_avg=("average", "mean"), best=("average", "max"), at_risk=("at_risk", "sum")).round(1))
print("\nSubject means by section:\n", report.groupby("section")[subjects].mean().round(1))
print("\nGrade distribution:", report["grade"].value_counts().reindex(list("ABCDF")).to_dict())
print("Students at risk:", report.loc[report["at_risk"], ["name", "average", "attendance_%"]].to_dict("records"))
corr = report["attendance_%"].corr(report["average"])
print(f"Correlation between attendance and average: r = {corr:.2f}")

report.to_csv("report.csv", index_label="rank")
print("\nExported report.csv")

# 5. charts
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
counts = report["grade"].value_counts().reindex(list("ABCDF"), fill_value=0)
a1.bar(counts.index, counts.values, color=["#FF6B1A", "#FCD34D", "#A78BFA", "#F43F5E", "#6B7280"])
a1.set_title("Grade distribution"); a1.set_ylabel("students")
report.boxplot(column="average", by="section", ax=a2, grid=False)
a2.set_title("Average mark by section"); a2.set_xlabel("section"); fig.suptitle("")
fig.tight_layout(); fig.savefig("session-11_project_student_report.png", dpi=110)
print("Chart saved: session-11_project_student_report.png")
