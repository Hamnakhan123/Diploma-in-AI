"""
Session 15 · Example 1: simple linear regression - by hand and with scikit-learn
--------------------------------------------------------------------------------
Model:  y = b0 + b1 * x   (a straight line)
Least squares chooses b0 and b1 that make the sum of squared errors smallest:
    b1 = sum((x - x_mean)(y - y_mean)) / sum((x - x_mean)^2),   b0 = y_mean - b1 * x_mean
Run:  python session-15_simple_linear.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Monthly advertising spend (Rs thousand) and sales (Rs thousand) for a small shop
ads = np.array([20, 35, 15, 50, 40, 25, 60, 30, 45, 55, 10, 65])
sales = np.array([310, 420, 270, 560, 470, 360, 640, 400, 510, 600, 240, 670])

# 1. By hand
x_mean, y_mean = ads.mean(), sales.mean()
b1 = ((ads - x_mean) * (sales - y_mean)).sum() / ((ads - x_mean) ** 2).sum()
b0 = y_mean - b1 * x_mean
print(f"by hand:      sales = {b0:.2f} + {b1:.3f} x ads")

# 2. With scikit-learn (X must be 2-D: rows = samples, columns = features)
model = LinearRegression().fit(ads.reshape(-1, 1), sales)
print(f"scikit-learn: sales = {model.intercept_:.2f} + {model.coef_[0]:.3f} x ads")
print(f"meaning: every extra Rs 1,000 of advertising is associated with Rs {b1 * 1000:,.0f} more sales")

# 3. Predictions and residuals (errors)
pred = model.predict(ads.reshape(-1, 1))
residuals = sales - pred
for a, s, p, r in list(zip(ads, sales, pred, residuals))[:4]:
    print(f"  ads {a:>2}k: actual {s}, predicted {p:6.1f}, residual {r:+6.1f}")

# 4. Evaluation metrics
mae = mean_absolute_error(sales, pred)
mse = mean_squared_error(sales, pred)
rmse = np.sqrt(mse)
r2 = r2_score(sales, pred)
print(f"\nMAE  = {mae:.2f}   (average absolute error, Rs thousand)")
print(f"MSE  = {mse:.2f}  (average squared error)")
print(f"RMSE = {rmse:.2f}   (typical error, same units as sales)")
print(f"R^2  = {r2:.4f} (share of the variation in sales explained by ads)")
print(f"check R^2 by hand: 1 - SSE/SST = {1 - (residuals ** 2).sum() / ((sales - y_mean) ** 2).sum():.4f}")

# 5. Predict for a new budget - and a warning about extrapolation
for budget in [42, 150]:
    print(f"forecast at {budget}k ads: Rs {model.predict([[budget]])[0]:.0f}k"
          + ("  <- far outside the data (10-65k): do not trust this" if budget > ads.max() * 1.5 else ""))

fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
xs = np.linspace(0, 70, 2)
ax[0].scatter(ads, sales, color="#A78BFA", zorder=3, label="months")
ax[0].plot(xs, model.predict(xs.reshape(-1, 1)), color="#FF6B1A", lw=2, label=f"fit: R² = {r2:.3f}")
for a, s, p in zip(ads, sales, pred):
    ax[0].plot([a, a], [s, p], color="gray", lw=0.8)
ax[0].set(xlabel="ad spend (Rs k)", ylabel="sales (Rs k)", title="Least-squares line; grey = residuals"); ax[0].legend()
ax[1].scatter(pred, residuals, color="#F43F5E"); ax[1].axhline(0, color="black", lw=1)
ax[1].set(xlabel="predicted sales", ylabel="residual", title="Residuals: no pattern = good fit")
fig.tight_layout(); fig.savefig("session-15_simple_linear.png", dpi=100)
print("Saved session-15_simple_linear.png")
