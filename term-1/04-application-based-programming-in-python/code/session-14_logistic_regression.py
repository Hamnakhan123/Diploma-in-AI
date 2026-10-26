"""
Session 14 · Example 1: supervised learning - logistic regression for classification
------------------------------------------------------------------------------------
Question: from hours studied, can we predict whether a student passes?
Logistic regression outputs a PROBABILITY with the sigmoid function
    p = 1 / (1 + e^-(b0 + b1*x))
and predicts "pass" when p >= 0.5.
Run:  python session-14_logistic_regression.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, classification_report
from sklearn.model_selection import train_test_split

def sigmoid(z):
    return 1 / (1 + np.exp(-z))
print("sigmoid squashes any number into (0, 1):", {z: round(float(sigmoid(z)), 3) for z in (-6, -2, 0, 2, 6)})

rng = np.random.default_rng(14)
hours = rng.uniform(0, 12, 200).round(1)
passed = (rng.random(200) < sigmoid(1.1 * (hours - 5.5))).astype(int)      # the hidden 'true' rule
X = hours.reshape(-1, 1)                                                   # scikit-learn wants a 2-D X
X_train, X_test, y_train, y_test = train_test_split(X, passed, test_size=0.25, random_state=0, stratify=passed)

model = LogisticRegression()
model.fit(X_train, y_train)                                                # learn b0 and b1
b0, b1 = model.intercept_[0], model.coef_[0, 0]
print(f"\nlearned: b0 = {b0:.2f}, b1 = {b1:.2f}  -> 50 % chance at {-b0 / b1:.1f} hours")
print(f"each extra hour multiplies the odds of passing by e^b1 = {np.exp(b1):.2f}")

for h in [2, 5, 6, 9]:
    p = model.predict_proba([[h]])[0, 1]
    print(f"  {h:>2} hours -> P(pass) = {p:.2f} -> predict {'pass' if p >= 0.5 else 'fail'}")

pred = model.predict(X_test)
print("\naccuracy :", round(accuracy_score(y_test, pred), 3))
print("precision:", round(precision_score(y_test, pred), 3), "(of predicted passes, how many really passed)")
print("recall   :", round(recall_score(y_test, pred), 3), "(of real passes, how many we caught)")
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(f"confusion matrix: TN={tn} FP={fp} FN={fn} TP={tp}")
print(classification_report(y_test, pred, target_names=["fail", "pass"]))

xs = np.linspace(0, 12, 200).reshape(-1, 1)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.scatter(hours, passed + rng.normal(0, 0.02, 200), s=12, alpha=0.5, color="#A78BFA", label="students (0 = fail, 1 = pass)")
ax.plot(xs, model.predict_proba(xs)[:, 1], color="#FF6B1A", lw=2.5, label="P(pass) from the model")
ax.axhline(0.5, color="gray", ls=":"); ax.axvline(-b0 / b1, color="#F43F5E", ls="--", label="decision boundary")
ax.set_xlabel("hours studied per week"); ax.set_ylabel("probability of passing"); ax.legend(fontsize=8)
ax.set_title("Logistic regression turns a score into a probability")
fig.tight_layout(); fig.savefig("session-14_logistic_regression.png", dpi=100)
print("Saved session-14_logistic_regression.png")
