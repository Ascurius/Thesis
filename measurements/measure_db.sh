#!/bin/bash

path=$(pwd)

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"
    # Fill the CSV files with dummy data
    echo "Generating test data..."
    python3 "$path/code/populate.py" "db" "$max_row"

    # Create the database and its contents
    query_name="comorbidity"
    query_file="$path/code/queries/sql/$query_name.sql"
    query=$(cat "$query_file")
    cd "duckdb"
    ./testData/duckdb-create_test_dbs.sh
    analysis=$(duckdb "./thesis_site1.duckdb" -c "EXPLAIN ANALYZE $query")

    # Extract total time using regex
    if [[ $analysis =~ Total\ Time:\ ([0-9]+\.[0-9]+)s ]]; then
        total_time="${BASH_REMATCH[1]}"
        echo "$max_row,$total_time" >> "../results/measurements/${query_name}_db.txt"
        # echo "Total Time: $total_time"
    else
        echo "Total Time not found."
        exit 1
    fi
    cd ..
done