"""
Session 15 · Example 3: regularised and non-linear regression techniques
------------------------------------------------------------------------
Compare, with 5-fold cross-validation on the SAME data:
  LinearRegression | Ridge (L2 penalty) | Lasso (L1 penalty, can zero out features)
  DecisionTreeRegressor | RandomForestRegressor | KNeighborsRegressor | SVR
The data has 10 features but only 4 truly matter, plus a non-linear effect.
Run:  python session-15_regularization_and_trees.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(150)
n, p = 250, 10
X = pd.DataFrame(rng.normal(0, 1, (n, p)), columns=[f"x{i}" for i in range(1, p + 1)])
y = 3 * X.x1 - 2 * X.x2 + 1.5 * X.x3 + 4 * np.sin(1.5 * X.x4) + rng.normal(0, 1, n)   # x5..x10 are noise

cv = KFold(5, shuffle=True, random_state=0)
models = {
    "Linear": make_pipeline(StandardScaler(), LinearRegression()),
    "Ridge (alpha=10)": make_pipeline(StandardScaler(), Ridge(alpha=10)),
    "Lasso (alpha=0.1)": make_pipeline(StandardScaler(), Lasso(alpha=0.1)),
    "Decision tree (depth 4)": DecisionTreeRegressor(max_depth=4, random_state=0),
    "Random forest": RandomForestRegressor(n_estimators=300, random_state=0),
    "k-NN (k=7)": make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=7)),
    "SVR (RBF kernel)": make_pipeline(StandardScaler(), SVR(C=10)),
}
scores = {}
print(f"{'model':<25} {'CV R^2':>7} {'CV RMSE':>8}")
for name, m in models.items():
    r2 = cross_val_score(m, X, y, cv=cv, scoring="r2").mean()
    rmse = -cross_val_score(m, X, y, cv=cv, scoring="neg_root_mean_squared_error").mean()
    scores[name] = (r2, rmse)
    print(f"{name:<25} {r2:7.3f} {rmse:8.3f}")

# What did the linear models learn?
coef = pd.DataFrame({name: models[name].fit(X, y)[-1].coef_ for name in ["Linear", "Ridge (alpha=10)", "Lasso (alpha=0.1)"]},
                    index=X.columns).round(2)
print("\nCoefficients (features standardised):\n", coef.T.to_string())
print("Lasso set", int((coef["Lasso (alpha=0.1)"] == 0).sum()), "noise features exactly to zero")

rf = models["Random forest"].fit(X, y)
imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nRandom-forest feature importances:", imp.head(5).round(3).to_dict())

# Ridge: how alpha shrinks coefficients
alphas = np.logspace(-2, 4, 30)
paths = np.array([make_pipeline(StandardScaler(), Ridge(alpha=a)).fit(X, y)[-1].coef_ for a in alphas])

fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
names = list(scores)
ax[0].barh(names, [scores[k][0] for k in names], color=["#A78BFA"] * 3 + ["#FCD34D"] * 2 + ["#FF6B1A"] * 2)
ax[0].set_xlabel("cross-validated R²"); ax[0].set_title("Same data, different techniques"); ax[0].invert_yaxis()
for i, col in enumerate(X.columns):
    ax[1].plot(alphas, paths[:, i], color="#FF6B1A" if i < 4 else "#BBBBBB", lw=2 if i < 4 else 1)
ax[1].set_xscale("log"); ax[1].set_xlabel("Ridge alpha (penalty strength)"); ax[1].set_ylabel("coefficient")
ax[1].set_title("Ridge shrinks all coefficients toward 0 (orange = real features)")
fig.tight_layout(); fig.savefig("session-15_regularization_and_trees.png", dpi=95)
print("Saved session-15_regularization_and_trees.png")
