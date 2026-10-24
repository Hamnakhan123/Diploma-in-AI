-- Today's stock feed from the warehouse
CREATE TABLE StockFeed (ProductID INT PRIMARY KEY, ProductName VARCHAR(50), Stock INT);
INSERT INTO StockFeed VALUES
 (101, 'Wireless Mouse', 55),     -- existing product, new stock level
 (105, 'Laptop Stand', 20),       -- existing product, back in stock
 (108, 'Portable SSD 1TB', 10);   -- brand-new product

-- SQLite / PostgreSQL "upsert" (the MERGE idea): insert, or update on key conflict
INSERT INTO Products (ProductID, ProductName, Category, UnitPrice, Stock)
SELECT ProductID, ProductName, 'New Arrivals', 0, Stock FROM StockFeed WHERE true
ON CONFLICT(ProductID) DO UPDATE SET Stock = excluded.Stock;

SELECT ProductID, ProductName, Category, Stock FROM Products ORDER BY ProductID;
