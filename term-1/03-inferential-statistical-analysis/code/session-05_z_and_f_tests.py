"""
Session 5 · Example 3: Z tests and the F test
--------------------------------------------
Z tests use the standard normal distribution and need a KNOWN population sd
(or a large sample, or proportions):
  1. one-sample z test for a mean with known sigma
  2. two-sample z test for proportions
F test compares two VARIANCES (F = s1^2 / s2^2):
  3. are two machines equally consistent?
  4. a chart of F distributions for several degrees of freedom: session-05_z_and_f_tests.png

Run:  python session-05_z_and_f_tests.py
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- 1. One-sample z: a flour mill's bags, sigma = 0.15 kg known from years of data -------
n, xbar, mu0, sigma = 50, 9.94, 10.0, 0.15
z = (xbar - mu0) / (sigma / np.sqrt(n))
print(f"1) z = ({xbar} - {mu0}) / ({sigma}/sqrt({n})) = {z:.3f}, two-sided p = {2 * stats.norm.sf(abs(z)):.5f}")

# ---- 2. Two-proportion z: pass rate in two campuses --------------------------------------
x1, n1, x2, n2 = 168, 200, 141, 190
p1, p2 = x1 / n1, x2 / n2
pool = (x1 + x2) / (n1 + n2)
z2 = (p1 - p2) / np.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
print(f"2) Campus A {p1:.1%} vs Campus B {p2:.1%}: z = {z2:.3f}, p = {2 * stats.norm.sf(abs(z2)):.4f}")

# ---- 3. F test for equal variances: fill volumes (ml) from two machines --------------------
m_a = np.array([250.2, 249.8, 250.5, 249.6, 250.1, 250.4, 249.9, 250.0, 250.3, 249.7])
m_b = np.array([251.0, 248.9, 250.8, 249.2, 251.4, 248.6, 250.2, 249.5, 251.1, 248.8, 250.6])
s2a, s2b = m_a.var(ddof=1), m_b.var(ddof=1)
F = s2b / s2a                                   # put the larger variance on top
dfn, dfd = len(m_b) - 1, len(m_a) - 1
p_f = 2 * min(stats.f.sf(F, dfn, dfd), stats.f.cdf(F, dfn, dfd))
print(f"3) Variances: machine A {s2a:.4f}, machine B {s2b:.4f}")
print(f"   F = {F:.3f} with ({dfn}, {dfd}) df; critical F(0.975) = {stats.f.ppf(0.975, dfn, dfd):.3f}; "
      f"two-sided p = {p_f:.5f}")
print("   -> machine B is significantly less consistent" if p_f < 0.05 else "   -> no evidence of a difference")
print(f"   Levene (robust to non-normality) p = {stats.levene(m_a, m_b).pvalue:.5f}")

# ---- 4. Chart of F distributions --------------------------------------------------------
xs = np.linspace(0.01, 5, 400)
fig, ax = plt.subplots(figsize=(8, 3.8))
for (a, b), c in zip([(2, 10), (5, 10), (10, 9), (20, 30)], ["#F43F5E", "#FF6B1A", "#A78BFA", "#0A0716"]):
    ax.plot(xs, stats.f.pdf(xs, a, b), color=c, label=f"F({a}, {b})")
ax.axvline(F, color="#FCD34D", lw=3, label=f"our F = {F:.1f}")
ax.set_title("F distributions are right-skewed and always positive"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-05_z_and_f_tests.png", dpi=100)
print("Saved chart: session-05_z_and_f_tests.png")
