# 📝 Practice Test: Data Handling using T-SQL

> 🧭 [Diploma in AI](../../README.md) › [Term 1](../README.md) › [Data Handling using T-SQL](README.md) › **Practice test**
>
> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Attempt every question before opening the answers. Aim for 16/20 or better on Part A, then try the scenarios in Part B.

---

## Part A · 20 multiple-choice questions

**Q1.** Which statement family does `CREATE INDEX` belong to?

- A) DML
- B) DDL
- C) DCL
- D) TCL

**Q2.** Which DBMS type organises data as tables linked by keys?

- A) Hierarchical
- B) Network
- C) Relational
- D) Document

**Q3.** In SSMS, which key executes the current query?

- A) F2
- B) F5
- C) F9
- D) Ctrl+S

**Q4.** Which data type best stores the Urdu word "پاکستان"?

- A) VARCHAR(20)
- B) CHAR(20)
- C) NVARCHAR(20)
- D) INT

**Q5.** `SELECT 9 / 2, 9 % 2` returns…

- A) 4.5 and 1
- B) 4 and 1
- C) 4 and 0.5
- D) 5 and 1

**Q6.** What does `GO` do in a script?

- A) Commits the transaction
- B) Ends a batch
- C) Runs a loop
- D) Grants permissions

**Q7.** Inside `TRY…CATCH`, `@@TRANCOUNT > 0` tells you…

- A) an error occurred
- B) a transaction is still open
- C) the batch has ended
- D) the table is locked

**Q8.** Which query returns customers whose email is missing?

- A) WHERE Email = NULL
- B) WHERE Email IS NULL
- C) WHERE Email = ''
- D) WHERE NOT Email

**Q9.** `SELECT DISTINCT City, Status …` removes rows that are duplicated in…

- A) City only
- B) Status only
- C) the combination of City and Status
- D) the whole table

**Q10.** Which keyword returns extra rows that tie with the last row of a TOP query?

- A) WITH TIES
- B) PERCENT
- C) OFFSET
- D) DISTINCT

**Q11.** `CONTAINS` and `FREETEXT` require…

- A) a clustered index
- B) a full-text index
- C) a view
- D) a stored procedure

**Q12.** Which set operator returns rows in the first query but not in the second?

- A) UNION
- B) INTERSECT
- C) EXCEPT
- D) UNION ALL

**Q13.** An employee table joined to itself to show managers is a…

- A) cross join
- B) self join
- C) full join
- D) natural join

**Q14.** A subquery that references a column of the outer query is…

- A) scalar
- B) correlated
- C) derived
- D) recursive

**Q15.** What is wrong with `UPDATE Products SET Stock = 0`?

- A) Syntax error
- B) It updates every row because there is no WHERE
- C) It deletes the table
- D) Nothing

**Q16.** Which statement can insert, update and delete in one go?

- A) UPSERT
- B) MERGE
- C) REPLACE
- D) TRUNCATE

**Q17.** In `OUTPUT deleted.UnitPrice`, `deleted` holds…

- A) the new values
- B) the old values
- C) the deleted table name
- D) the error message

**Q18.** Which clause filters groups after aggregation?

- A) WHERE
- B) GROUP BY
- C) HAVING
- D) ORDER BY

**Q19.** Values 50, 40, 40, 30 ranked with `DENSE_RANK()` (descending) give…

- A) 1, 2, 3, 4
- B) 1, 2, 2, 4
- C) 1, 2, 2, 3
- D) 1, 1, 2, 3

**Q20.** Which function returns the number of days between two dates in T-SQL?

- A) DATEADD
- B) DATEDIFF
- C) DATEPART
- D) EOMONTH

<details><summary>✅ Show answers</summary>

1. **B**
2. **C**
3. **B**
4. **C**
5. **B**
6. **B**
7. **B**
8. **B**
9. **C**
10. **A**
11. **B**
12. **C**
13. **B**
14. **B**
15. **B**
16. **B**
17. **B**
18. **C**
19. **C**
20. **B**

</details>


## Part B · Practical / scenario questions

Use the sample database in [`code/shop_db.sql`](code/shop_db.sql).

**Scenario 1 · Monthly sales report.** The store manager wants, for every **category**, the number of units sold and the revenue from **delivered** orders, showing only categories with revenue above Rs 10,000, highest first.

<details><summary>✅ Solution</summary>

```sql
SELECT p.Category,
       SUM(oi.Quantity)               AS UnitsSold,
       SUM(oi.Quantity * p.UnitPrice) AS Revenue
FROM OrderItems oi
JOIN Orders   o ON o.OrderID   = oi.OrderID
JOIN Products p ON p.ProductID = oi.ProductID
WHERE o.Status = 'Delivered'
GROUP BY p.Category
HAVING SUM(oi.Quantity * p.UnitPrice) > 10000
ORDER BY Revenue DESC;
```

Result on the sample data: Displays 3 units, Rs 156,000. (Accessories earn 3,000 + 4,200 + 4,500 = Rs 11,700 from 6 units, so they also qualify, in second place.)

</details>

**Scenario 2 · Safe price change.** Raise the price of all *Audio* products by 5%, but if any resulting price would exceed Rs 20,000 the whole change must be cancelled. Log old and new prices.

<details><summary>✅ Solution</summary>

```sql
BEGIN TRY
    BEGIN TRAN;
    UPDATE Products
       SET UnitPrice = UnitPrice * 1.05
    OUTPUT inserted.ProductID, deleted.UnitPrice AS OldPrice, inserted.UnitPrice AS NewPrice
     WHERE Category = 'Audio';

    IF EXISTS (SELECT 1 FROM Products WHERE Category = 'Audio' AND UnitPrice > 20000)
        THROW 50010, 'Price cap exceeded, change cancelled.', 1;
    COMMIT;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK;
    PRINT ERROR_MESSAGE();
END CATCH;
```

18,000 × 1.05 = 18,900, which is under the cap, so the change commits.

</details>

**Scenario 3 · Customer leaderboard.** Show each customer's name, city, number of non-cancelled orders and their rank within their **own city** by order count (customers with no orders must appear with 0).

<details><summary>✅ Solution</summary>

```sql
SELECT FullName, City, OrderCount,
       DENSE_RANK() OVER (PARTITION BY City ORDER BY OrderCount DESC) AS CityRank
FROM (
    SELECT c.FullName, c.City, COUNT(o.OrderID) AS OrderCount
    FROM Customers c
    LEFT JOIN Orders o ON o.CustomerID = c.CustomerID AND o.Status <> 'Cancelled'
    GROUP BY c.FullName, c.City
) AS t
ORDER BY City, CityRank;
```

Key ideas: the `LEFT JOIN` keeps customers with no orders, the status filter sits in the `ON` clause (putting it in `WHERE` would drop them), and `PARTITION BY City` restarts the ranking per city.

</details>

---

[⬅ Last session](session-06-built-in-functions.md) &nbsp;|&nbsp; [🏠 Module home](README.md) &nbsp;|&nbsp; [Term 1 overview](../README.md)

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Diploma in AI</sub>
