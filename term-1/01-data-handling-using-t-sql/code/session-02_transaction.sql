-- A transfer that must be all-or-nothing
CREATE TABLE Wallet (Owner VARCHAR(20) PRIMARY KEY, Balance INT CHECK (Balance >= 0));
INSERT INTO Wallet VALUES ('Ayesha', 5000), ('Bilal', 1000);

-- 1) A successful transaction
BEGIN TRANSACTION;
UPDATE Wallet SET Balance = Balance - 2000 WHERE Owner = 'Ayesha';
UPDATE Wallet SET Balance = Balance + 2000 WHERE Owner = 'Bilal';
COMMIT;
SELECT * FROM Wallet;

-- 2) A transaction we cancel
BEGIN TRANSACTION;
UPDATE Wallet SET Balance = 0 WHERE Owner = 'Bilal';
ROLLBACK;
SELECT * FROM Wallet;

-- 3) A rule violation: Bilal cannot go below zero
UPDATE Wallet SET Balance = Balance - 99999 WHERE Owner = 'Bilal';
SELECT * FROM Wallet;
