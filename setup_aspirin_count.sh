cd duckdb
duckdb thesis.duckdb -c "DROP TABLE table1;"
duckdb thesis.duckdb -c "DROP TABLE table2;"

duckdb thesis.duckdb -c "CREATE TABLE table1 (
field0 INT,
field1 INT,
field2 INT,
field3 INT,
field4 INT,
field5 INT,
field6 INT,
field7 INT,
field8 INT,
field9 INT,
field10 BIGINT,
field11 INT,
field12 INT
);"

duckdb thesis.duckdb -c "CREATE TABLE table2 (
field0 INT,
field1 INT,
field2 INT,
field3 INT,
field4 INT,
field5 INT,
field6 INT,
field7 INT,
field8 INT,
field9 INT,
field10 BIGINT,
field11 INT,
field12 INT
);"

duckdb thesis.duckdb -c "COPY table1 FROM '../MP-SPDZ/Player-Data/Input-P0-0' (DELIMITER ' ', HEADER FALSE);"
duckdb thesis.duckdb -c "COPY table2 FROM '../MP-SPDZ/Player-Data/Input-P1-0' (DELIMITER ' ', HEADER FALSE);"