WITH all_diagnoses AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
), 
diags (field1, field2, r) AS (
    SELECT field1,field2, row_number() OVER (PARTITION BY field1 ORDER BY field2) AS r
    FROM all_diagnoses
    WHERE field8 == 8
)
SELECT DISTINCT a.field1
    FROM diags a JOIN diags b ON a.field1 == b.field1
    WHERE abs(a.field2 - b.field2) >= 15 
    AND abs(a.field2 - b.field2) <= 56 AND a.r+1 = b.r