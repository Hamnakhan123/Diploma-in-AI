-- DDL: define a structure
CREATE TABLE Students (
    StudentID  INT PRIMARY KEY,
    Name       VARCHAR(40) NOT NULL,
    Program    VARCHAR(30)
);

-- DML: put data in and read it back
INSERT INTO Students (StudentID, Name, Program) VALUES
 (1, 'Ali', 'AI'),
 (2, 'Maryam', 'Data Science'),
 (3, 'Hamza', 'AI');

SELECT * FROM Students;

SELECT Name FROM Students WHERE Program = 'AI';

-- DDL again: change the structure
ALTER TABLE Students ADD COLUMN City VARCHAR(30);
UPDATE Students SET City = 'Karachi';
SELECT StudentID, Name, City FROM Students;
