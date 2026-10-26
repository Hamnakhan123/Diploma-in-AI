"""
Session 14 · Real-life problem: an early-warning system for student dropout
---------------------------------------------------------------------------
PROBLEM
A diploma program loses students every term. Using last year's records,
build a SUPERVISED classifier that flags students at risk after week 4, so
advisers can contact them early. Requirements:
  1. features known by week 4 only (attendance, quiz average, assignments
     submitted, commute time, works part-time, fee instalment late),
  2. logistic regression inside a pipeline (scaling), evaluated on a test set,
  3. explain the model with odds ratios that advisers can understand,
  4. pick a probability threshold: missing an at-risk student is worse than
     an extra phone call, so we trade precision for recall,
  5. output a ranked contact list for the new cohort, plus a chart.
Data is synthetic (seeded).
Run:  python session-14_problem_dropout_warning.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(404)
def make_students(n):
    df = pd.DataFrame({
        "attendance_pct": np.clip(rng.normal(80, 12, n), 30, 100).round(0),
        "quiz_avg": np.clip(rng.normal(65, 15, n), 0, 100).round(0),
        "assignments_done": rng.integers(0, 5, n),                 # out of 4 by week 4
        "commute_min": rng.gamma(3, 15, n).round(0),
        "works_part_time": rng.integers(0, 2, n),
        "fee_late": (rng.random(n) < 0.2).astype(int),
    })
    z = (2.0 - 0.07 * (df.attendance_pct - 80) - 0.04 * (df.quiz_avg - 65) - 0.6 * df.assignments_done
         + 0.015 * df.commute_min + 0.7 * df.works_part_time + 1.2 * df.fee_late - 3.1)
    df["dropped_out"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return df

hist = make_students(900)
features = [c for c in hist.columns if c != "dropped_out"]
print(f"last year: {len(hist)} students, dropout rate {hist.dropped_out.mean():.1%}")
X_tr, X_te, y_tr, y_te = train_test_split(hist[features], hist["dropped_out"], test_size=0.3,
                                          stratify=hist["dropped_out"], random_state=1)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]
print(f"test ROC-AUC: {roc_auc_score(y_te, proba):.3f} (0.5 = guessing, 1.0 = perfect ranking)")

# Explain: refit on unscaled data so each odds ratio is "per 1 unit" of the original feature
plain = LogisticRegression(max_iter=2000).fit(X_tr, y_tr)
odds = pd.Series(np.exp(plain.coef_[0]), index=features)
units = {"attendance_pct": "+1 % attendance", "quiz_avg": "+1 quiz mark", "assignments_done": "+1 assignment",
         "commute_min": "+1 min commute", "works_part_time": "has a part-time job", "fee_late": "fee paid late"}
print("\nOdds ratios (how the odds of dropping out change):")
for f, o in odds.sort_values().items():
    print(f"  {units[f]:<22} x{o:5.2f}  ({'lower' if o < 1 else 'higher'} risk)")

print("\nThreshold trade-off on the test set:")
print(f"  {'threshold':>9} {'flagged':>8} {'recall':>7} {'precision':>9}")
rows = []
for t in [0.5, 0.4, 0.3, 0.2]:
    pred = (proba >= t).astype(int)
    rows.append((t, pred.sum(), recall_score(y_te, pred), precision_score(y_te, pred)))
    print(f"  {t:>9.1f} {pred.sum():>8} {rows[-1][2]:>7.2f} {rows[-1][3]:>9.2f}")
chosen = 0.3
t, flagged, rec, prec = next(r for r in rows if r[0] == chosen)
print(f"chosen threshold {chosen}: catches {rec:.0%} of real dropouts while calling {flagged / len(y_te):.0%} of students")

cohort = make_students(20).drop(columns="dropped_out")
cohort.insert(0, "student", [f"New-{i:02d}" for i in range(1, 21)])
cohort["risk"] = model.predict_proba(cohort[features])[:, 1].round(2)
contact = cohort[cohort["risk"] >= chosen].sort_values("risk", ascending=False)
print(f"\nContact list for the new cohort ({len(contact)} of {len(cohort)} students):")
print(contact[["student", "attendance_pct", "quiz_avg", "assignments_done", "fee_late", "risk"]].to_string(index=False))

fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
ax[0].barh([units[f] for f in odds.sort_values().index], odds.sort_values().values,
           color=["#FF6B1A" if o < 1 else "#F43F5E" for o in odds.sort_values().values])
ax[0].axvline(1, color="black", lw=1); ax[0].set_xscale("log"); ax[0].set_title("Odds ratios (log scale; 1 = no effect)")
ts = [r[0] for r in rows]
ax[1].plot(ts, [r[2] for r in rows], "o-", color="#FF6B1A", label="recall")
ax[1].plot(ts, [r[3] for r in rows], "s-", color="#A78BFA", label="precision")
ax[1].invert_xaxis(); ax[1].set_xlabel("probability threshold"); ax[1].legend(); ax[1].set_title("Lower threshold: more caught, more false alarms")
fig.tight_layout(); fig.savefig("session-14_problem_dropout_warning.png", dpi=100)
print("Saved session-14_problem_dropout_warning.png")
