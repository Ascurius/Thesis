WITH all_diagnoses AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
), all_medications AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
)
select COUNT(DISTINCT a.field0)
FROM all_diagnoses a JOIN all_medications b on a.field1 == b.field1
WHERE a.field8 == 414 AND b.field4 == 0 AND a.field2 <= b.field2;