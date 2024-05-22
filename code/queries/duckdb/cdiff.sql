WITH diags (field0, field2, r) AS (
    SELECT field0,field2, row_number() OVER (PARTITION BY field0 ORDER BY field2) AS r
    FROM table1
    WHERE field8 == 8
)
SELECT DISTINCT a.field0
    FROM diags a JOIN diags b ON a.field0 == b.field0
    WHERE abs(a.field2 - b.field2) >= 15 
    AND abs(a.field2 - b.field2) <= 56 AND a.r+1 = b.r