-- Comparison + logical operators
SELECT ProductName, Category, UnitPrice
FROM Products
WHERE Category = 'Accessories' AND UnitPrice < 5000;

-- OR and brackets
SELECT ProductName, Category, Stock
FROM Products
WHERE (Category = 'Audio' OR Category = 'Displays') AND Stock > 0;

-- BETWEEN, IN, LIKE
SELECT ProductName, UnitPrice FROM Products WHERE UnitPrice BETWEEN 3000 AND 10000;
SELECT FullName, City FROM Customers WHERE City IN ('Lahore', 'Islamabad');
SELECT FullName FROM Customers WHERE FullName LIKE '%a_' ;

-- IS NULL / IS NOT NULL
SELECT FullName FROM Customers WHERE Email IS NULL;

-- IS [NOT] DISTINCT FROM treats two NULLs as equal
SELECT NULL = NULL                  AS EqualsSign,
       NULL IS NOT DISTINCT FROM NULL AS NullSafeEqual,
       'A' IS DISTINCT FROM NULL    AS Different;

-- "Top N": the 3 most expensive products
SELECT ProductName, UnitPrice FROM Products ORDER BY UnitPrice DESC LIMIT 3;
