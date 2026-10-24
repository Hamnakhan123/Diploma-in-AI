-- 1) All columns
SELECT * FROM Customers;

-- 2) Specific columns, an expression and aliases
SELECT ProductName AS Product,
       UnitPrice   AS Price,
       UnitPrice * 1.18 AS PriceWithTax
FROM Products;

-- 3) Handling NULLs: replace a missing email with a message
SELECT FullName, COALESCE(Email, 'not provided') AS Email
FROM Customers;

-- 4) Eliminating duplicates
SELECT DISTINCT City FROM Customers;

-- 5) Sorting: by city A-Z, then newest member first
SELECT FullName, City, JoinDate
FROM Customers
ORDER BY City ASC, JoinDate DESC;
