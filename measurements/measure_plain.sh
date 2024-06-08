#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments provided. Make sure you specify the name of the query to be measured."
    exit 1
fi

path=$(pwd)
query=$1
query_path="$path/code/queries/plain/$query.py"
num_tests=5
out_file="$path/measurements/results/${query}_plain.txt"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

echo "Running performance test for plain query: $query"

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
for max_rows in "${rows[@]}"; do
    echo "Performance test for $max_rows rows"
    total_execution_time=0.0
    for ((i=1; i<=$num_tests; i++)); do
        populate_script="$path/code/populate.py"
        echo "Generating test data..."
        python3 "$populate_script" "secure" "$max_rows"

        output=$(python3 "$query_path" "$max_rows")
        execution_time=$(echo "$output" | awk -F': ' '{print $2}')
        total_execution_time=$(echo "$total_execution_time + $execution_time" | bc)
    done

    average_execution_time=$(echo "scale=6; ($total_execution_time / $num_tests)" | bc)

    echo "$max_rows, $average_execution_time" >> $out_file

    echo "Done"
done