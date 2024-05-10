#!/bin/bash

query="comorbidity"
extension="_secure.txt"
path=$(pwd)

rows=(1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"
    # # -- Generate new test data
    echo "Generating test data..."
    python3 "$path/code/populate.py" "secure" "$max_row"

    # # -- Modify the high-level program
    sed -i "103s/sint.Matrix([0-9]*, p0_col)/sint.Matrix($max_row, p0_col)/" "code/main.py"


    # -- Change to MP-SPDZ and compile the program
    cd "MP-SPDZ" # Compiling and execution must be done from within the MP-SPDZ directory
    echo "Compiling high-level code..."
    python3 "./compile.py" -B 64 "../code/main.py" >/dev/null
    echo "Executing the program..."
    output=$(eval "./Scripts/replicated.sh main") # Execute the query
    execution_time=$(echo $output | grep -o 'Time = [0-9.]*' | awk '{print $3}') # Filter for the execution time only

    echo "$max_row,$execution_time" >> "../results/measurements/$query$extension" # Store the result of the execution in a text file
    echo "Done"
    cd ..
done