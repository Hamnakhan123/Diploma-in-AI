"""
Session 4 · Example 3: The hypothesis-testing procedure, step by step
--------------------------------------------------------------------
A juice factory claims each bottle holds 500 ml. An inspector measures 15
bottles. Is the true mean different from 500 ml?  (two-tailed one-sample t test)

Then we SIMULATE:
  * Type I error rate  - how often we wrongly reject a TRUE H0 at alpha = 0.05
  * Power              - how often we correctly reject a FALSE H0, for several n

Run:  python session-04_hypothesis_test.py
"""
import numpy as np
from scipy import stats

ml = np.array([497.2, 499.1, 495.8, 498.4, 500.3, 496.9, 497.7, 499.6,
               494.9, 498.1, 497.4, 501.0, 496.2, 498.8, 497.5])
mu0, alpha = 500, 0.05

print("Step 1. Hypotheses:  H0: mu = 500 ml    H1: mu != 500 ml   (two-tailed)")
print(f"Step 2. Significance level alpha = {alpha}")
n, xbar, s = len(ml), ml.mean(), ml.std(ddof=1)
se = s / np.sqrt(n)
t = (xbar - mu0) / se
print(f"Step 3. Test statistic: t = (x_bar - mu0) / (s / sqrt(n)) = ({xbar:.3f} - {mu0}) / {se:.4f} = {t:.3f}")
crit = stats.t.ppf(1 - alpha / 2, n - 1)
p = 2 * stats.t.sf(abs(t), n - 1)
print(f"Step 4. Critical values +/-{crit:.3f} (df = {n - 1});  p-value = {p:.5f}")
decision = "REJECT H0" if p < alpha else "FAIL TO REJECT H0"
print(f"Step 5. Decision: |t| = {abs(t):.2f} {'>' if abs(t) > crit else '<='} {crit:.2f} and p "
      f"{'<' if p < alpha else '>='} {alpha} -> {decision}")
print("Step 6. Conclusion: the bottles hold less than the labelled 500 ml on average." if p < alpha
      else "Step 6. Conclusion: no evidence the mean differs from 500 ml.")
res = stats.ttest_1samp(ml, mu0)
print(f"Check with scipy: t = {res.statistic:.3f}, p = {res.pvalue:.5f}")
lo, hi = stats.t.interval(0.95, n - 1, loc=xbar, scale=se)
print(f"95% CI [{lo:.2f}, {hi:.2f}] does not contain 500 -> same decision as the test" if not lo <= 500 <= hi
      else f"95% CI [{lo:.2f}, {hi:.2f}] contains 500")

# One-tailed version: consumer group suspects UNDER-filling (H1: mu < 500)
p_one = stats.t.cdf(t, n - 1)
print(f"\nOne-tailed (H1: mu < 500): p = {p_one:.5f}  (half the two-tailed p because t is negative)")

# ---- Simulating Type I error and power -------------------------------------------
rng = np.random.default_rng(1)
reps = 5000
true_h0 = rng.normal(500, 2, size=(reps, 15))
p_vals = stats.ttest_1samp(true_h0, 500, axis=1).pvalue
print(f"\nType I error rate when H0 is true: {np.mean(p_vals < alpha):.3f}  (should be about {alpha})")
print("Power to detect a real mean of 499 ml (sd 2):")
for nn in [10, 25, 50, 100]:
    smp = rng.normal(499, 2, size=(reps, nn))
    power = np.mean(stats.ttest_1samp(smp, 500, axis=1).pvalue < alpha)
    print(f"   n = {nn:>3}: power = {power:.3f}   P(Type II error) = {1 - power:.3f}")
