-- INNER JOIN: orders with the customer's name
SELECT o.OrderID, c.FullName, o.Status
FROM Orders AS o
INNER JOIN Customers AS c ON c.CustomerID = o.CustomerID;

-- Three tables: what did each order contain, and what was it worth?
SELECT o.OrderID, p.ProductName, oi.Quantity, oi.Quantity * p.UnitPrice AS LineTotal
FROM Orders o
JOIN OrderItems oi ON oi.OrderID = o.OrderID
JOIN Products  p  ON p.ProductID = oi.ProductID
WHERE o.Status = 'Delivered'
ORDER BY o.OrderID;

-- LEFT OUTER JOIN: every customer, even those who never ordered
SELECT c.FullName, o.OrderID
FROM Customers c
LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
ORDER BY c.CustomerID;

-- Anti-join pattern: customers with NO orders
SELECT c.FullName
FROM Customers c
LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
WHERE o.OrderID IS NULL;

-- CROSS JOIN: every size with every colour (Cartesian product)
CREATE TABLE Sizes (Size VARCHAR(5));   INSERT INTO Sizes VALUES ('S'),('M');
CREATE TABLE Colours (Colour VARCHAR(10)); INSERT INTO Colours VALUES ('Black'),('White'),('Red');
SELECT Size, Colour FROM Sizes CROSS JOIN Colours;

-- SELF JOIN: each employee with their manager
SELECT e.EmpName AS Employee, m.EmpName AS Manager
FROM Employees e
LEFT JOIN Employees m ON m.EmpID = e.ManagerID;
