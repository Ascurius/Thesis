#!/bin/bash

query=$1
extension="_secure.txt"
path=$(pwd)
query_path="$path/code/queries/secure/$query.py"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
echo "max_row,execution_time,data_sent,rounds,global_sent" >> "$path/measurements/results/test_$query$extension"
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"
    # # -- Generate new test data
    echo "Generating test data..."
    python3 "$path/code/populate.py" "secure" "$max_row"

    # # -- Modify the high-level program
    sed -i -r "s/(max_rows\s*=\s*)[0-9]+/\1$max_row/" $query_path

    # -- Change to MP-SPDZ and compile the program
    cd "MP-SPDZ" # Compiling and execution must be done from within the MP-SPDZ directory
    echo "Compiling high-level code..."
    python3 "./compile.py" -B 64 $query_path >/dev/null
    echo "Executing the program..."
    output=$(eval "$path/MP-SPDZ/Scripts/replicated.sh $query") # Execute the query

    # Extract relevant lines
    time_line=$(echo "$output" | grep "Time =")
    data_line=$(echo "$output" | grep "Data sent =")
    global_line=$(echo "$output" | grep "Global data sent =")

    # Extract values using sed
    execution_time=$(echo "$time_line" | sed -n 's/Time = \([0-9\.]*\).*/\1/p')
    data_sent=$(echo "$data_line" | sed -n 's/Data sent = \([0-9\.]*\).*/\1/p')
    rounds=$(echo "$data_line" | sed -n 's/.*~\([0-9]*\).*/\1/p')
    global_sent=$(echo "$global_line" | sed -n 's/Global data sent = \([0-9\.]*\).*/\1/p')

    echo "$max_row,$execution_time,$data_sent,$rounds,$global_sent" >> "$path/measurements/results/test_$query$extension" # Store the result of the execution in a text file
    echo "Done"
    cd ..
done