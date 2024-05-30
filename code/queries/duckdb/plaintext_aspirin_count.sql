WITH union_x AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
), union_y AS (
    (SELECT * FROM table1)
    UNION ALL
    (SELECT * FROM table2)
)
select COUNT(DISTINCT a.field0)
FROM union_x a JOIN union_y b on a.field1 == b.field1
WHERE a.field8 == 414 AND b.field4 == 0 AND a.field2 <= b.field2;