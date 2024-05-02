#!/bin/bash

#run from smcql home, which contains src/ 
path=$(pwd)
echo "Using test data from $path"

if [ ! -d "$path/testData" ]; then
  echo "Running from incorrect directory. Please run from project home directory."
  exit
fi

echo "Creating test database..."

dbPrefix='thesis'
duckdb "$path/thesis.duckdb" -c ".read $path/testData/test_schema.sql"

for i in 1 2
do
    dbName=$dbPrefix'_site'$i
    duckdb "$path/$dbName.duckdb" -c ".read $path/testData/test_schema.sql"
    duckdb "$path/$dbName.duckdb" -c "COPY diagnoses FROM '$path/testData/$i/diagnoses.csv' WITH DELIMITER ','"
    duckdb "$path/$dbName.duckdb" -c "COPY medications FROM '$path/testData/$i/medications.csv' WITH DELIMITER ','"
    duckdb "$path/$dbName.duckdb" -c "COPY site FROM '$path/testData/$i/site.csv' WITH DELIMITER ','"

    val=$i
    if (($val == 1)); then
        duckdb "$path/$dbName.duckdb" -c "COPY remote_diagnoses FROM '$path/testData/2/diagnoses.csv' WITH DELIMITER ','"
    else
        duckdb "$path/$dbName.duckdb" -c "COPY remote_diagnoses FROM '$path/testData/1/diagnoses.csv' WITH DELIMITER ','"
    fi
    duckdb "$path/$dbName.duckdb" -c "CREATE TABLE remote_cdiff_cohort_diagnoses AS (SELECT * FROM remote_diagnoses WHERE icd9='008.45')"
    duckdb "$path/$dbName.duckdb" -c "CREATE TABLE remote_mi_cohort_diagnoses AS (SELECT * FROM remote_diagnoses WHERE icd9 like '414%')"
    duckdb "$path/$dbName.duckdb" -c "CREATE TABLE remote_mi_cohort_medications AS (SELECT * FROM remote_medications WHERE lower(medication) like '%aspirin%')"

    duckdb "$path/$dbName.duckdb" -c ".read $path/testData/setup_test_registries.sql"
done

# psql -lqt | cut -d \| -f 1 | grep -qw $dbPrefix
# res0=$?
# psql -lqt | cut -d \| -f 1 | grep -qw $dbPrefix'_site1'
# res1=$?
# psql -lqt | cut -d \| -f 1 | grep -qw $dbPrefix'_site2'
# res2=$?

# if (($res0 == 0)) && (($res1 == 0)) && (($res2 == 0)); then
#     exit 0
# else
#     exit 1
# fi
