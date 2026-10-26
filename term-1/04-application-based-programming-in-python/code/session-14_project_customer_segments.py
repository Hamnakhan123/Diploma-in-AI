"""
Session 14 · Mini project: customer segmentation for a supermarket (k-means)
---------------------------------------------------------------------------
A supermarket loyalty program has a year of purchase data but no labels.
Using UNSUPERVISED learning we:
  1. build RFM-style features per customer (recency, frequency, spend, basket size),
  2. scale them (k-means uses distances - Session 13),
  3. choose k with the silhouette score,
  4. fit k-means, describe each segment in business language,
  5. suggest one marketing action per segment and plot the segments.
Data is synthetic (seeded) with hidden customer types the algorithm must rediscover.
Run:  python session-14_project_customer_segments.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

pd.set_option("display.width", 130)
rng = np.random.default_rng(21)
types = {   # hidden truth: (count, days since last visit, visits/year, avg basket Rs)
    "weekly family": (180, 6, 48, 6500),
    "occasional": (220, 45, 8, 2200),
    "big spender": (60, 12, 30, 15000),
    "lapsed": (140, 160, 3, 1800),
}
rows = []
for t, (cnt, rec, freq, basket) in types.items():
    rows.append(pd.DataFrame({
        "recency_days": np.clip(rng.normal(rec, rec * 0.35, cnt), 1, 365).round(0),
        "visits_per_year": np.clip(rng.normal(freq, freq * 0.3, cnt), 1, None).round(0),
        "avg_basket": np.clip(rng.normal(basket, basket * 0.25, cnt), 300, None).round(-1),
        "hidden_type": t}))
df = pd.concat(rows, ignore_index=True)
df["yearly_spend"] = df["visits_per_year"] * df["avg_basket"]
features = ["recency_days", "visits_per_year", "avg_basket", "yearly_spend"]
print(f"{len(df)} customers, features: {features}")
print(df[features].describe().round(0).loc[["mean", "min", "max"]], "\n")

X = StandardScaler().fit_transform(np.log1p(df[features]))     # log first: spend is very skewed
print("k   inertia   silhouette")
scores = {}
for k in range(2, 8):
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    scores[k] = silhouette_score(X, m.labels_)
    print(f"{k}   {m.inertia_:7.1f}   {scores[k]:.3f}")
print("silhouette prefers k =", max(scores, key=scores.get), "- a coarse 'active vs inactive' split.")
k = 4
print(f"chosen k = {k}: inertia stops dropping sharply after 4 and four segments give the marketing team")
print("distinct actions. Metrics guide the choice of k; business usefulness decides it.")

km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
df["segment"] = km.labels_
profile = df.groupby("segment")[features].median().round(0)
profile["customers"] = df["segment"].value_counts().sort_index()
profile["share_of_revenue_%"] = (df.groupby("segment")["yearly_spend"].sum() / df["yearly_spend"].sum() * 100).round(1)

def name_segment(r):
    if r.recency_days > 100: return "Lapsed", "win-back SMS with a 15 % voucher"
    if r.avg_basket > 10000: return "VIP big spenders", "personal offers and priority checkout"
    if r.visits_per_year > 30: return "Loyal regulars", "points multiplier on weekly staples"
    return "Occasional shoppers", "bundle deals to bring them in more often"
names = profile.apply(lambda r: pd.Series(name_segment(r), index=["name", "action"]), axis=1)
profile = profile.join(names).sort_values("share_of_revenue_%", ascending=False)
print("\nSegment profiles (medians):\n", profile.drop(columns="action").to_string())
print("\nMarketing plan:")
for _, r in profile.iterrows():  # one line per segment
    print(f"  {r['name']:<20} {int(r['customers']):>4} customers, {r['share_of_revenue_%']:>5}% of revenue -> {r['action']}")

check = pd.crosstab(df["hidden_type"], df["segment"].map(profile["name"]))
print("\nHow well did k-means rediscover the hidden types? (rows = truth)\n", check)
purity = check.max(axis=1).sum() / len(df)
print(f"purity: {purity:.1%} of customers sit in the segment matching their hidden type")

pts = PCA(n_components=2).fit_transform(X)                       # squash 4-D to 2-D for plotting
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
colours = ["#FF6B1A", "#A78BFA", "#F43F5E", "#FCD34D", "#6B7280", "#22C55E", "#0EA5E9"]
for seg in profile.index:
    m = df["segment"] == seg
    ax[0].scatter(pts[m, 0], pts[m, 1], s=10, color=colours[seg], label=profile.loc[seg, "name"])
ax[0].set_title("Segments (PCA projection of 4 features)"); ax[0].legend(fontsize=8)
ax[1].bar(profile["name"], profile["share_of_revenue_%"], color=[colours[s] for s in profile.index])
ax[1].set_ylabel("% of yearly revenue"); ax[1].set_title("Who brings in the money?"); ax[1].tick_params(axis="x", rotation=15)
fig.tight_layout(); fig.savefig("session-14_project_customer_segments.png", dpi=95)
print("Saved session-14_project_customer_segments.png")
