#!/bin/bash

# Check if the current directory is "duckdb"
if [[ $(basename "$(pwd)") == "duckdb" ]]; then
  # Check for sibling directory "MP-SPDZ"
  if [[ ! -d "../MP-SPDZ" ]]; then
    echo "Script is running from duckdb directory but sibling directory MP-SPDZ not found."
    exit 1
  fi
else
  echo "Script is not running from the duckdb directory!"
  exit 2
fi

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