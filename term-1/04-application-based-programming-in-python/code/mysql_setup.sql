-- Session 10 · Creating a database and a table with the MySQL command-line client
-- Start the client:   mysql -u root -p          (type your password when asked)
-- Then run these statements one by one, or:  mysql -u root -p < mysql_setup.sql

CREATE DATABASE IF NOT EXISTS campus CHARACTER SET utf8mb4;
SHOW DATABASES;
USE campus;

CREATE TABLE IF NOT EXISTS students (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    roll    VARCHAR(12)  NOT NULL UNIQUE,
    name    VARCHAR(60)  NOT NULL,
    city    VARCHAR(30)  DEFAULT 'Karachi',
    cgpa    DECIMAL(3,2) CHECK (cgpa BETWEEN 0 AND 4),
    created TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
DESCRIBE students;

INSERT INTO students (roll, name, city, cgpa) VALUES
    ('AI-01', 'Ali Khan', 'Karachi', 3.10),
    ('AI-02', 'Sana Tariq', 'Lahore', 3.80);
SELECT * FROM students;

-- A dedicated user for the Python app (never connect apps as root)
CREATE USER IF NOT EXISTS 'campus_app'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT SELECT, INSERT, UPDATE, DELETE ON campus.* TO 'campus_app'@'localhost';
FLUSH PRIVILEGES;
