#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments provided."
    exit 1
fi

path=$(pwd)
if [ ! -d "$path/MP-SPDZ" ]; then
    echo "The 'MP-SPDZ' directory does not exist. Please make sure you are in the correct directory."
    exit 1
fi

echo "Running performance test for plain queries"

num_tests=$1
query="comorbidity"
out_file="$path/results/measurements/comorbidity_plain.txt"

if [ -f "$out_file" ]; then
    rm "$out_file"
fi

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)

for max_rows in "${rows[@]}"; do
    echo "Performance test for $max_rows rows"
    total_execution_time=0.0
    for ((i=1; i<=$num_tests; i++)); do
        populate_script="$path/code/populate.py"
        python3 "$populate_script" "secure" "$max_rows"

        query_script="$path/code/queries/plain/${query}.py"
        output=$(python3 "$query_script" "$max_rows")
        execution_time=$(echo "$output" | awk -F': ' '{print $2}')
        total_execution_time=$(echo "$total_execution_time + $execution_time" | bc)
    done

    average_execution_time=$(echo "scale=6; ($total_execution_time / $num_tests)" | bc)

    echo "$max_rows, $average_execution_time" >> $out_file
done