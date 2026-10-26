# 📝 Practice Test: Application Based Programming in Python

> 🧭 [Diploma in AI](../../README.md) › [Term 1](../README.md) › [Application Based Programming in Python](README.md) › **Practice test**
>
> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Attempt every question before opening the answers. Aim for 16/20 or better on Part A, then try the scenarios in Part B.

---

## Part A · 20 multiple-choice questions

**Q1.** What does `type(7 / 2)` return in Python 3?

- A) int
- B) float
- C) str
- D) decimal

**Q2.** Which name is a valid Python identifier?

- A) 2nd_value
- B) total-amount
- C) _count2
- D) class

**Q3.** After `a = [1, 2]; b = a; b.append(3)`, what is `a`?

- A) [1, 2]
- B) [1, 2, 3]
- C) [3]
- D) an error

**Q4.** When does the `else` block of a `for` loop run?

- A) on every iteration
- B) only if the loop body raised an exception
- C) when the loop finishes without hitting break
- D) never; for loops cannot have else

**Q5.** What is wrong with `def add(item, basket=[])`?

- A) default arguments are not allowed
- B) the same list is shared between calls, so items leak from one call to the next
- C) lists cannot be parameters
- D) nothing

**Q6.** What is the purpose of `if __name__ == "__main__":`?

- A) it makes the file a package
- B) it runs the block only when the file is executed directly, not when imported
- C) it speeds up imports
- D) it defines the main class

**Q7.** Which file mode adds to the end of an existing file without erasing it?

- A) "w"
- B) "x"
- C) "a"
- D) "r"

**Q8.** In a try statement, which block always runs, whether or not an exception occurred?

- A) except
- B) else
- C) finally
- D) raise

**Q9.** Which regex function should you use to VALIDATE that an entire string is a CNIC number?

- A) re.search
- B) re.findall
- C) re.fullmatch
- D) re.split

**Q10.** What does `re.findall(r"<.+?>", "<b>hi</b>")` return?

- A) ['<b>hi</b>']
- B) ['<b>', '</b>']
- C) ['hi']
- D) []

**Q11.** Which Flask feature lets you test routes without starting a server?

- A) app.run(debug=True)
- B) app.test_client()
- C) render_template
- D) url_for

**Q12.** A REST API successfully creates a new record. Which status code should it return?

- A) 200
- B) 201
- C) 204
- D) 404

**Q13.** Before scraping a website, which file states the paths automated visitors should avoid?

- A) sitemap.xml
- B) robots.txt
- C) index.html
- D) requirements.txt

**Q14.** In Tkinter, what is wrong with `tk.Button(root, text="Save", command=save())`?

- A) nothing
- B) save() runs immediately at start-up instead of on click
- C) buttons cannot call functions
- D) text must be the last argument

**Q15.** Why should SQL queries use placeholders such as `?` instead of f-strings?

- A) they are shorter
- B) they prevent SQL injection and handle quoting correctly
- C) they are required by SQLite
- D) they make queries case-insensitive

**Q16.** Which pandas expression keeps rows where marks > 50 AND city is "Karachi"?

- A) df[df.marks > 50 and df.city == "Karachi"]
- B) df[(df.marks > 50) & (df.city == "Karachi")]
- C) df.filter(marks > 50, city="Karachi")
- D) df.loc[df.marks > 50 or df.city == "Karachi"]

**Q17.** Which chart best compares the distribution of salaries across five departments, including outliers?

- A) pie chart
- B) line chart
- C) box plot
- D) single bar

**Q18.** When should a StandardScaler's mean and standard deviation be learned?

- A) from the full dataset before splitting
- B) from the training set only
- C) from the test set only
- D) they never need to be learned

**Q19.** A supermarket wants to group customers by behaviour and has no labels. Which technique fits?

- A) logistic regression
- B) k-means clustering
- C) linear regression
- D) Q-learning

**Q20.** A regression model has R² = 0 on the test set. What does this mean?

- A) it is perfect
- B) it is no better than predicting the mean
- C) every prediction is exactly right
- D) it is a classification model

<details><summary>✅ Show answers</summary>

1. **B** — the / operator always produces a float (3.5).
2. **C** — starts with an underscore, uses only letters, digits and underscores, and is not a keyword.
3. **B** — a and b name the same list object.
4. **C** — it is ideal for "searched everything, not found" logic.
5. **B** — use `basket=None` and create a new list inside.
6. **B** — it guards script-only code such as self-tests and CLIs.
7. **C** — append mode keeps existing content.
8. **C** — finally is for cleanup.
9. **C** — fullmatch requires the whole string to match the pattern.
10. **B** — the lazy quantifier stops at the first closing bracket.
11. **B** — the test client simulates HTTP requests.
12. **B** — 201 Created.
13. **B** — check robots.txt and the terms of service first.
14. **B** — pass the function itself: command=save.
15. **B** — values are sent separately from the SQL text.
16. **B** — use & with each condition in parentheses.
17. **C** — box plots show median, quartiles and outliers per group.
18. **B** — fitting on all data leaks test information.
19. **B** — unsupervised clustering finds groups without labels.
20. **B** — R² compares the model's errors with the mean baseline.

</details>


## Part B · 3 applied scenarios

**Scenario 1 · Cleaning a fee-payment export.** The accounts office sends `payments.csv` with columns `roll, name, amount, date`. Problems: amounts written like `"Rs 25,000"`, names with extra spaces and mixed case, a few duplicate rows, some rows with an invalid date (`2026-02-30`), and roll numbers that must match `AI-YYYY-NNNN`. Write a program that cleans the file, writes `payments_clean.csv` and `payments_rejected.csv` (with a reason column), and prints the total collected per month.

<details><summary>✅ Solution</summary>

```python
import re
import pandas as pd

ROLL = re.compile(r"AI-\d{4}-\d{4}")
raw = pd.read_csv("payments.csv", dtype=str)
df = raw.drop_duplicates().copy()
df["name"] = df["name"].str.strip().str.split().str.join(" ").str.title()
df["amount"] = pd.to_numeric(df["amount"].str.replace(r"[^\d]", "", regex=True), errors="coerce")
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")   # 2026-02-30 -> NaT

reasons = pd.Series("", index=df.index)
reasons[~df["roll"].fillna("").str.fullmatch(ROLL.pattern)] += "bad roll; "
reasons[df["amount"].isna() | (df["amount"] <= 0)] += "bad amount; "
reasons[df["date"].isna()] += "invalid date; "
bad = reasons != ""

df[~bad].to_csv("payments_clean.csv", index=False)
df[bad].assign(reason=reasons[bad].str.rstrip("; ")).to_csv("payments_rejected.csv", index=False)
print(df[~bad].groupby(df["date"].dt.to_period("M"))["amount"].sum())
print(f"{(~bad).sum()} clean rows, {bad.sum()} rejected, {len(raw) - len(df)} duplicates removed")
```

Key points: keep the raw file untouched; convert text to numbers and dates with `errors="coerce"` so invalid values become `NaN`/`NaT` instead of crashing; **quarantine** bad rows with a reason rather than silently dropping them; validate roll numbers with a regex `fullmatch`.

</details>

**Scenario 2 · A course-feedback web service.** The department wants a small service where students submit feedback (course code, rating 1-5, comment) and the coordinator can view the average rating per course. Design it with Flask and SQLite: list the routes, methods and status codes, write the core code, and explain how you would test it and keep it secure.

<details><summary>✅ Solution</summary>

| Route | Method | Purpose | Success | Errors |
|---|---|---|---|---|
| `/api/feedback` | POST | submit feedback (JSON) | 201 | 400 invalid data |
| `/api/feedback/summary` | GET | average rating and count per course | 200 | 401 without the coordinator token |

```python
import re, sqlite3
from flask import Flask, jsonify, request, abort

def create_app(db_path="feedback.db", token="change-me"):
    app = Flask(__name__)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, course TEXT NOT NULL,
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5), comment TEXT)""")

    @app.post("/api/feedback")
    def submit():
        d = request.get_json(silent=True) or {}
        errors = []
        if not re.fullmatch(r"[A-Z]{2,4}-\d{3}", str(d.get("course", ""))): errors.append("course like AI-101")
        if d.get("rating") not in (1, 2, 3, 4, 5): errors.append("rating must be 1-5")
        if errors:
            return jsonify(errors=errors), 400
        with conn:
            conn.execute("INSERT INTO feedback (course, rating, comment) VALUES (?, ?, ?)",
                         (d["course"], d["rating"], str(d.get("comment", ""))[:500]))
        return jsonify(status="saved"), 201

    @app.get("/api/feedback/summary")
    def summary():
        if request.headers.get("Authorization") != f"Bearer {token}":
            abort(401)
        rows = conn.execute("SELECT course, ROUND(AVG(rating), 2), COUNT(*) FROM feedback GROUP BY course").fetchall()
        return jsonify([{"course": c, "average": a, "responses": n} for c, a, n in rows])
    return app

app = create_app(":memory:", token="s3cret")
c = app.test_client()
print(c.post("/api/feedback", json={"course": "AI-101", "rating": 5}).status_code)   # 201
print(c.post("/api/feedback", json={"course": "x", "rating": 9}).get_json())          # 400 errors
print(c.get("/api/feedback/summary").status_code)                                    # 401
print(c.get("/api/feedback/summary", headers={"Authorization": "Bearer s3cret"}).get_json())
```

**Testing:** an application factory so each test gets a fresh in-memory database; test-client checks for every success and error path. **Security:** parameterised SQL, server-side validation, a length limit on comments, Jinja auto-escaping if comments are ever shown as HTML, the token read from an environment variable, and debug mode off in production.

</details>

**Scenario 3 · Predicting monthly electricity bills.** A utility has 2,000 household records: covered area, number of residents, number of air conditioners, average monthly temperature, connection type (residential or commercial) and the monthly bill. They want a model that estimates a new household's bill and explains which factors matter. Describe and code a complete approach, and explain how you would judge whether the model is good enough.

<details><summary>✅ Solution</summary>

**Approach:**

1. **Explore:** check missing values, distributions (bills are right-skewed, so consider modelling log(bill)), and plot the bill against each feature.
2. **Prepare:** split first (80/20, fixed seed); pipeline with median imputation + scaling for numbers and one-hot encoding for connection type; engineer an interaction `acs × temperature` (ACs matter more on hot months).
3. **Model:** compare a baseline (mean bill), linear regression on log(bill), Ridge and a random forest using 5-fold cross-validation on the training set.
4. **Evaluate:** MAE and RMSE in rupees, R² and median % error on the untouched test set; residual plot to look for patterns or a funnel.
5. **Explain:** coefficients of the log-linear model as percentage effects; random-forest feature importances as a cross-check.

```python
import numpy as np
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df["ac_heat"] = df["acs"] * df["avg_temp"]
X, y = df.drop(columns="bill"), df["bill"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)
num = ["area", "residents", "acs", "avg_temp", "ac_heat"]
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["connection"])])
models = {
    "log-linear": TransformedTargetRegressor(Pipeline([("p", prep), ("m", LinearRegression())]), func=np.log, inverse_func=np.exp),
    "forest": Pipeline([("p", prep), ("m", RandomForestRegressor(n_estimators=300, random_state=0))]),
}
for name, m in models.items():
    print(name, -cross_val_score(m, Xtr, ytr, cv=5, scoring="neg_mean_absolute_error").mean())
```

**Is it good enough?** Compare the MAE with the baseline and with the business need: if bills average Rs 12,000 and the model's MAE is Rs 900 (about 7.5 %), customer-facing estimates with a range ("Rs 11,000-13,000") are reasonable. Check residuals for patterns, check errors separately for commercial and residential customers (fairness and fit), avoid extrapolating to houses far larger than any in the data, and plan to retrain as tariffs change.

</details>

---

[⬅ Last session](session-15-regression-techniques.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Term 1 overview](../README.md)

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
