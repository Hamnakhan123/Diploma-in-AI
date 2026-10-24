-- How many rows does each table hold?
SELECT 'Customers' AS TableName, COUNT(*) AS TotalRows FROM Customers
UNION ALL SELECT 'Products', COUNT(*) FROM Products
UNION ALL SELECT 'Orders', COUNT(*) FROM Orders
UNION ALL SELECT 'OrderItems', COUNT(*) FROM OrderItems
UNION ALL SELECT 'Employees', COUNT(*) FROM Employees;

-- Peek at the first three products
SELECT ProductID, ProductName, UnitPrice FROM Products LIMIT 3;
