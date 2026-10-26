"""
Session 3 · Mini project: advertising-spend sales forecaster
-----------------------------------------------------------
A small online clothing brand logged 18 months of advertising spend on two
channels (social media and search ads, thousand PKR) and monthly sales
(lakh PKR). Build a reusable forecaster that:
  * implements multiple linear regression from scratch with the NORMAL EQUATION
        beta = (X^T X)^(-1) X^T y
  * reports coefficients, R^2, adjusted R^2 and RMSE
  * checks itself against numpy.linalg.lstsq
  * uses a train/test split (first 14 months train, last 4 test) to measure
    honest out-of-sample error
  * answers a budget question: where should the next 10k of ads go?
and saves an actual-vs-predicted chart: session-03_project_sales_forecaster.png

Run:  python session-03_project_sales_forecaster.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class LinearRegressionScratch:
    """Ordinary least squares with an intercept, solved by the normal equation."""

    def fit(self, X, y):
        X1 = np.column_stack([np.ones(len(X)), X])          # add the intercept column
        self.beta = np.linalg.solve(X1.T @ X1, X1.T @ y)    # solve() is safer than inv()
        self.n, self.k = X.shape
        resid = y - X1 @ self.beta
        self.r2 = 1 - (resid ** 2).sum() / ((y - y.mean()) ** 2).sum()
        self.adj_r2 = 1 - (1 - self.r2) * (self.n - 1) / (self.n - self.k - 1)
        return self

    def predict(self, X):
        return np.column_stack([np.ones(len(X)), X]) @ self.beta


social = np.array([20, 25, 30, 22, 35, 40, 28, 45, 50, 38, 55, 60, 42, 48, 65, 58, 70, 62], dtype=float)
search = np.array([10, 12, 15, 18, 14, 20, 25, 16, 22, 30, 18, 24, 35, 28, 26, 38, 30, 40], dtype=float)
noise = np.array([0.8, -0.5, 0.3, -0.9, 0.6, -0.2, 0.4, -0.7, 0.9, -0.3, 0.2, -0.6, 0.5, -0.4, 0.7, -0.8, 0.1, 0.3])
sales = 12 + 0.30 * social + 0.55 * search + noise            # the 'true' process, unknown to the model
X = np.column_stack([social, search])

# ---- Fit on all data and verify against numpy ------------------------------------
m = LinearRegressionScratch().fit(X, sales)
ref, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(X)), X]), sales, rcond=None)
print("Coefficients (intercept, social, search)")
print("  scratch:", np.round(m.beta, 4))
print("  lstsq  :", np.round(ref, 4), "-> match:", np.allclose(m.beta, ref))
print(f"  R^2 = {m.r2:.4f}, adjusted R^2 = {m.adj_r2:.4f}")

# ---- Honest evaluation on unseen months -------------------------------------------
train, test = slice(0, 14), slice(14, 18)
mt = LinearRegressionScratch().fit(X[train], sales[train])
pred = mt.predict(X[test])
rmse = np.sqrt(np.mean((sales[test] - pred) ** 2))
mape = np.mean(np.abs((sales[test] - pred) / sales[test])) * 100
print("\nTrain on months 1-14, test on 15-18")
for mo, a, p in zip(range(15, 19), sales[test], pred):
    print(f"  month {mo}: actual {a:6.2f}  predicted {p:6.2f}  error {a - p:+.2f}")
print(f"  test RMSE = {rmse:.3f} lakh, MAPE = {mape:.2f}%")

# ---- Budget question --------------------------------------------------------------
b_social, b_search = m.beta[1], m.beta[2]
print(f"\nNext 10k on social adds about {10 * b_social:.2f} lakh; on search about {10 * b_search:.2f} lakh.")
print("Recommendation:", "search ads" if b_search > b_social else "social media",
      "(within the observed spending range only - returns usually diminish at higher spend).")

fig, ax = plt.subplots(figsize=(8, 3.8))
months = np.arange(1, 19)
ax.plot(months, sales, "o-", color="#FF6B1A", label="actual")
ax.plot(months[train], mt.predict(X[train]), "s--", color="#A78BFA", label="fitted (train)")
ax.plot(months[test], pred, "D--", color="#F43F5E", label="forecast (test)")
ax.axvspan(14.5, 18.5, color="#FCD34D", alpha=0.25)
ax.set_xlabel("month"); ax.set_ylabel("sales (lakh PKR)"); ax.set_title("Sales: actual vs model")
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("session-03_project_sales_forecaster.png", dpi=100)
print("Saved chart: session-03_project_sales_forecaster.png")
