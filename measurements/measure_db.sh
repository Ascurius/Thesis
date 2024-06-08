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
    total_execution_time=0.0
    for ((i=1; i<=$num_tests; i++)); do
        analysis=$(duckdb "./thesis.duckdb" -c "EXPLAIN ANALYZE $query")

        # Extract total time using regex
        if [[ $analysis =~ Total\ Time:\ ([0-9]+\.[0-9]+)s ]]; then
            execution_time="${BASH_REMATCH[1]}"
            total_execution_time=$(echo "$total_execution_time + $execution_time" | bc)
        else
            echo "Total Time not found."
            exit 1
        fi
    done

    average_execution_time=$(echo "scale=6; ($total_execution_time / $num_tests)" | bc)
    echo "$max_row, $average_execution_time" >> $out_file

    cd ..
done