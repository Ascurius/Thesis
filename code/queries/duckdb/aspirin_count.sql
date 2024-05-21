select COUNT(DISTINCT a.field0)
FROM table1 a JOIN table2 b on a.field1 == b.field1
WHERE a.field8 == 414 AND b.field4 == 0 AND a.field2 <= b.field2;