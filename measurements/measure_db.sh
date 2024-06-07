#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments provided. Make sure you specify the name of the query to be measured."
    exit 1
fi

path=$(pwd)
query=$1
query_path="$path/code/queries/duckdb/$query.sql"
num_tests=5
out_file="$path/measurements/results/${query}_db.txt"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"
    echo "Generating test data..."
    python3 "$path/code/populate.py" "secure" "$max_row"

    # Create the database and its contents
    query=$(cat "$query_path")
    cd "duckdb"
    echo "Fill reference table with test data..."
    ./setup_reference_table.sh
    echo "Analyzing the query..."
    analysis=$(duckdb "./thesis.duckdb" -c "EXPLAIN ANALYZE $query")

    # Extract total time using regex
    if [[ $analysis =~ Total\ Time:\ ([0-9]+\.[0-9]+)s ]]; then
        total_time="${BASH_REMATCH[1]}"
        echo "$max_row,$total_time" >> $out_file
    else
        echo "Total Time not found."
        exit 1
    fi
    cd ..
done