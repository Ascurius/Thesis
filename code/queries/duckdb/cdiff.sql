WITH diags (field0, field10, r) AS (
    SELECT field0,field10, row_number() OVER (PARTITION BY field0 ORDER BY field10) AS r
    FROM table1
    WHERE field8 == 8
)
SELECT DISTINCT a.field0
    FROM diags a JOIN diags b ON a.field0 == b.field0
    WHERE datediff('day', a.field10, b.field10) >= 15 
    AND datediff('day', a.field10, b.field10) <= 56 AND a.r+1 = b.r