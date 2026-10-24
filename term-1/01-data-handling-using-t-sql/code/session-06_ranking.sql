-- Ranking functions are window functions: OVER (ORDER BY ...)
SELECT ProductName, Category, UnitPrice,
       ROW_NUMBER() OVER (ORDER BY UnitPrice DESC)  AS RowNum,
       RANK()       OVER (ORDER BY Category)        AS RankByCat,
       DENSE_RANK() OVER (ORDER BY Category)        AS DenseRankByCat,
       NTILE(3)     OVER (ORDER BY UnitPrice DESC)  AS PriceBand
FROM Products;

-- PARTITION BY restarts the numbering for each group:
-- most expensive product in every category
SELECT Category, ProductName, UnitPrice FROM (
    SELECT Category, ProductName, UnitPrice,
           ROW_NUMBER() OVER (PARTITION BY Category ORDER BY UnitPrice DESC) AS rn
    FROM Products) t
WHERE rn = 1;
