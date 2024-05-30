WITH all_diagnoses AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
)
SELECT t.field1, count(*) as cnt 
FROM all_diagnoses t
GROUP BY t.field1
ORDER BY count(*) DESC 
LIMIT 10