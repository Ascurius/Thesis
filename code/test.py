from pprint import pprint
import re
import duckdb

con = duckdb.connect("duckdb/thesis_site1.duckdb", read_only = True)

res = con.execute("""
EXPLAIN ANALYZE SELECT d.major_icd9, count(*) as cnt 
FROM cdiff_cohort_diagnoses d 
GROUP BY d.major_icd9 
ORDER BY count(*) DESC 
LIMIT 10
""").fetchall()

analysis = res[0][1]

total_time = re.search(r'Total Time: (\d+\.\d+)s', analysis).group(1)
print("Total Time:", total_time)

# Extract time for each operator block
# operator_blocks = re.findall(r'\n\s+(\w+) \(#?\d+\)\n\s+─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\s+\d+\s+\(\d+\.\d+s\)\s+', res)
# for operator in operator_blocks:
#     operator_time = re.search(r'\n\s+' + re.escape(operator) + r' \(#?\d+\)\n\s+─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\s+\d+\s+\((\d+\.\d+)s\)\s+', res).group(1)
#     print("Operator:", operator)
#     print("Time:", operator_time)

