#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: script.sh <query> [start_max_rows]"
    exit 1
fi

path=$(pwd)
query=$1
start_max_rows=$2
query_path="$path/code/queries/plain/$query.py"
num_tests=5
out_file="$path/measurements/results/${query}_plain.txt"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

echo "Running performance test for plain query: $query"

# Write column headers to output file depending on query
base_header="rows,total_time"
if [ $query = "aspirin_count" ]; then
    header="$base_header,first_filter,second_filter,join,third_filter,distinct,distinct_sort,count"
elif [ $query = "cdiff" ]; then
    header="$base_header,first_filter,sort,partition_by,join,distinct,distinct_sort,count"
elif [ $query = "comorbidity" ]; then
    header="$base_header,group_by,order_by,limit"
fi
echo $header >> $out_file

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
# rows=(1000)
# Set default start_max_rows if not specified
if [ -z "$start_max_rows" ]; then
    start_max_rows=${rows[0]}
fi

# Find the starting index
start_index=-1
for i in "${!rows[@]}"; do
    if [ "${rows[$i]}" -eq "$start_max_rows" ]; then
        start_index=$i
        break
    fi
done

# Check if the specified start_max_rows is in the list
if [ $start_index -eq -1 ]; then
    echo "Specified start_max_rows '$start_max_rows' is not in the predefined list of rows."
    echo "Possible values are: ${rows[*]}"
    exit 1
fi

echo "Generating test data..."
populate_script="$path/code/populate.py"
python3 "$populate_script" "secure" "1000000"

for ((i=start_index; i<${#rows[@]}; i++)); do
    max_rows=${rows[i]}
    echo "Performance test for $max_rows rows"

    # total_execution_time=0.0
    total_times=()
    for ((j=1; j<=$num_tests; j++)); do
        output=$(python3 "$query_path" "$max_rows")
        
        # Extract times using grep and regex
        times=($(echo "$output" | grep -oP '\d+\.\d+'))

        # Accumulate the times for each test
        total_times+=("${times[@]}")
    done

    # Average each specific time over the number of tests
    average_times=()
    for ((k=0; k<${#times[@]}; k++)); do
        sum_time=0.0
        for ((j=0; j<$num_tests; j++)); do
            index=$((j * ${#times[@]} + k))
            sum_time=$(echo "$sum_time + ${total_times[$index]}" | bc)
        done
        avg_time=$(echo "scale=6; $sum_time / $num_tests" | bc)
        average_times+=("$avg_time")
    done

    # Only output as many times as currently present in the array:
    output_line="$max_rows"
    for ((index=0; index<${#average_times[@]}; index++)); do
        output_line+=",${average_times[index]}"
    done
    echo "$output_line" >> $out_file

    echo "Done"
done
