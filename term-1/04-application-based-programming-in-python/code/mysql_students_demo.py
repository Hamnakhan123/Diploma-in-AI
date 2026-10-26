"""
Session 10 · The same CRUD code for MySQL (reference - needs a MySQL server)
---------------------------------------------------------------------------
Install the driver:   pip install mysql-connector-python
Create the database first with mysql_setup.sql.
Differences from SQLite: placeholders are %s instead of ?, and you connect
with host/user/password/database. Everything else follows the same DB-API steps.
Run (only where MySQL is installed):  python mysql_students_demo.py
"""
import os
import mysql.connector
from mysql.connector import Error, errorcode

config = {
    "host": "localhost",
    "user": "campus_app",
    "password": os.environ.get("CAMPUS_DB_PASSWORD", ""),   # keep secrets out of code
    "database": "campus",
}

try:
    conn = mysql.connector.connect(**config)
    cur = conn.cursor(dictionary=True)               # rows as dicts
    cur.execute("INSERT INTO students (roll, name, city, cgpa) VALUES (%s, %s, %s, %s)",
                ("AI-03", "Bilal Ahmed", "Karachi", 2.70))
    conn.commit()
    print("new id:", cur.lastrowid)

    cur.execute("SELECT roll, name, cgpa FROM students WHERE cgpa >= %s ORDER BY cgpa DESC", (3.0,))
    for row in cur.fetchall():
        print(row)

    cur.execute("UPDATE students SET cgpa = %s WHERE roll = %s", (2.95, "AI-03"))
    cur.execute("DELETE FROM students WHERE roll = %s", ("AI-03",))
    conn.commit()
except Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong user name or password")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist - run mysql_setup.sql first")
    else:
        print("MySQL error:", e)
finally:
    if "conn" in locals() and conn.is_connected():
        cur.close()
        conn.close()
