SELECT t.field1, count(*) as cnt 
FROM table1 t
GROUP BY t.field1
ORDER BY count(*) DESC 
LIMIT 10