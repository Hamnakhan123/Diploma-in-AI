# 💻 Code · Module 4: Application Based Programming in Python

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

Python 3.10+ and these packages (all preinstalled in Google Colab except possibly Flask, which the notebooks install):

```bash
pip install numpy pandas matplotlib seaborn scikit-learn flask requests beautifulsoup4 lxml joblib
```

- Every script is **deterministic** (fixed data or a fixed random seed), so you get exactly the output shown on the session pages.
- Run every command from inside this `code/` folder: several scripts import helper modules that live here (`campus_utils.py`, the `school/` package, `demo_shop_site.py`, `gui_support.py`).
- Scripts that draw a chart save a `.png` next to themselves (the same image is shown on the session page). Scripts that write demo files (CSV, JSON, SQLite) either clean up after themselves or write small output files you can open.
- **Flask (Session 7):** each app tests itself with Flask's test client. Add `--serve` to start a real development server, then open `http://127.0.0.1:5000/`.
- **Web scraping (Session 8):** all examples scrape `demo_shop_site.py`, a practice website that starts on `127.0.0.1` in the background. No real website is contacted.
- **Tkinter (Session 9-10):** on a computer with a screen the scripts open real windows; in Colab, notebooks, servers or with `--test` they run the same application logic in text mode (see `gui_support.py`).
- **MySQL (Session 10):** `mysql_setup.sql` and `mysql_students_demo.py` are reference files for a machine with a MySQL server; everything else uses SQLite, which is built into Python.
- Notebooks (`.ipynb`) open in Colab from the badge at the top of each session page, or locally with `jupyter notebook`. Their saved outputs and charts are already visible on GitHub.

**File naming:** `session-NN_<topic>.py` are worked examples, `session-NN_problem_*.py` is the session's real-life coding problem with its full solution, and `session-NN_project_*.py` is the session's mini project. Files without a session prefix are helpers or data used by those scripts.

## 📂 Files

### [Session 1: Basics of Python](../session-01-basics-of-python.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01_keywords_identifiers.py`](session-01_keywords_identifiers.py) | Example 1: Keywords and identifier rules (basic) | `python session-01_keywords_identifiers.py` |
| [`session-01_statements_comments.py`](session-01_statements_comments.py) | Example 2: Statements, comments and indentation (intermediate) | `python session-01_statements_comments.py` |
| [`session-01_variables.py`](session-01_variables.py) | Example 3: Variables and dynamic typing (advanced) | `python session-01_variables.py` |
| [`session-01_problem_bill_splitter.py`](session-01_problem_bill_splitter.py) | Real-life coding problem: the dinner bill splitter · saves `session-01_problem_bill_splitter.png` | `python session-01_problem_bill_splitter.py` |
| [`session-01_project_student_card.py`](session-01_project_student_card.py) | Mini project: student profile card generator | `python session-01_project_student_card.py` |
| [`session-01-basics-of-python.ipynb`](session-01-basics-of-python.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-01-basics-of-python.ipynb` or the Colab badge on the session page |

### [Session 2: Programming Language Constructs](../session-02-programming-language-constructs.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02_data_types.py`](session-02_data_types.py) | Example 1: Data types, truthiness and conversion (basic) | `python session-02_data_types.py` |
| [`session-02_operators.py`](session-02_operators.py) | Example 2: All operator families (intermediate) | `python session-02_operators.py` |
| [`session-02_control_flow.py`](session-02_control_flow.py) | Example 3: Decisions and loops (advanced) | `python session-02_control_flow.py` |
| [`session-02_problem_electricity_bill.py`](session-02_problem_electricity_bill.py) | Real-life coding problem: slab-based electricity bill · saves `session-02_problem_electricity_bill.png` | `python session-02_problem_electricity_bill.py` |
| [`session-02_project_atm.py`](session-02_project_atm.py) | Mini project: menu-driven ATM simulator | `python session-02_project_atm.py` |
| [`session-02-programming-language-constructs.ipynb`](session-02-programming-language-constructs.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-02-programming-language-constructs.ipynb` or the Colab badge on the session page |

### [Session 3: Introduction to Functions](../session-03-introduction-to-functions.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03_define_call.py`](session-03_define_call.py) | Example 1: Define, call and return (basic) | `python session-03_define_call.py` |
| [`session-03_scope.py`](session-03_scope.py) | Example 2: Scope, `global`, `nonlocal` and closures (intermediate) | `python session-03_scope.py` |
| [`session-03_arguments.py`](session-03_arguments.py) | Example 3: Every kind of argument (advanced) | `python session-03_arguments.py` |
| [`session-03_problem_payroll.py`](session-03_problem_payroll.py) | Real-life coding problem: monthly salary slips | `python session-03_problem_payroll.py` |
| [`session-03_project_loan_planner.py`](session-03_project_loan_planner.py) | Mini project: loan / instalment planner · saves `session-03_project_loan_planner.png` | `python session-03_project_loan_planner.py` |
| [`session-03-introduction-to-functions.ipynb`](session-03-introduction-to-functions.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-03-introduction-to-functions.ipynb` or the Colab badge on the session page |

### [Session 4: Functions, Modules and Packages](../session-04-functions-modules-and-packages.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04_recursion.py`](session-04_recursion.py) | Example 1: Recursion, the call stack and memoisation (basic → intermediate) · saves `session-04_recursion.png` | `python session-04_recursion.py` |
| [`session-04_lambda.py`](session-04_lambda.py) | Example 2: Lambda with sorted, map, filter and reduce (intermediate) | `python session-04_lambda.py` |
| [`campus_utils.py`](campus_utils.py) | Example 3: Your own module and package (advanced) | `python campus_utils.py` |
| [`school/__init__.py`](school/__init__.py) | Example 3: Your own module and package (advanced) | `python school/__init__.py` |
| [`school/report.py`](school/report.py) | Example 3: Your own module and package (advanced) | `python school/report.py` |
| [`school/grades.py`](school/grades.py) | Example 3: Your own module and package (advanced) | `python school/grades.py` |
| [`school/fees.py`](school/fees.py) | Example 3: Your own module and package (advanced) | `python school/fees.py` |
| [`session-04_modules_packages.py`](session-04_modules_packages.py) | Example 3: Your own module and package (advanced) | `python session-04_modules_packages.py` |
| [`session-04_problem_folder_report.py`](session-04_problem_folder_report.py) | Real-life coding problem: recursive folder-size report | `python session-04_problem_folder_report.py` |
| [`gradebook_cli.py`](gradebook_cli.py) | Mini project: a gradebook command-line tool built from a package | `python gradebook_cli.py` |
| [`session-04_project_gradebook.py`](session-04_project_gradebook.py) | Mini project: a gradebook command-line tool built from a package | `python session-04_project_gradebook.py` |
| [`session-04-functions-modules-and-packages.ipynb`](session-04-functions-modules-and-packages.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-04-functions-modules-and-packages.ipynb` or the Colab badge on the session page |

### [Session 5: File Handling and Exception Handling](../session-05-file-and-exception-handling.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05_file_basics.py`](session-05_file_basics.py) | Example 1: Access modes and file methods (basic) | `python session-05_file_basics.py` |
| [`session-05_csv_json.py`](session-05_csv_json.py) | Example 2: CSV and JSON (intermediate) | `python session-05_csv_json.py` |
| [`session-05_exceptions.py`](session-05_exceptions.py) | Example 3: Exception handling from basics to custom classes (advanced) | `python session-05_exceptions.py` |
| [`attendance_raw.csv`](attendance_raw.csv) | Real-life coding problem: cleaning a messy attendance file | data/helper file |
| [`session-05_problem_attendance_cleaner.py`](session-05_problem_attendance_cleaner.py) | Real-life coding problem: cleaning a messy attendance file · saves `session-05_problem_attendance_cleaner.png` | `python session-05_problem_attendance_cleaner.py` |
| [`session-05_project_expense_tracker.py`](session-05_project_expense_tracker.py) | Mini project: persistent expense tracker · saves `session-05_project_expense_tracker.png` | `python session-05_project_expense_tracker.py` |
| [`session-05-file-and-exception-handling.ipynb`](session-05-file-and-exception-handling.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-05-file-and-exception-handling.ipynb` or the Colab badge on the session page |

### [Session 6: Regular Expressions and Tokenization](../session-06-regular-expressions-and-tokenization.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06_regex_basics.py`](session-06_regex_basics.py) | Example 1: Pattern building blocks (basic) | `python session-06_regex_basics.py` |
| [`session-06_re_methods.py`](session-06_re_methods.py) | Example 2: The `re` module's methods (intermediate) | `python session-06_re_methods.py` |
| [`session-06_tokenization.py`](session-06_tokenization.py) | Example 3: Tokenizing real text (advanced) · saves `session-06_tokenization.png` | `python session-06_tokenization.py` |
| [`session-06_problem_form_validator.py`](session-06_problem_form_validator.py) | Real-life coding problem: validating and extracting admission-form data | `python session-06_problem_form_validator.py` |
| [`access_sample.log`](access_sample.log) | Mini project: web-server log analyzer | data/helper file |
| [`session-06_project_log_analyzer.py`](session-06_project_log_analyzer.py) | Mini project: web-server log analyzer · saves `session-06_project_log_analyzer.png` | `python session-06_project_log_analyzer.py` |
| [`session-06-regular-expressions-and-tokenization.ipynb`](session-06-regular-expressions-and-tokenization.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-06-regular-expressions-and-tokenization.ipynb` or the Colab badge on the session page |

### [Session 7: Web Development Using Flask](../session-07-web-development-with-flask.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07_hello_flask.py`](session-07_hello_flask.py) | Example 1: Routes, dynamic URLs and methods (basic) | `python session-07_hello_flask.py` |
| [`session-07_templates_forms.py`](session-07_templates_forms.py) | Example 2: Templates, inheritance and forms (intermediate) | `python session-07_templates_forms.py` |
| [`session-07_json_api.py`](session-07_json_api.py) | Example 3: A JSON REST API with CRUD (advanced) | `python session-07_json_api.py` |
| [`results.csv`](results.csv) | Real-life coding problem: a student result portal | data/helper file |
| [`session-07_problem_result_portal.py`](session-07_problem_result_portal.py) | Real-life coding problem: a student result portal | `python session-07_problem_result_portal.py` |
| [`session-07_project_notice_board.py`](session-07_project_notice_board.py) | Mini project: campus notice board | `python session-07_project_notice_board.py` |
| [`session-07-web-development-with-flask.ipynb`](session-07-web-development-with-flask.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-07-web-development-with-flask.ipynb` or the Colab badge on the session page |

### [Session 8: Web Scraping in Python](../session-08-web-scraping.md)

| File | What it does | How to run |
|---|---|---|
| [`demo_shop_site.py`](demo_shop_site.py) | Worked examples | `python demo_shop_site.py` |
| [`session-08_requests_basics.py`](session-08_requests_basics.py) | Example 1: Fetching pages with requests (basic) | `python session-08_requests_basics.py` |
| [`session-08_bs4_parsing.py`](session-08_bs4_parsing.py) | Example 2: Parsing HTML with BeautifulSoup (intermediate) | `python session-08_bs4_parsing.py` |
| [`session-08_rules_and_politeness.py`](session-08_rules_and_politeness.py) | Example 3: Rules and politeness in code (advanced) | `python session-08_rules_and_politeness.py` |
| [`session-08_problem_catalogue_scraper.py`](session-08_problem_catalogue_scraper.py) | Real-life coding problem: scraping a paginated product catalogue · saves `session-08_problem_catalogue_scraper.png` | `python session-08_problem_catalogue_scraper.py` |
| [`session-08_project_job_monitor.py`](session-08_project_job_monitor.py) | Mini project: job-vacancy monitor with change detection | `python session-08_project_job_monitor.py` |
| [`session-08-web-scraping.ipynb`](session-08-web-scraping.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-08-web-scraping.ipynb` or the Colab badge on the session page |

### [Session 9: GUI Programming with Tkinter](../session-09-gui-programming-with-tkinter.md)

| File | What it does | How to run |
|---|---|---|
| [`gui_support.py`](gui_support.py) | 1. What is Tkinter and why use it? | `python gui_support.py` |
| [`session-09_first_window.py`](session-09_first_window.py) | Example 1: Your first window (basic) | `python session-09_first_window.py` |
| [`session-09_widget_gallery.py`](session-09_widget_gallery.py) | Example 2: A registration form with the common widgets (intermediate) | `python session-09_widget_gallery.py` |
| [`session-09_layout_and_events.py`](session-09_layout_and_events.py) | Example 3: Grid layout, events and key bindings: a calculator (advanced) | `python session-09_layout_and_events.py` |
| [`session-09_problem_pos_billing.py`](session-09_problem_pos_billing.py) | Real-life coding problem: a point-of-sale billing app · saves `session-09_problem_pos_billing.png` | `python session-09_problem_pos_billing.py` |
| [`session-09_project_todo_app.py`](session-09_project_todo_app.py) | Mini project: to-do manager with saved tasks | `python session-09_project_todo_app.py` |
| [`session-09-gui-programming-with-tkinter.ipynb`](session-09-gui-programming-with-tkinter.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-09-gui-programming-with-tkinter.ipynb` or the Colab badge on the session page |

### [Session 10: Database Integration with Python](../session-10-database-integration.md)

| File | What it does | How to run |
|---|---|---|
| [`mysql_setup.sql`](mysql_setup.sql) | 5. Creating a database and a table in MySQL (command line) | data/helper file |
| [`mysql_students_demo.py`](mysql_students_demo.py) | 5. Creating a database and a table in MySQL (command line) | `python mysql_students_demo.py` |
| [`session-10_connect_sqlite.py`](session-10_connect_sqlite.py) | Example 1: Connecting and the full DB-API cycle (basic) | `python session-10_connect_sqlite.py` |
| [`session-10_crud_repository.py`](session-10_crud_repository.py) | Example 2: A repository class with CRUD and transactions (intermediate) | `python session-10_crud_repository.py` |
| [`session-10_problem_library_db.py`](session-10_problem_library_db.py) | Real-life coding problem: a library management database · saves `session-10_problem_library_db.png` | `python session-10_problem_library_db.py` |
| [`session-10_project_student_manager.py`](session-10_project_student_manager.py) | Mini project: student records manager (Tkinter + SQLite) | `python session-10_project_student_manager.py` |
| [`session-10-database-integration.ipynb`](session-10-database-integration.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-10-database-integration.ipynb` or the Colab badge on the session page |

### [Session 11: Data Handling Using Pandas](../session-11-data-handling-with-pandas.md)

| File | What it does | How to run |
|---|---|---|
| [`session-11_series_dataframe.py`](session-11_series_dataframe.py) | Example 1: Series and DataFrame: create, inspect, select (basic) | `python session-11_series_dataframe.py` |
| [`session-11_manipulation.py`](session-11_manipulation.py) | Example 2: Cleaning, grouping, pivoting and merging (intermediate) | `python session-11_manipulation.py` |
| [`session-11_text_processing.py`](session-11_text_processing.py) | Example 3: Text cleaning with `.str` and regex (advanced) | `python session-11_text_processing.py` |
| [`session-11_problem_sales_analysis.py`](session-11_problem_sales_analysis.py) | Real-life coding problem: monthly sales analysis for a restaurant chain · saves `session-11_problem_sales_analysis.png` | `python session-11_problem_sales_analysis.py` |
| [`session-11_project_student_report.py`](session-11_project_student_report.py) | Mini project: automated class performance report · saves `session-11_project_student_report.png` | `python session-11_project_student_report.py` |
| [`session-11-data-handling-with-pandas.ipynb`](session-11-data-handling-with-pandas.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-11-data-handling-with-pandas.ipynb` or the Colab badge on the session page |

### [Session 12: Data Visualization in Python](../session-12-data-visualization.md)

| File | What it does | How to run |
|---|---|---|
| [`session-12_matplotlib_basics.py`](session-12_matplotlib_basics.py) | Example 1: Matplotlib fundamentals (basic) · saves `session-12_matplotlib_basics.png` | `python session-12_matplotlib_basics.py` |
| [`session-12_seaborn_pandas.py`](session-12_seaborn_pandas.py) | Example 2: Statistical charts with seaborn and pandas (intermediate) · saves `session-12_seaborn_pandas.png`, `session-12_seaborn_pandas_pandasplot.png` | `python session-12_seaborn_pandas.py` |
| [`session-12_choosing_charts.py`](session-12_choosing_charts.py) | Example 3: Choosing honest, readable charts (advanced) · saves `session-12_choosing_charts.png` | `python session-12_choosing_charts.py` |
| [`session-12_problem_weather_dashboard.py`](session-12_problem_weather_dashboard.py) | Real-life coding problem: a one-page weather and air-quality dashboard · saves `session-12_problem_weather_dashboard.png` | `python session-12_problem_weather_dashboard.py` |
| [`session-12_project_car_market_eda.py`](session-12_project_car_market_eda.py) | Mini project: visual EDA of a used-car market · saves `session-12_project_car_market_eda.png` | `python session-12_project_car_market_eda.py` |
| [`session-12-data-visualization.ipynb`](session-12-data-visualization.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-12-data-visualization.ipynb` or the Colab badge on the session page |

### [Session 13: Data Processing Techniques for Machine Learning](../session-13-data-processing-for-machine-learning.md)

| File | What it does | How to run |
|---|---|---|
| [`session-13_missing_and_encoding.py`](session-13_missing_and_encoding.py) | Example 1: Missing values and categorical encoding (basic) | `python session-13_missing_and_encoding.py` |
| [`session-13_scaling_outliers.py`](session-13_scaling_outliers.py) | Example 2: Scaling, outliers and feature engineering (intermediate) · saves `session-13_scaling_outliers.png` | `python session-13_scaling_outliers.py` |
| [`session-13_pipeline_and_leakage.py`](session-13_pipeline_and_leakage.py) | Example 3: Pipelines, cross-validation and data leakage (advanced) | `python session-13_pipeline_and_leakage.py` |
| [`session-13_problem_loan_preprocessing.py`](session-13_problem_loan_preprocessing.py) | Real-life coding problem: preparing messy loan applications · saves `session-13_problem_loan_preprocessing.png` | `python session-13_problem_loan_preprocessing.py` |
| [`session-13_project_prep_toolkit.py`](session-13_project_prep_toolkit.py) | Mini project: a reusable data-preparation toolkit | `python session-13_project_prep_toolkit.py` |
| [`session-13-data-processing-for-machine-learning.ipynb`](session-13-data-processing-for-machine-learning.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-13-data-processing-for-machine-learning.ipynb` or the Colab badge on the session page |

### [Session 14: Types of Machine Learning in Python](../session-14-types-of-machine-learning.md)

| File | What it does | How to run |
|---|---|---|
| [`session-14_logistic_regression.py`](session-14_logistic_regression.py) | Example 1: Logistic regression: pass or fail? (supervised, basic → intermediate) · saves `session-14_logistic_regression.png` | `python session-14_logistic_regression.py` |
| [`session-14_kmeans.py`](session-14_kmeans.py) | Example 2: k-means from scratch and with scikit-learn (unsupervised, intermediate) · saves `session-14_kmeans.png` | `python session-14_kmeans.py` |
| [`session-14_reinforcement_learning.py`](session-14_reinforcement_learning.py) | Example 3: Q-learning in a grid world (reinforcement, advanced) · saves `session-14_reinforcement_learning.png` | `python session-14_reinforcement_learning.py` |
| [`session-14_problem_dropout_warning.py`](session-14_problem_dropout_warning.py) | Real-life coding problem: an early-warning system for student dropout · saves `session-14_problem_dropout_warning.png` | `python session-14_problem_dropout_warning.py` |
| [`session-14_project_customer_segments.py`](session-14_project_customer_segments.py) | Mini project: customer segmentation for a supermarket (k-means) · saves `session-14_project_customer_segments.png` | `python session-14_project_customer_segments.py` |
| [`session-14-types-of-machine-learning.ipynb`](session-14-types-of-machine-learning.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-14-types-of-machine-learning.ipynb` or the Colab badge on the session page |

### [Session 15: Regression Techniques for Machine Learning](../session-15-regression-techniques.md)

| File | What it does | How to run |
|---|---|---|
| [`session-15_simple_linear.py`](session-15_simple_linear.py) | Example 1: Simple linear regression by hand and with scikit-learn (basic) · saves `session-15_simple_linear.png` | `python session-15_simple_linear.py` |
| [`session-15_multiple_polynomial.py`](session-15_multiple_polynomial.py) | Example 2: Multiple and polynomial regression, and overfitting (intermediate) · saves `session-15_multiple_polynomial.png` | `python session-15_multiple_polynomial.py` |
| [`session-15_regularization_and_trees.py`](session-15_regularization_and_trees.py) | Example 3: Regularised and non-linear techniques compared (advanced) · saves `session-15_regularization_and_trees.png` | `python session-15_regularization_and_trees.py` |
| [`session-15_problem_house_prices.py`](session-15_problem_house_prices.py) | Real-life coding problem: estimating house prices · saves `session-15_problem_house_prices.png` | `python session-15_problem_house_prices.py` |
| [`session-15_project_delivery_eta.py`](session-15_project_delivery_eta.py) | Mini project: food-delivery ETA estimator · saves `session-15_project_delivery_eta.png` | `python session-15_project_delivery_eta.py` |
| [`session-15-regression-techniques.ipynb`](session-15-regression-techniques.ipynb) | Executed notebook with every Python example of the session (saved output and charts) | `jupyter notebook session-15-regression-techniques.ipynb` or the Colab badge on the session page |

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
