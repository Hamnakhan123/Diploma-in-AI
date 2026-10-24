-- Sample "Karachi Gadget Store" database used across this module.
-- Written in portable SQL (runs on SQL Server and SQLite).
CREATE TABLE Customers (
    CustomerID   INT PRIMARY KEY,
    FullName     VARCHAR(50) NOT NULL,
    City         VARCHAR(30),
    Email        VARCHAR(60),
    JoinDate     DATE
);
CREATE TABLE Products (
    ProductID    INT PRIMARY KEY,
    ProductName  VARCHAR(50) NOT NULL,
    Category     VARCHAR(30),
    UnitPrice    DECIMAL(10,2),
    Stock        INT
);
CREATE TABLE Orders (
    OrderID      INT PRIMARY KEY,
    CustomerID   INT REFERENCES Customers(CustomerID),
    OrderDate    DATE,
    Status       VARCHAR(15)
);
CREATE TABLE OrderItems (
    OrderID      INT REFERENCES Orders(OrderID),
    ProductID    INT REFERENCES Products(ProductID),
    Quantity     INT,
    PRIMARY KEY (OrderID, ProductID)
);
CREATE TABLE Employees (
    EmpID        INT PRIMARY KEY,
    EmpName      VARCHAR(40),
    Title        VARCHAR(30),
    ManagerID    INT NULL REFERENCES Employees(EmpID),
    Salary       DECIMAL(10,2)
);

INSERT INTO Customers VALUES
 (1,'Ayesha Khan','Karachi','ayesha@mail.com','2024-01-15'),
 (2,'Bilal Ahmed','Lahore','bilal@mail.com','2024-03-02'),
 (3,'Sana Malik','Karachi',NULL,'2024-05-20'),
 (4,'Usman Tariq','Islamabad','usman@mail.com','2024-07-11'),
 (5,'Hira Siddiqui','Karachi','hira@mail.com','2025-01-08'),
 (6,'Zain Raza','Lahore',NULL,'2025-02-14');

INSERT INTO Products VALUES
 (101,'Wireless Mouse','Accessories',1500.00,40),
 (102,'Mechanical Keyboard','Accessories',8500.00,15),
 (103,'27-inch Monitor','Displays',52000.00,6),
 (104,'USB-C Hub','Accessories',4200.00,25),
 (105,'Laptop Stand','Furniture',3500.00,0),
 (106,'Noise-Cancel Headset','Audio',18000.00,9);

INSERT INTO Orders VALUES
 (1001,1,'2025-03-01','Delivered'),
 (1002,2,'2025-03-03','Delivered'),
 (1003,1,'2025-03-10','Shipped'),
 (1004,3,'2025-03-12','Pending'),
 (1005,4,'2025-03-15','Delivered'),
 (1006,5,'2025-03-18','Cancelled');

INSERT INTO OrderItems VALUES
 (1001,101,2),(1001,104,1),
 (1002,103,1),
 (1003,102,1),(1003,106,1),
 (1004,101,1),
 (1005,103,2),(1005,101,3),
 (1006,105,1);

INSERT INTO Employees VALUES
 (1,'Farah Naz','Store Manager',NULL,250000),
 (2,'Kamran Ali','Sales Lead',1,140000),
 (3,'Nida Hussain','Sales Associate',2,85000),
 (4,'Omer Shah','Sales Associate',2,82000),
 (5,'Rabia Noor','Inventory Lead',1,130000);
