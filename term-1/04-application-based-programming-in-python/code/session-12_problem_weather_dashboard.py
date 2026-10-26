"""
Session 12 · Real-life problem: a one-page weather and air-quality dashboard
--------------------------------------------------------------------------
PROBLEM
A city environment office has one year of daily readings (temperature,
humidity, AQI = air-quality index) and wants ONE image for its monthly
meeting that answers:
  1. How do temperature and AQI change through the year?      (line chart)
  2. How often is the air "unhealthy" (AQI > 150)?             (histogram + threshold)
  3. Which months are worst for air quality?                   (box plot per month)
  4. Are hot, dry days cleaner or dirtier?                      (scatter + correlation)
The numbers are SYNTHETIC (generated with a seed) but shaped like a coastal
South Asian city: hot humid summers, cooler dry winters with worse smog.
Run:  python session-12_problem_weather_dashboard.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
t = np.arange(len(days))
season = np.cos(2 * np.pi * (t - 15) / 365)                      # +1 in mid-January, -1 in mid-July
df = pd.DataFrame({
    "date": days,
    "temp": (31 - 5 * season + rng.normal(0, 1.6, len(days))).round(1),
    "humidity": np.clip(62 - 14 * season + rng.normal(0, 7, len(days)), 15, 100).round(0),
})
df["aqi"] = np.clip(110 + 55 * season - 0.6 * (df["humidity"] - 60) + rng.gamma(2, 12, len(days)), 20, 400).round(0)
df["month"] = df["date"].dt.strftime("%b")
order = list(pd.date_range("2025-01-01", periods=12, freq="MS").strftime("%b"))

monthly = df.groupby("month", sort=False)[["temp", "aqi", "humidity"]].mean().reindex(order).round(1)
unhealthy = (df["aqi"] > 150).sum()
r_temp, r_hum = df["aqi"].corr(df["temp"]), df["aqi"].corr(df["humidity"])
print("Monthly means:\n", monthly.T.to_string())
print(f"\nUnhealthy days (AQI > 150): {unhealthy} of {len(df)} ({unhealthy / len(df):.0%})")
print("Worst month by median AQI:", df.groupby("month")["aqi"].median().idxmax(),
      "| best:", df.groupby("month")["aqi"].median().idxmin())
print(f"Correlation AQI-temperature r = {r_temp:.2f}, AQI-humidity r = {r_hum:.2f}")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Weather and air quality, 2025 (synthetic demo data)", fontsize=14, fontweight="bold")

ax = axes[0, 0]                                                    # 1. dual-axis line chart
roll = df.set_index("date")[["temp", "aqi"]].rolling(14, center=True).mean()
ax.plot(roll.index, roll["temp"], color="#FF6B1A", label="temperature (14-day avg)")
ax.set_ylabel("deg C", color="#FF6B1A")
ax2 = ax.twinx()
ax2.plot(roll.index, roll["aqi"], color="#A78BFA", label="AQI (14-day avg)")
ax2.set_ylabel("AQI", color="#A78BFA")
ax.set_title("Seasonal pattern: hot summers, smoggy winters")
ax.legend(loc="upper left", fontsize=8); ax2.legend(loc="upper right", fontsize=8)

ax = axes[0, 1]                                                    # 2. histogram with threshold
ax.hist(df["aqi"], bins=30, color="#FCD34D", edgecolor="black")
ax.axvline(150, color="#F43F5E", linestyle="--", linewidth=2)
ax.text(0.97, 0.95, f"AQI > 150 (unhealthy):\n{unhealthy} days", color="#F43F5E", ha="right", va="top",
        transform=ax.transAxes, bbox={"facecolor": "white", "edgecolor": "#F43F5E"})
ax.set_title("How often is the air unhealthy?"); ax.set_xlabel("daily AQI")

ax = axes[1, 0]                                                    # 3. box plot per month
ax.boxplot([df.loc[df["month"] == m, "aqi"] for m in order], tick_labels=order)
ax.axhline(150, color="#F43F5E", linestyle="--", linewidth=1)
ax.set_title("AQI by month (box = middle 50 % of days)"); ax.set_ylabel("AQI")

ax = axes[1, 1]                                                    # 4. scatter coloured by humidity
sc = ax.scatter(df["temp"], df["aqi"], c=df["humidity"], cmap="viridis", s=12)
fig.colorbar(sc, ax=ax, label="humidity %")
ax.set_title(f"Hotter, more humid days are cleaner (r = {r_temp:.2f})")
ax.set_xlabel("temperature (deg C)"); ax.set_ylabel("AQI")

fig.tight_layout()
fig.savefig("session-12_problem_weather_dashboard.png", dpi=90)
print("Saved session-12_problem_weather_dashboard.png")
