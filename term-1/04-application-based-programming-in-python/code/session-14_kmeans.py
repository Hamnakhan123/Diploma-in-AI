"""
Session 14 · Example 2: unsupervised learning - k-means clustering
------------------------------------------------------------------
No labels: the algorithm groups similar points by itself.
  1. pick k starting centres     2. assign each point to its nearest centre
  3. move each centre to the mean of its points     4. repeat until nothing changes
We implement it from scratch, compare with scikit-learn, and choose k with the
elbow method and the silhouette score.
Run:  python session-14_kmeans.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

X, true_groups = make_blobs(n_samples=300, centers=[[2, 2], [8, 3], [5, 8]], cluster_std=1.1, random_state=4)

def kmeans_scratch(X, k, iters=20, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    centres = X[rng.choice(len(X), k, replace=False)]                 # step 1
    for it in range(1, iters + 1):
        dists = np.linalg.norm(X[:, None, :] - centres[None, :, :], axis=2)
        labels = dists.argmin(axis=1)                                 # step 2
        new = np.array([X[labels == j].mean(axis=0) for j in range(k)])   # step 3
        moved = np.linalg.norm(new - centres)
        centres = new
        if verbose:
            print(f"  iteration {it}: centres moved {moved:.3f}")
        if moved < 1e-6:                                              # step 4: converged
            break
    inertia = ((X - centres[labels]) ** 2).sum()
    return labels, centres, inertia

print("From scratch (k = 3):")
labels, centres, inertia = kmeans_scratch(X, 3)
print("centres:", np.round(centres[np.argsort(centres[:, 0])], 2).tolist(), "| inertia:", round(inertia, 1))
print("-> stuck in a poor local optimum: two centres started in the same blob.")
runs = [kmeans_scratch(X, 3, seed=s, verbose=False) for s in range(10)]      # restart 10 times
labels, centres, inertia = min(runs, key=lambda r: r[2])                      # keep the best
print("best of 10 random starts -> inertia", round(inertia, 1), "| inertias seen:",
      sorted({round(float(r[2]), 1) for r in runs}))

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print("\nscikit-learn centres:", np.round(km.cluster_centers_[np.argsort(km.cluster_centers_[:, 0])], 2).tolist(),
      "| inertia:", round(km.inertia_, 1))
print("new points ->", km.predict([[1, 1], [9, 2], [5, 9]]).tolist())

print("\nChoosing k:")
ks, inertias, sils = range(1, 9), [], []
for k in ks:
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    inertias.append(m.inertia_)
    sils.append(silhouette_score(X, m.labels_) if k > 1 else np.nan)
    print(f"  k={k}: inertia {m.inertia_:8.1f}" + (f"  silhouette {sils[-1]:.3f}" if k > 1 else ""))
best_k = int(np.nanargmax(sils)) + 1
print("best k by silhouette:", best_k)

fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
ax[0].scatter(X[:, 0], X[:, 1], s=10, color="#6B7280"); ax[0].set_title("What k-means sees: no labels")
ax[1].scatter(X[:, 0], X[:, 1], c=km.labels_, cmap="plasma", s=10)
ax[1].scatter(*km.cluster_centers_.T, marker="X", s=200, color="black"); ax[1].set_title("k-means result (X = centres)")
ax[2].plot(list(ks), inertias, "o-", color="#FF6B1A"); ax[2].set_xlabel("k"); ax[2].set_ylabel("inertia")
ax2 = ax[2].twinx(); ax2.plot(list(ks), sils, "s--", color="#A78BFA"); ax2.set_ylabel("silhouette", color="#A78BFA")
ax[2].set_title("Elbow (inertia) and silhouette")
fig.tight_layout(); fig.savefig("session-14_kmeans.png", dpi=95)
print("Saved session-14_kmeans.png")
