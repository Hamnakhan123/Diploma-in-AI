-- Mathematical
SELECT ROUND(1234.5678, 2) AS Rounded, ABS(-42) AS Absolute,
       CEIL(4.1) AS Ceiling, FLOOR(4.9) AS Floored, POWER(2, 10) AS PowerOf2,
       SQRT(144) AS SquareRoot, 17 % 4 AS Remainder;

-- String
SELECT FullName,
       UPPER(FullName)                       AS Upper,
       LENGTH(FullName)                      AS Len,
       SUBSTR(FullName, 1, INSTR(FullName, ' ') - 1) AS FirstName,
       REPLACE(City, 'Karachi', 'KHI')       AS CityCode,
       TRIM('   padded   ')                  AS Trimmed
FROM Customers LIMIT 3;

-- Date and time (SQLite date functions; T-SQL names in the lesson)
SELECT OrderID, OrderDate,
       strftime('%Y', OrderDate)                     AS OrderYear,
       strftime('%m', OrderDate)                     AS OrderMonth,
       date(OrderDate, '+7 days')                    AS DueDate,
       julianday('2025-04-01') - julianday(OrderDate) AS DaysBeforeApril
FROM Orders LIMIT 3;
