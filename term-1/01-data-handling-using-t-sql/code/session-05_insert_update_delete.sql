-- INSERT a single row, naming the columns (best practice)
INSERT INTO Products (ProductID, ProductName, Category, UnitPrice, Stock)
VALUES (107, 'Webcam HD', 'Accessories', 6500, 12);

-- INSERT several rows at once
INSERT INTO Customers (CustomerID, FullName, City, Email, JoinDate) VALUES
 (7, 'Mahnoor Ali', 'Hyderabad', 'mahnoor@mail.com', '2025-04-01'),
 (8, 'Saad Qureshi', 'Karachi', NULL, '2025-04-03');

-- INSERT ... SELECT: copy rows from a query into another table
CREATE TABLE KarachiCustomers (CustomerID INT, FullName VARCHAR(50));
INSERT INTO KarachiCustomers (CustomerID, FullName)
SELECT CustomerID, FullName FROM Customers WHERE City = 'Karachi';
SELECT * FROM KarachiCustomers;

-- UPDATE with a WHERE clause: 10% price rise for accessories
UPDATE Products SET UnitPrice = UnitPrice * 1.10 WHERE Category = 'Accessories';
SELECT ProductName, UnitPrice FROM Products WHERE Category = 'Accessories';

-- UPDATE several columns
UPDATE Customers SET Email = 'saad.q@mail.com', City = 'Karachi' WHERE CustomerID = 8;

-- UPDATE using another table: mark orders of Lahore customers as 'Priority'
UPDATE Orders SET Status = 'Priority'
WHERE CustomerID IN (SELECT CustomerID FROM Customers WHERE City = 'Lahore')
  AND Status = 'Delivered';
SELECT OrderID, CustomerID, Status FROM Orders;

-- DELETE specific rows
DELETE FROM OrderItems WHERE OrderID = 1006;
DELETE FROM Orders WHERE Status = 'Cancelled';
SELECT COUNT(*) AS OrdersLeft FROM Orders;
