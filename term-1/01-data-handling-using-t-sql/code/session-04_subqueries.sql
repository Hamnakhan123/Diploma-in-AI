-- Scalar subquery: products priced above the average price
SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products);

-- Multi-valued subquery with IN: customers who bought a monitor
SELECT FullName FROM Customers
WHERE CustomerID IN (
    SELECT o.CustomerID FROM Orders o
    JOIN OrderItems oi ON oi.OrderID = o.OrderID
    WHERE oi.ProductID = 103);

-- Correlated subquery with EXISTS: products that have never been ordered
SELECT ProductName FROM Products p
WHERE NOT EXISTS (SELECT 1 FROM OrderItems oi WHERE oi.ProductID = p.ProductID);

-- Subquery in SELECT: number of orders per customer
SELECT FullName,
       (SELECT COUNT(*) FROM Orders o WHERE o.CustomerID = c.CustomerID) AS OrderCount
FROM Customers c;

-- Derived table (subquery in FROM)
SELECT Status, AVG(Items) AS AvgItemsPerOrder
FROM (SELECT o.OrderID, o.Status, SUM(oi.Quantity) AS Items
      FROM Orders o JOIN OrderItems oi ON oi.OrderID = o.OrderID
      GROUP BY o.OrderID, o.Status) AS t
GROUP BY Status;
