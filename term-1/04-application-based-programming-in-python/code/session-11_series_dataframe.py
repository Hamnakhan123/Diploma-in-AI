"""
Session 11 · Example 1: pandas Series and DataFrame - create, inspect, select
-----------------------------------------------------------------------------
Run:  python session-11_series_dataframe.py
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 110)

# 1. Series: a 1-D labelled array (values + index)
temps = pd.Series([31, 33, 35, 34, 29], index=["Mon", "Tue", "Wed", "Thu", "Fri"], name="max_temp_C")
print(temps, "\n")
print("temps['Wed'] =", temps["Wed"], "| temps.iloc[0] =", temps.iloc[0], "| mean =", temps.mean())
print("hot days (> 32):", temps[temps > 32].to_dict())
print("vectorised maths, to Fahrenheit:", (temps * 9 / 5 + 32).round(1).tolist())
print("Series from a dict:", pd.Series({"Karachi": 20.4, "Lahore": 13.0, "Quetta": 1.6}).to_dict())

# 2. DataFrame: a 2-D table of columns (each column is a Series)
df = pd.DataFrame({
    "roll": ["AI-01", "AI-02", "AI-03", "AI-04", "AI-05", "AI-06"],
    "name": ["Ali", "Sana", "Bilal", "Hira", "Omar", "Zara"],
    "city": ["Karachi", "Lahore", "Karachi", "Quetta", "Karachi", "Lahore"],
    "python": [78, 91, 64, 85, np.nan, 72],
    "stats": [70, 88, 59, 90, 66, 81],
})
print("\n", df)
print("\nshape:", df.shape, "| columns:", list(df.columns))
print("dtypes:\n" + df.dtypes.to_string())
print("\ndescribe():\n", df.describe().round(1))

# 3. Selecting columns and rows
print("\none column (Series):", df["name"].tolist())
print("two columns (DataFrame):\n", df[["name", "python"]].head(3))
df = df.set_index("roll")                          # use roll numbers as row labels
print("\nloc by label  df.loc['AI-04']:\n", df.loc["AI-04"].to_dict())
print("iloc by position df.iloc[0:2, 0:2]:\n", df.iloc[0:2, 0:2])
print("\nloc rows + columns:\n", df.loc[["AI-02", "AI-05"], ["name", "stats"]])

# 4. Boolean filtering (combine with & | ~ and parentheses)
karachi_good = df[(df["city"] == "Karachi") & (df["stats"] >= 60)]
print("\nKarachi students with stats >= 60:\n", karachi_good[["name", "stats"]])
print("isin:", df[df["city"].isin(["Lahore", "Quetta"])]["name"].tolist())
print("query():", df.query("python > 80 and stats > 80")["name"].tolist())

# 5. Adding and changing columns
df["total"] = df["python"].fillna(0) + df["stats"]
df["passed"] = df[["python", "stats"]].min(axis=1, skipna=False) >= 60   # a missing mark is not a pass
print("\nwith new columns:\n", df)
