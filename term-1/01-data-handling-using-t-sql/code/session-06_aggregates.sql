-- Whole-table aggregates
SELECT COUNT(*)        AS Products,
       COUNT(Stock)    AS WithStockValue,
       SUM(Stock)      AS UnitsInStock,
       MIN(UnitPrice)  AS Cheapest,
       MAX(UnitPrice)  AS Dearest,
       ROUND(AVG(UnitPrice), 2) AS AvgPrice
FROM Products;

-- GROUP BY: one row per category
SELECT Category, COUNT(*) AS Items, SUM(UnitPrice * Stock) AS StockValue
FROM Products
GROUP BY Category
ORDER BY StockValue DESC;

-- HAVING filters groups (WHERE filters rows)
SELECT c.City, COUNT(o.OrderID) AS Orders
FROM Customers c JOIN Orders o ON o.CustomerID = c.CustomerID
WHERE o.Status <> 'Cancelled'
GROUP BY c.City
HAVING COUNT(o.OrderID) >= 2;

-- Revenue per customer from delivered orders
SELECT c.FullName, SUM(oi.Quantity * p.UnitPrice) AS Revenue
FROM Customers c
JOIN Orders o      ON o.CustomerID = c.CustomerID
JOIN OrderItems oi ON oi.OrderID = o.OrderID
JOIN Products p    ON p.ProductID = oi.ProductID
WHERE o.Status = 'Delivered'
GROUP BY c.FullName
ORDER BY Revenue DESC;
