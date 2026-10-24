-- Cities where we have customers vs. a list of cities with branches
CREATE TABLE Branches (City VARCHAR(30));
INSERT INTO Branches VALUES ('Karachi'), ('Lahore'), ('Multan');

SELECT City FROM Customers UNION     SELECT City FROM Branches ORDER BY City;  -- no duplicates
SELECT City FROM Customers UNION ALL SELECT City FROM Branches;               -- keeps duplicates
SELECT City FROM Customers INTERSECT SELECT City FROM Branches;               -- in both
SELECT City FROM Branches  EXCEPT    SELECT City FROM Customers;              -- branch with no customers
