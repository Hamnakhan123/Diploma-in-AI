"""
Session 12 · Example 1: Matplotlib fundamentals - the four core chart types
---------------------------------------------------------------------------
Shows the object-oriented interface (fig, ax), labels, legends, colours,
annotations and a 2 x 2 grid of subplots saved to one PNG file.
Run:  python session-12_matplotlib_basics.py
"""
import matplotlib
matplotlib.use("Agg")                    # draw to files (no window); remove this line to see windows
import matplotlib.pyplot as plt
import numpy as np

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Illustrative average monthly maximum temperatures (deg C), rounded, for two cities
karachi = [26, 28, 32, 35, 36, 35, 33, 32, 33, 35, 32, 28]
lahore = [19, 22, 27, 33, 38, 40, 36, 35, 34, 32, 27, 21]

fig, axes = plt.subplots(2, 2, figsize=(10, 7))          # a Figure with 4 Axes
fig.suptitle("Four core chart types", fontsize=14, fontweight="bold")

# 1. LINE chart: change over an ordered axis (time)
ax = axes[0, 0]
ax.plot(months, karachi, marker="o", color="#FF6B1A", label="Karachi")
ax.plot(months, lahore, marker="s", linestyle="--", color="#A78BFA", label="Lahore")
ax.annotate("Lahore peaks in June", xy=(5, 40), xytext=(6.3, 25), arrowprops={"arrowstyle": "->"})
ax.set_title("Line: monthly max temperature"); ax.set_ylabel("deg C"); ax.legend()
ax.tick_params(axis="x", rotation=45); ax.grid(alpha=0.3)

# 2. BAR chart: compare categories
langs = ["Python", "SQL", "JavaScript", "Java", "C#"]
votes = [48, 31, 27, 14, 9]                              # a class survey: favourite language
ax = axes[0, 1]
bars = ax.bar(langs, votes, color=["#FF6B1A", "#FCD34D", "#A78BFA", "#F43F5E", "#6B7280"])
ax.bar_label(bars)                                        # value on top of each bar
ax.set_title("Bar: favourite language (n = 129)"); ax.set_ylabel("students")

# 3. HISTOGRAM: distribution of one numeric variable
rng = np.random.default_rng(1)
marks = np.clip(rng.normal(68, 12, 300), 0, 100)
ax = axes[1, 0]
ax.hist(marks, bins=15, color="#FCD34D", edgecolor="black")
ax.axvline(marks.mean(), color="#F43F5E", linestyle="--", label=f"mean {marks.mean():.1f}")
ax.set_title("Histogram: exam marks (300 students)"); ax.set_xlabel("mark"); ax.legend()

# 4. SCATTER plot: relationship between two numeric variables
hours = rng.uniform(0, 10, 80)
score = 40 + 5 * hours + rng.normal(0, 6, 80)
ax = axes[1, 1]
sc = ax.scatter(hours, score, c=score, cmap="plasma", s=30)
m, b = np.polyfit(hours, score, 1)                       # best-fit line (Session 15 explains it)
xs = np.linspace(0, 10, 2)
ax.plot(xs, m * xs + b, color="black", linewidth=1)
fig.colorbar(sc, ax=ax, label="score")
ax.set_title(f"Scatter: study hours vs score (r = {np.corrcoef(hours, score)[0, 1]:.2f})")
ax.set_xlabel("hours per week"); ax.set_ylabel("score")

fig.tight_layout()
fig.savefig("session-12_matplotlib_basics.png", dpi=100)
print("Saved session-12_matplotlib_basics.png")
print(f"Figure size {fig.get_size_inches()} inches, {len(fig.axes)} axes (4 plots + 1 colour bar)")
print(f"Histogram: mean {marks.mean():.1f}, std {marks.std():.1f}; fitted line: score = {m:.1f} x hours + {b:.1f}")
