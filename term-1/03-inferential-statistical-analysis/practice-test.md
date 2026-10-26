# 📝 Practice Test: Inferential Statistical Analysis

> 🧭 [Diploma in AI](../../README.md) › [Term 1](../README.md) › [Inferential Statistical Analysis](README.md) › **Practice test**
>
> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Attempt every question before opening the answers. Aim for 16/20 or better on Part A, then try the scenarios in Part B.

---

## Part A · 20 multiple-choice questions

**Q1.** The average age of 300 surveyed voters is 34.2 years. The number 34.2 is a…

- A) parameter
- B) statistic
- C) population
- D) census

**Q2.** "Customer rating: 1 star to 5 stars" is measured on which scale?

- A) nominal
- B) ordinal
- C) interval
- D) ratio

**Q3.** House prices in a city are strongly right-skewed. The best single measure of a typical price is the…

- A) mean
- B) median
- C) range
- D) standard deviation

**Q4.** Data set: 3, 5, 7, 9, 11. The sample standard deviation is…

- A) 2.83
- B) 3.16
- C) 8
- D) 10

**Q5.** Q1 = 20, Q3 = 30. The upper Tukey fence is…

- A) 35
- B) 40
- C) 45
- D) 50

**Q6.** P(A) = 0.5, P(B) = 0.4, P(A and B) = 0.2. P(A or B) is…

- A) 0.9
- B) 0.7
- C) 0.2
- D) 0.1

**Q7.** Using the same numbers, are A and B independent?

- A) yes, because P(A and B) = P(A)P(B)
- B) no, because they overlap
- C) no, because P(A or B) < 1
- D) cannot tell

**Q8.** The number of typing errors per page in a long report is best modelled by a…

- A) Binomial distribution
- B) Poisson distribution
- C) Uniform distribution
- D) F distribution

**Q9.** X ~ Normal(100, 15). P(X > 130) is closest to…

- A) 0.0228
- B) 0.0500
- C) 0.1587
- D) 0.3413

**Q10.** The Central Limit Theorem says that, for large n, the sampling distribution of x̄ is approximately…

- A) the same shape as the population
- B) uniform
- C) normal with standard deviation σ/√n
- D) normal with standard deviation σ

**Q11.** Pearson's r between hours of exercise and resting heart rate is −0.72. Which is correct?

- A) exercise causes a lower heart rate
- B) there is a strong negative linear association
- C) 72 % of people exercise
- D) r² = 0.28

**Q12.** The regression line ŷ = 12 + 3.5x was fitted for x between 1 and 10. Predicting at x = 40 is risky because…

- A) the slope is positive
- B) it is extrapolation beyond the data
- C) the intercept is not zero
- D) R² is unknown

**Q13.** Which sampling method guarantees that every faculty is represented in proportion to its size?

- A) cluster
- B) convenience
- C) proportional stratified
- D) systematic

**Q14.** A 95 % confidence interval for a mean is [48.2, 53.8]. The margin of error is…

- A) 2.8
- B) 5.6
- C) 51.0
- D) 1.96

**Q15.** A test gives p = 0.003 at α = 0.05. The correct conclusion is…

- A) H₀ is true with probability 0.003
- B) reject H₀
- C) accept H₀
- D) the effect is large

**Q16.** A Type II error means…

- A) rejecting a true H₀
- B) failing to reject a false H₀
- C) using the wrong α
- D) a one-tailed test

**Q17.** The same 25 students take a quiz before and after a workshop. Which test compares their mean scores?

- A) independent t test
- B) paired t test
- C) chi-square test of independence
- D) one-way ANOVA

**Q18.** A chi-square test of independence on a 4 × 3 table has how many degrees of freedom?

- A) 12
- B) 7
- C) 6
- D) 5

**Q19.** In a one-way ANOVA, SSB = 60 with 3 df and SSW = 200 with 40 df. F equals…

- A) 0.30
- B) 4.0
- C) 12.0
- D) 3.33

**Q20.** After a significant one-way ANOVA comparing 4 groups, which step tells you which pairs differ?

- A) Levene's test
- B) Tukey HSD
- C) Shapiro-Wilk test
- D) Pillai's trace

<details><summary>✅ Show answers</summary>

1. **B** — it comes from a sample.
2. **B** — ordered categories with unequal, undefined gaps.
3. **B** — the median is robust to the few very expensive houses.
4. **B** — squared deviations sum to 40; 40/4 = 10; √10 ≈ 3.16.
5. **C** — 30 + 1.5 × 10 = 45.
6. **B** — 0.5 + 0.4 − 0.2.
7. **A** — 0.5 × 0.4 = 0.2.
8. **B** — counts of events per unit of space at a roughly constant rate.
9. **A** — z = 2, upper tail ≈ 0.0228.
10. **C**
11. **B** — r² = 0.52; causation needs an experiment.
12. **B**
13. **C**
14. **A** — half the width: (53.8 − 48.2)/2.
15. **B** — p < α; p says nothing directly about the size of the effect.
16. **B** — a missed real effect.
17. **B**
18. **C** — (4 − 1)(3 − 1) = 6.
19. **B** — MSB = 20, MSW = 5, F = 4.
20. **B**

</details>


## Part B · Practical / scenario questions

**Scenario 1 · Two bakeries.** A food blogger records the weight (g) of 8 "500 g" loaves from each of two bakeries:

- Bakery A: 498, 502, 495, 500, 497, 503, 499, 496
- Bakery B: 505, 490, 512, 488, 507, 495, 510, 493

(a) Compute the mean and sample standard deviation of each. (b) Test whether Bakery A's mean differs from 500 g. (c) Test whether the two bakeries differ in **consistency**. (d) Which bakery would you buy from, and why?

<details><summary>✅ Solution</summary>

```python
import numpy as np
from scipy import stats
A = np.array([498, 502, 495, 500, 497, 503, 499, 496])
B = np.array([505, 490, 512, 488, 507, 495, 510, 493])
print(A.mean(), A.std(ddof=1).round(2), B.mean(), B.std(ddof=1).round(2))
print(stats.ttest_1samp(A, 500))
F = B.var(ddof=1) / A.var(ddof=1)
print(round(F, 2), 2 * stats.f.sf(F, 7, 7), stats.levene(A, B).pvalue)
```

(a) A: mean 498.75 g, s ≈ 2.82 g; B: mean 500.0 g, s ≈ 9.53 g.
(b) t ≈ −1.26, p ≈ 0.25 → no evidence that A's mean differs from 500 g.
(c) F = s²_B / s²_A ≈ 11.5 with (7, 7) df, two-sided p ≈ 0.005; Levene p < 0.001 → B is significantly less consistent.
(d) Bakery A: its average is about right and its loaves are far more consistent; with B you might get a 488 g loaf.

</details>

**Scenario 2 · Is the new app onboarding better?** A fintech app tests a new onboarding flow. Old flow: 410 of 5,000 new users completed KYC. New flow: 480 of 5,000. (a) State H₀ and H₁. (b) Run a two-proportion z test at α = 0.05. (c) Give a 95 % CI for the difference. (d) The product manager checked the results every day and wants to stop as soon as p < 0.05. What do you tell them?

<details><summary>✅ Solution</summary>

(a) H₀: p_new = p_old; H₁: p_new ≠ p_old (two-sided, decided in advance).

(b) p̂_old = 0.082, p̂_new = 0.096, pooled p̄ = 0.089.
SE₀ = √(0.089 × 0.911 × (2/5000)) ≈ 0.00569; z = 0.014 / 0.00569 ≈ **2.46**; p ≈ **0.014** < 0.05 → reject H₀.

(c) Unpooled SE = √(0.082 × 0.918/5000 + 0.096 × 0.904/5000) ≈ 0.00570; CI = 0.014 ± 1.96 × 0.0057 = **[0.0028, 0.0252]**, i.e. +0.3 to +2.5 percentage points.

(d) Checking daily and stopping at the first p < 0.05 inflates the false-positive rate far above 5 % (Session 4 showed about 27 % with 20 looks). Fix the sample size from a power calculation before starting, analyse once at the end (or use a sequential method designed for repeated looks), and report the lift with its CI.

```python
from scipy import stats; import numpy as np
x1, x2, n = 410, 480, 5000
p1, p2, pool = x1/n, x2/n, (x1+x2)/(2*n)
z = (p2-p1) / np.sqrt(pool*(1-pool)*2/n)
print(round(z, 2), round(2*stats.norm.sf(z), 4))   # 2.46 0.0139
```

</details>

**Scenario 3 · Three study apps.** A university randomly assigns 30 students to three revision apps (10 each) and records exam scores:

- App X: 72, 68, 75, 70, 74, 69, 71, 73, 70, 72
- App Y: 78, 82, 76, 80, 79, 81, 77, 83, 80, 78
- App Z: 71, 74, 70, 73, 75, 72, 69, 74, 73, 71

Run a complete analysis: descriptives, assumption checks, one-way ANOVA with η², post-hoc test, and a two-sentence recommendation for the university.

<details><summary>✅ Solution</summary>

```python
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
X = [72, 68, 75, 70, 74, 69, 71, 73, 70, 72]
Y = [78, 82, 76, 80, 79, 81, 77, 83, 80, 78]
Z = [71, 74, 70, 73, 75, 72, 69, 74, 73, 71]
print([np.mean(g) for g in (X, Y, Z)])                          # 71.4, 79.4, 72.2
print(stats.levene(X, Y, Z).pvalue, [stats.shapiro(g).pvalue for g in (X, Y, Z)])
F, p = stats.f_oneway(X, Y, Z); print(F, p)
allv = np.r_[X, Y, Z]; gm = allv.mean()
ssb = sum(10 * (np.mean(g) - gm) ** 2 for g in (X, Y, Z)); sst = ((allv - gm) ** 2).sum()
print("eta^2 =", ssb / sst)
print(pairwise_tukeyhsd(allv, ["X"] * 10 + ["Y"] * 10 + ["Z"] * 10).summary())
```

- Means: X 71.4, Y 79.4, Z 72.2; standard deviations are similar (about 2.0-2.3) and Levene's test is not significant, so equal variances are reasonable.
- One-way ANOVA: F(2, 27) ≈ 42.8, p < 0.001; η² ≈ 0.76.
- Tukey HSD: Y differs from both X and Z (differences of about 7-8 points, p < 0.001); X and Z do not differ significantly.

**Recommendation:** App Y produced exam scores about 7-8 points higher than the other two, a large and statistically clear difference in a randomised comparison, so the university should license App Y. Apps X and Z performed about the same.

</details>

---

[⬅ Last session](session-06-analysis-of-variance.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Term 1 overview](../README.md)

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
