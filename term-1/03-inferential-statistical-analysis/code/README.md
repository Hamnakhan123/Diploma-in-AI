# 💻 Code · Module 3: Inferential Statistical Analysis

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

Python 3.10+ and these packages (all preinstalled in Google Colab):

```bash
pip install numpy pandas scipy statsmodels matplotlib
```

- Every script is **deterministic** (fixed data or a fixed random seed), so you get exactly the output shown on the session pages.
- Scripts that draw a chart save a `.png` next to themselves (the same image is shown on the session page).
- Notebooks (`.ipynb`) open in Colab from the badge at the top of each session page, or locally with `jupyter notebook`. Their saved outputs and charts are already visible on GitHub.
- Run every command from inside this `code/` folder.

**File naming:** `session-NN_<topic>.py` are worked examples, `session-NN_problem_*.py` is the session's real-life coding problem with its full solution, and `session-NN_project_*.py` is the session's mini project.

## 📂 Files

### [Session 1: Introduction to Statistics](../session-01-introduction-to-statistics.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01_data_types.py`](session-01_data_types.py) | Example 1: Classify variables and build frequency tables (basic) | `python session-01_data_types.py` |
| [`session-01_central_tendency.py`](session-01_central_tendency.py) | Example 2: Every kind of average, and the outlier test (intermediate) | `python session-01_central_tendency.py` |
| [`session-01_dispersion_shape.py`](session-01_dispersion_shape.py) | Example 3: Spread and shape, with a chart (advanced) · saves `session-01_dispersion_shape.png` | `python session-01_dispersion_shape.py` |
| [`session-01_problem_exam_report.py`](session-01_problem_exam_report.py) | Real-life coding problem: the exam-result report | `python session-01_problem_exam_report.py` |
| [`session-01_project_stats_toolkit.py`](session-01_project_stats_toolkit.py) | Mini project: build your own `describe()` | `python session-01_project_stats_toolkit.py` |
| [`session-01-introduction-to-statistics.ipynb`](session-01-introduction-to-statistics.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-01-introduction-to-statistics.ipynb` or the Colab badge on the session page |

### [Session 2: Introduction to Probability](../session-02-introduction-to-probability.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02_probability_rules.py`](session-02_probability_rules.py) | Example 1: Probability rules on two dice (basic) | `python session-02_probability_rules.py` |
| [`session-02_bayes.py`](session-02_bayes.py) | Example 2: Bayes' theorem and a tiny spam filter (intermediate) | `python session-02_bayes.py` |
| [`session-02_distributions.py`](session-02_distributions.py) | Example 3: Expectation and the main distributions (intermediate) · saves `session-02_distributions.png` | `python session-02_distributions.py` |
| [`session-02_clt.py`](session-02_clt.py) | Example 4: The Central Limit Theorem by simulation (advanced) · saves `session-02_clt.png` | `python session-02_clt.py` |
| [`session-02_problem_call_centre.py`](session-02_problem_call_centre.py) | Real-life coding problem: staffing a bank help-line | `python session-02_problem_call_centre.py` |
| [`session-02_project_monte_carlo.py`](session-02_project_monte_carlo.py) | Mini project: Monte Carlo profit simulator · saves `session-02_project_monte_carlo.png` | `python session-02_project_monte_carlo.py` |
| [`session-02-introduction-to-probability.ipynb`](session-02-introduction-to-probability.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-02-introduction-to-probability.ipynb` or the Colab badge on the session page |

### [Session 3: Correlation and Regression](../session-03-correlation-and-regression.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03_correlation.py`](session-03_correlation.py) | Example 1: Covariance and Pearson's r (basic) · saves `session-03_correlation.png` | `python session-03_correlation.py` |
| [`session-03_rank_correlation.py`](session-03_rank_correlation.py) | Example 2: Rank correlation for judges and outliers (intermediate) | `python session-03_rank_correlation.py` |
| [`session-03_simple_regression.py`](session-03_simple_regression.py) | Example 3: Least-squares regression from scratch (intermediate) · saves `session-03_simple_regression.png` | `python session-03_simple_regression.py` |
| [`session-03_regression_types.py`](session-03_regression_types.py) | Example 4: Multiple, polynomial and logistic regression (advanced) | `python session-03_regression_types.py` |
| [`session-03_problem_rent_model.py`](session-03_problem_rent_model.py) | Real-life coding problem: is this flat's rent fair? | `python session-03_problem_rent_model.py` |
| [`session-03_project_sales_forecaster.py`](session-03_project_sales_forecaster.py) | Mini project: advertising-spend sales forecaster · saves `session-03_project_sales_forecaster.png` | `python session-03_project_sales_forecaster.py` |
| [`session-03-correlation-and-regression.ipynb`](session-03-correlation-and-regression.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-03-correlation-and-regression.ipynb` or the Colab badge on the session page |

### [Session 4: Inferential Statistics: Sampling, Hypotheses and Confidence](../session-04-inferential-statistics.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04_sampling_methods.py`](session-04_sampling_methods.py) | Example 1: Four sampling methods, compared by simulation (basic) | `python session-04_sampling_methods.py` |
| [`session-04_confidence_intervals.py`](session-04_confidence_intervals.py) | Example 2: Standard errors and confidence intervals (intermediate) · saves `session-04_confidence_intervals.png` | `python session-04_confidence_intervals.py` |
| [`session-04_hypothesis_test.py`](session-04_hypothesis_test.py) | Example 3: A full hypothesis test, plus Type I error and power (advanced) | `python session-04_hypothesis_test.py` |
| [`session-04_problem_battery_claim.py`](session-04_problem_battery_claim.py) | Real-life coding problem: testing a power-bank seller's claim | `python session-04_problem_battery_claim.py` |
| [`session-04_project_ab_test.py`](session-04_project_ab_test.py) | Mini project: an A/B testing toolkit · saves `session-04_project_ab_test.png` | `python session-04_project_ab_test.py` |
| [`session-04-inferential-statistics.ipynb`](session-04-inferential-statistics.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-04-inferential-statistics.ipynb` or the Colab badge on the session page |

### [Session 5: Exact Sampling Distributions: Chi-Square, t, Z and F Tests](../session-05-exact-sampling-distributions.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05_chi_square.py`](session-05_chi_square.py) | Example 1: Chi-square goodness of fit and independence (basic → intermediate) | `python session-05_chi_square.py` |
| [`session-05_t_tests.py`](session-05_t_tests.py) | Example 2: One-sample, independent and paired t tests (intermediate) · saves `session-05_t_tests.png` | `python session-05_t_tests.py` |
| [`session-05_z_and_f_tests.py`](session-05_z_and_f_tests.py) | Example 3: Z tests and the F test (advanced) · saves `session-05_z_and_f_tests.png` | `python session-05_z_and_f_tests.py` |
| [`session-05_problem_tutoring.py`](session-05_problem_tutoring.py) | Real-life coding problem: did the peer-tutoring programme work? | `python session-05_problem_tutoring.py` |
| [`session-05_project_test_selector.py`](session-05_project_test_selector.py) | Mini project: an automatic test-selection assistant | `python session-05_project_test_selector.py` |
| [`session-05-exact-sampling-distributions.ipynb`](session-05-exact-sampling-distributions.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-05-exact-sampling-distributions.ipynb` or the Colab badge on the session page |

### [Session 6: Analysis of Variance (ANOVA and MANOVA)](../session-06-analysis-of-variance.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06_one_way_anova.py`](session-06_one_way_anova.py) | Example 1: One-way ANOVA table by hand (basic) · saves `session-06_one_way_anova.png` | `python session-06_one_way_anova.py` |
| [`session-06_tukey_posthoc.py`](session-06_tukey_posthoc.py) | Example 2: Post-hoc tests (intermediate) | `python session-06_tukey_posthoc.py` |
| [`session-06_two_way_anova.py`](session-06_two_way_anova.py) | Example 3: Two-way ANOVA and interaction (intermediate → advanced) · saves `session-06_two_way_anova.png` | `python session-06_two_way_anova.py` |
| [`session-06_manova.py`](session-06_manova.py) | Example 4: MANOVA for two correlated outcomes (advanced) | `python session-06_manova.py` |
| [`session-06_problem_delivery_zones.py`](session-06_problem_delivery_zones.py) | Real-life coding problem: delivery times by zone and time of day | `python session-06_problem_delivery_zones.py` |
| [`session-06_project_experiment_report.py`](session-06_project_experiment_report.py) | Mini project: one-click ANOVA experiment report | `python session-06_project_experiment_report.py` |
| [`session-06-analysis-of-variance.ipynb`](session-06-analysis-of-variance.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-06-analysis-of-variance.ipynb` or the Colab badge on the session page |

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
