"""
Session 2 · Example 2: Bayes' theorem in medicine and spam filtering
-------------------------------------------------------------------
Bayes' theorem turns P(evidence | cause) into P(cause | evidence):

        P(H | E) = P(E | H) * P(H) / P(E)
        P(E)     = P(E | H) P(H) + P(E | not H) P(not H)     (total probability)

Part 1 solves the classic 'positive test' puzzle with the formula AND with a
table of 100,000 imaginary people (natural frequencies).
Part 2 trains a tiny word-based spam filter (naive Bayes) on 8 messages.

Run:  python session-02_bayes.py
"""
from collections import Counter
import math

# ---------------- Part 1: a screening test -------------------------------------------
prevalence = 0.01        # P(disease): 1 in 100 people has it
sensitivity = 0.95       # P(positive | disease)
specificity = 0.90       # P(negative | healthy) -> false-positive rate 0.10

p_pos = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
p_disease_given_pos = sensitivity * prevalence / p_pos
print("Screening test")
print(f"  P(positive)           = {p_pos:.4f}")
print(f"  P(disease | positive) = {p_disease_given_pos:.4f}  <- only about 9 %!")

# Natural frequencies: the same answer with counting, which most people find intuitive
N = 100_000
sick = N * prevalence
true_pos = sick * sensitivity
false_pos = (N - sick) * (1 - specificity)
print(f"  Of {N:,} people: {sick:,.0f} sick -> {true_pos:,.0f} test positive; "
      f"{N - sick:,.0f} healthy -> {false_pos:,.0f} false alarms")
print(f"  {true_pos:,.0f} / ({true_pos:,.0f} + {false_pos:,.0f}) = {true_pos / (true_pos + false_pos):.4f}")

# A second, independent positive test: yesterday's posterior becomes today's prior
prior = p_disease_given_pos
p_pos2 = sensitivity * prior + (1 - specificity) * (1 - prior)
print(f"  After a SECOND positive test: P(disease) = {sensitivity * prior / p_pos2:.4f}")

# ---------------- Part 2: a naive Bayes spam filter ----------------------------------
train = [
    ("win a free prize now", "spam"), ("free cash offer click now", "spam"),
    ("claim your free reward", "spam"), ("cheap loan offer now", "spam"),
    ("meeting moved to monday", "ham"), ("please send the lab report", "ham"),
    ("lunch at the cafe on monday", "ham"), ("your assignment marks are out", "ham"),
]
classes = Counter(label for _, label in train)
words = {c: Counter() for c in classes}
for text, label in train:
    words[label].update(text.split())
vocab = {w for c in words for w in words[c]}

def log_posterior(text, c):
    """log P(c) + sum log P(word | c), with Laplace (+1) smoothing for unseen words."""
    total = sum(words[c].values())
    lp = math.log(classes[c] / len(train))
    for w in text.split():
        lp += math.log((words[c][w] + 1) / (total + len(vocab)))
    return lp

print("\nNaive Bayes spam filter")
for msg in ["free prize offer", "lab report on monday", "click now for cheap marks"]:
    scores = {c: log_posterior(msg, c) for c in classes}
    # convert log scores back to probabilities that sum to 1
    m = max(scores.values())
    exp = {c: math.exp(s - m) for c, s in scores.items()}
    p_spam = exp["spam"] / sum(exp.values())
    print(f"  {msg!r:<30} P(spam) = {p_spam:.3f} -> {'SPAM' if p_spam > 0.5 else 'ham'}")
