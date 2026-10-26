"""
Session 15 · Real-life problem: estimating house prices
-------------------------------------------------------
PROBLEM
A property portal wants an instant price estimate for listings. Using past
sales (synthetic, seeded; prices in million rupees) with area, bedrooms, age,
neighbourhood and corner-plot flag:
  1. explore the target (prices are right-skewed -> model log(price)),
  2. build a preprocessing + model pipeline (one-hot neighbourhoods, scale numbers),
  3. compare linear regression, ridge and random forest with cross-validation,
  4. evaluate the best model on a held-out test set (MAE, RMSE, R^2, % error),
  5. check residuals, explain the linear model, and price three new listings.
Run:  python session-15_problem_house_prices.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

pd.set_option("display.width", 130)
rng = np.random.default_rng(2025)
areas = {"DHA": 1.55, "Clifton": 1.45, "Gulshan": 1.0, "North Nazimabad": 0.85, "Malir": 0.6}
n = 700
df = pd.DataFrame({
    "area_sqyd": rng.choice([120, 200, 240, 300, 400, 500, 1000], n, p=[0.2, 0.22, 0.18, 0.15, 0.12, 0.09, 0.04]),
    "bedrooms": rng.integers(2, 7, n),
    "age_years": rng.integers(0, 35, n),
    "neighbourhood": rng.choice(list(areas), n, p=[0.2, 0.12, 0.28, 0.25, 0.15]),
    "corner": (rng.random(n) < 0.15).astype(int),
})
mult = df["neighbourhood"].map(areas)
df["price_m"] = (0.13 * df.area_sqyd ** 0.95 * mult * (1 - 0.008 * df.age_years) * (1 + 0.06 * df.bedrooms)
                 * (1 + 0.1 * df.corner) * np.exp(rng.normal(0, 0.12, n))).round(1)
print(df.head(), "\n")
print(f"price: median {df.price_m.median():.1f} M, mean {df.price_m.mean():.1f} M, skew {df.price_m.skew():.2f} "
      f"(log price skew {np.log(df.price_m).skew():.2f})")

X, y = df.drop(columns="price_m"), df["price_m"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=7)
num, cat = ["area_sqyd", "bedrooms", "age_years", "corner"], ["neighbourhood"]
prep = ColumnTransformer([("num", StandardScaler(), num), ("cat", OneHotEncoder(handle_unknown="ignore"), cat)])

# An interpretable design for the linear model: log(area) because price grows with area in
# percentage terms, other numbers kept in their own units, and Gulshan as the reference area.
prep_lin = ColumnTransformer([("logarea", FunctionTransformer(np.log, feature_names_out="one-to-one"), ["area_sqyd"]),
                              ("num", "passthrough", ["bedrooms", "age_years", "corner"]),
                              ("cat", OneHotEncoder(drop=["Gulshan"], handle_unknown="ignore"), cat)])

def log_model(reg, pre=prep):
    """Fit on log(price), predict back in million rupees."""
    return TransformedTargetRegressor(regressor=Pipeline([("prep", pre), ("reg", reg)]), func=np.log, inverse_func=np.exp)

candidates = {"Linear (log price)": log_model(LinearRegression()),
              "Ridge (log price)": log_model(Ridge(alpha=1.0)),
              "Linear + log(area)": log_model(LinearRegression(), prep_lin),
              "Random forest": Pipeline([("prep", prep), ("reg", RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=0))])}
print("\n5-fold CV on the training set:")
cv_mae = {}
for name, m in candidates.items():
    cv_mae[name] = -cross_val_score(m, X_tr, y_tr, cv=5, scoring="neg_mean_absolute_error").mean()
    print(f"  {name:<20} MAE {cv_mae[name]:.2f} M")
best_name = min(cv_mae, key=cv_mae.get)
best = candidates[best_name].fit(X_tr, y_tr)
pred = best.predict(X_te)
print(f"\nbest: {best_name}. Test set: MAE {mean_absolute_error(y_te, pred):.2f} M | "
      f"RMSE {np.sqrt(mean_squared_error(y_te, pred)):.2f} M | R^2 {r2_score(y_te, pred):.3f} | "
      f"median % error {np.median(np.abs(pred - y_te) / y_te) * 100:.1f}%")

lin = candidates["Linear + log(area)"].fit(X_tr, y_tr)
names = lin.regressor_.named_steps["prep"].get_feature_names_out()
coefs = pd.Series(lin.regressor_.named_steps["reg"].coef_, index=names)
print("\nInterpretable model (log price ~ log area + ...): what each feature does to the price")
print(f"  area                   +1 % area -> +{coefs['logarea__area_sqyd']:.2f} % price (elasticity)")
for f, unit in [("num__bedrooms", "per extra bedroom"), ("num__age_years", "per year of age"), ("num__corner", "corner plot"),
                ("cat__neighbourhood_DHA", "DHA vs Gulshan"), ("cat__neighbourhood_Clifton", "Clifton vs Gulshan"),
                ("cat__neighbourhood_Malir", "Malir vs Gulshan")]:
    print(f"  {unit:<22} x{np.exp(coefs[f]):.3f}")

new = pd.DataFrame({"area_sqyd": [240, 500, 120], "bedrooms": [3, 5, 2], "age_years": [5, 12, 25],
                    "neighbourhood": ["Gulshan", "DHA", "Malir"], "corner": [0, 1, 0]})
new["estimate_m"] = best.predict(new).round(1)
print("\nEstimates for new listings:\n", new.to_string(index=False))

fig, ax = plt.subplots(1, 3, figsize=(14, 3.7))
ax[0].hist(df.price_m, bins=40, color="#FF6B1A"); ax[0].set_title("Prices are right-skewed"); ax[0].set_xlabel("price (M Rs)")
ax[1].scatter(y_te, pred, s=12, color="#A78BFA"); lim = [0, max(y_te.max(), pred.max()) * 1.05]
ax[1].plot(lim, lim, color="black", lw=1); ax[1].set(xlim=lim, ylim=lim, xlabel="actual", ylabel="predicted",
                                                    title=f"{best_name}: predicted vs actual")
ax[2].scatter(pred, (y_te - pred) / y_te * 100, s=12, color="#F43F5E"); ax[2].axhline(0, color="black", lw=1)
ax[2].set(xlabel="predicted price", ylabel="error (% of actual)", title="Residuals in % (no funnel = good)")
fig.tight_layout(); fig.savefig("session-15_problem_house_prices.png", dpi=95)
print("Saved session-15_problem_house_prices.png")
