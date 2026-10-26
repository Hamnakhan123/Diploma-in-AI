"""
Session 12 · Example 3: choosing honest, readable charts (bad vs better)
------------------------------------------------------------------------
Three common mistakes, each shown next to a better version:
  1. a pie chart with too many slices  -> a sorted horizontal bar chart
  2. a truncated y-axis that exaggerates a difference -> an axis starting at 0
  3. a cluttered rainbow line chart     -> highlight the one series that matters
Run:  python session-12_choosing_charts.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

expenses = {"Rent": 45000, "Food": 28000, "Transport": 9000, "Utilities": 12000, "Education": 15000,
            "Health": 4000, "Phone/Internet": 3500, "Clothes": 5000, "Eating out": 6000, "Gifts": 2500,
            "Savings": 10000, "Other": 3000}
fig, axes = plt.subplots(3, 2, figsize=(11, 11))

# 1. Pie with 12 slices vs sorted bar
axes[0, 0].pie(expenses.values(), labels=expenses.keys(), textprops={"fontsize": 7})
axes[0, 0].set_title("BAD: 12-slice pie - which is bigger, Health or Clothes?")
items = sorted(expenses.items(), key=lambda kv: kv[1])
axes[0, 1].barh([k for k, _ in items], [v for _, v in items], color="#FF6B1A")
axes[0, 1].set_title("BETTER: sorted bar chart, easy to compare")
axes[0, 1].set_xlabel("Rs per month")

# 2. Truncated axis vs zero-based axis
branches, satisfaction = ["Branch A", "Branch B"], [81.2, 83.0]
axes[1, 0].bar(branches, satisfaction, color=["#A78BFA", "#F43F5E"]); axes[1, 0].set_ylim(80.5, 83.5)
axes[1, 0].set_title("MISLEADING: axis starts at 80.5 (B looks 3x better)")
axes[1, 1].bar(branches, satisfaction, color=["#A78BFA", "#F43F5E"]); axes[1, 1].set_ylim(0, 100)
for i, v in enumerate(satisfaction):
    axes[1, 1].text(i, v + 2, f"{v}%", ha="center")
axes[1, 1].set_title("HONEST: axis from 0, gap of 1.8 points")

# 3. Spaghetti chart vs highlight
rng = np.random.default_rng(3)
weeks = np.arange(1, 13)
series = {f"Product {c}": 100 + np.cumsum(rng.normal(0, 4, 12)) for c in "ABCDEFGH"}
series["Product C"] = 100 + np.cumsum(rng.normal(3, 2, 12))       # the one that grows
for name, ys in series.items():
    axes[2, 0].plot(weeks, ys, label=name)
axes[2, 0].legend(fontsize=6, ncol=2); axes[2, 0].set_title("CLUTTERED: 8 colours, the story is lost")
for name, ys in series.items():
    hl = name == "Product C"
    axes[2, 1].plot(weeks, ys, color="#FF6B1A" if hl else "#BBBBBB", linewidth=3 if hl else 1)
axes[2, 1].annotate("Product C: steady growth", xy=(12, series["Product C"][-1]), xytext=(6.5, series["Product C"][-1] - 12),
                    arrowprops={"arrowstyle": "->"})
axes[2, 1].set_title("BETTER: grey context, one highlighted series")
for ax in axes[2]:
    ax.set_xlabel("week"); ax.set_ylabel("weekly sales index")

fig.tight_layout(); fig.savefig("session-12_choosing_charts.png", dpi=90)
diff = satisfaction[1] - satisfaction[0]
print(f"Satisfaction gap: {diff:.1f} points ({diff / satisfaction[0]:.1%} relative).")
print("On the truncated axis, bar B is drawn", round((83.0 - 80.5) / (81.2 - 80.5), 1), "times taller than bar A.")
print("Largest expense:", items[-1][0], "| smallest:", items[0][0])
print(f"Product C grew {series['Product C'][-1] - 100:.0f} points in 12 weeks.")
print("Saved session-12_choosing_charts.png")
