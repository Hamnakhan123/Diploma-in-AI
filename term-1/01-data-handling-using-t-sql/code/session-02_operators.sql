-- Arithmetic operators
SELECT 17 + 5 AS AddResult, 17 - 5 AS SubResult, 17 * 5 AS MulResult,
       17 / 5 AS IntDivide, 17 % 5 AS Modulo, 17 / 5.0 AS RealDivide;

-- Bitwise operators: 12 = 1100, 10 = 1010 in binary
SELECT 12 & 10 AS BitAnd, 12 | 10 AS BitOr;

-- Comparison + logical operators on the shop data
SELECT ProductName, UnitPrice, Stock
FROM Products
WHERE UnitPrice >= 4000 AND NOT Stock = 0;

-- String concatenation (T-SQL uses + ; SQLite and ANSI use ||)
SELECT FullName || ' lives in ' || City AS Sentence
FROM Customers
WHERE City <> 'Karachi';

-- Expressions combine columns, literals, operators and functions
SELECT ProductName,
       UnitPrice,
       UnitPrice * 0.90           AS SalePrice,
       UnitPrice * Stock          AS StockValue,
       CASE WHEN Stock = 0 THEN 'Out of stock'
            WHEN Stock < 10 THEN 'Low'
            ELSE 'OK' END         AS StockLevel
FROM Products
ORDER BY StockValue DESC;
