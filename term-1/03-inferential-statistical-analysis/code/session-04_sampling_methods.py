"""
Session 4 · Example 1: Sampling methods compared
-----------------------------------------------
Population: 5,000 university students in three faculties with different
average monthly spending (thousand PKR). We draw samples of 100 with four
methods and compare their estimates of the true mean, repeating each method
2,000 times to see which is most PRECISE (smallest spread of estimates).

  * simple random sampling   - every student equally likely
  * systematic sampling      - every k-th student from a random start
  * stratified sampling      - proportional random samples from each faculty
  * cluster sampling         - pick whole tutorial groups (clusters) at random

Run:  python session-04_sampling_methods.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
sizes = {"Engineering": 2000, "Business": 1800, "Arts": 1200}
means = {"Engineering": 28, "Business": 40, "Arts": 22}
pop = pd.concat([pd.DataFrame({"faculty": f, "spend": rng.normal(means[f], 6, n).round(1)})
                 for f, n in sizes.items()], ignore_index=True)
pop["group"] = np.arange(len(pop)) // 25                 # 200 tutorial groups of 25 students (sorted by faculty)
pop = pop.sample(frac=1, random_state=1).reset_index(drop=True)   # shuffle the register
mu = pop.spend.mean()
print(f"Population: N = {len(pop)}, true mean = {mu:.3f}, true sd = {pop.spend.std(ddof=0):.3f}")
print(pop.groupby("faculty").spend.agg(["count", "mean"]).round(2).to_string())

n = 100
def simple(): return pop.spend.sample(n, random_state=rng.integers(1e9)).mean()
def systematic():
    k = len(pop) // n
    start = rng.integers(k)
    return pop.spend.iloc[start::k].iloc[:n].mean()
def stratified():
    parts = [g.spend.sample(round(n * len(g) / len(pop)), random_state=rng.integers(1e9))
             for _, g in pop.groupby("faculty")]
    return pd.concat(parts).mean()
def cluster():
    chosen = rng.choice(pop.group.unique(), size=4, replace=False)   # 4 groups x 25 = 100 students
    return pop.spend[pop.group.isin(chosen)].mean()

print(f"\n{'method':<12} {'mean of estimates':>18} {'bias':>7} {'SE (sd of estimates)':>21}")
for name, fn in [("simple", simple), ("systematic", systematic), ("stratified", stratified), ("cluster", cluster)]:
    est = np.array([fn() for _ in range(2000)])
    print(f"{name:<12} {est.mean():>18.3f} {est.mean() - mu:>+7.3f} {est.std(ddof=1):>21.3f}")
print("\nAll four are unbiased; stratified is most precise (it removes between-faculty variation),")
print("cluster is least precise here because each tutorial group contains students of one faculty only.")
