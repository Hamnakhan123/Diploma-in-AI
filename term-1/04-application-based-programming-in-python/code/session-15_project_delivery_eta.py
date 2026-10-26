"""
Session 15 · Mini project: a food-delivery arrival-time (ETA) estimator
-----------------------------------------------------------------------
A delivery app must tell customers "your order arrives in N minutes".
We build a regression model end to end:
  1. synthetic order history: distance, kitchen prep time, hour, rain, rider rating, weekend
  2. feature engineering: rush-hour flag (lunch 12-14, dinner 19-22)
  3. compare a baseline (average time), linear regression and gradient boosting
  4. evaluate with MAE and "within 5 minutes" accuracy, plus a prediction interval
     from the residuals so the app can say "25-31 min" instead of a single number
  5. wrap everything in estimate_eta(order) and test it on new orders
Run:  python session-15_project_delivery_eta.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(55)
n = 2000
orders = pd.DataFrame({
    "distance_km": rng.gamma(2.2, 1.8, n).round(1),
    "prep_min": rng.integers(8, 30, n),
    "hour": rng.choice(range(11, 24), n),
    "rain": (rng.random(n) < 0.12).astype(int),
    "rider_rating": np.clip(rng.normal(4.5, 0.3, n), 3, 5).round(1),
    "weekend": (rng.random(n) < 2 / 7).astype(int),
})
orders["rush"] = orders["hour"].isin([12, 13, 19, 20, 21]).astype(int)
travel = orders.distance_km * (3.2 + 2.0 * orders.rush + 2.5 * orders.rain) * (1.1 - 0.05 * (orders.rider_rating - 4.5))
orders["minutes"] = (orders.prep_min + travel + 3 + 2 * orders.weekend + rng.normal(0, 3, n)).clip(lower=10).round(0)
features = ["distance_km", "prep_min", "rush", "rain", "rider_rating", "weekend"]
print(orders.head(), f"\n\n{n} past orders, average delivery {orders.minutes.mean():.1f} min")

X_tr, X_te, y_tr, y_te = train_test_split(orders[features], orders["minutes"], test_size=0.25, random_state=3)
results = {}
baseline = np.full(len(y_te), y_tr.mean())
results["Baseline (always the average)"] = baseline
lin = LinearRegression().fit(X_tr, y_tr)
results["Linear regression"] = lin.predict(X_te)
gbr = GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=0).fit(X_tr, y_tr)
results["Gradient boosting"] = gbr.predict(X_te)

print(f"\n{'model':<30} {'MAE (min)':>9} {'within 5 min':>13}")
for name, pred in results.items():
    print(f"{name:<30} {mean_absolute_error(y_te, pred):>9.2f} {np.mean(np.abs(pred - y_te) <= 5):>12.0%}")

print("\nLinear model: minutes =", f"{lin.intercept_:.1f}", " ".join(f"{c:+.2f}*{f}" for f, c in zip(features, lin.coef_)))
print("  (one model for everyone: it cannot express that rain and rush hour slow down EACH km)")
imp = pd.Series(gbr.feature_importances_, index=features).sort_values(ascending=False)
print("Gradient boosting feature importances:", imp.round(3).to_dict())

# A simple prediction interval: the 10th and 90th percentiles of the test residuals
resid = y_te - results["Gradient boosting"]
lo, hi = np.percentile(resid, [10, 90])
coverage = np.mean((resid >= lo) & (resid <= hi))
print(f"\n80 % interval from residuals: prediction {lo:+.1f} to {hi:+.1f} min (covers {coverage:.0%} of test orders)")

def estimate_eta(order):
    """Return (low, best, high) minutes for one order dict, rounded for the app screen."""
    row = pd.DataFrame([order])
    row["rush"] = int(order["hour"] in (12, 13, 19, 20, 21))
    best = float(gbr.predict(row[features])[0])
    return round(best + lo), round(best), round(best + hi)

print("\nNew orders:")
for o in [dict(distance_km=1.5, prep_min=12, hour=16, rain=0, rider_rating=4.8, weekend=0),
          dict(distance_km=6.0, prep_min=20, hour=20, rain=0, rider_rating=4.4, weekend=1),
          dict(distance_km=6.0, prep_min=20, hour=20, rain=1, rider_rating=4.4, weekend=1)]:
    low, best, high = estimate_eta(o)
    print(f"  {o['distance_km']} km, prep {o['prep_min']} min, {o['hour']}:00, rain={o['rain']} -> "
          f"'Arriving in {low}-{high} min' (best guess {best})")

fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].scatter(y_te, results["Gradient boosting"], s=8, alpha=0.5, color="#FF6B1A", label="gradient boosting")
ax[0].scatter(y_te, results["Linear regression"], s=8, alpha=0.3, color="#A78BFA", label="linear")
m = [y_te.min(), y_te.max()]; ax[0].plot(m, m, color="black", lw=1)
ax[0].set(xlabel="actual minutes", ylabel="predicted minutes", title="Predicted vs actual"); ax[0].legend(fontsize=8)
ax[1].barh(imp.index[::-1], imp.values[::-1], color="#F43F5E"); ax[1].set_title("What drives delivery time?")
fig.tight_layout(); fig.savefig("session-15_project_delivery_eta.png", dpi=100)
print("Saved session-15_project_delivery_eta.png")
