#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments provided. Make sure you specify the name of the query to be measured."
    exit 1
fi

path=$(pwd)
query=$1
query_path="$path/code/queries/secure/$query.py"
n_tests=1
out_file="$path/measurements/results/${query}_secure.txt"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

echo "Running performance test for secure query: $query"

# # -- Generate new test data
echo "Generating test data..."
python3 "$path/code/populate.py" "secure" "1000000"

# rows=(100 200 300 400 500 600 700 800 900 1000 2000 4000 6000 8000 10000 20000 40000 60000 80000 100000 200000 400000 600000 800000 1000000)
rows=(100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000)
# rows=(100)
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"

    # # -- Modify the high-level program
    sed -i -r "s/(max_rows\s*=\s*)[0-9]+/\1$max_row/" $query_path

    # -- Change to MP-SPDZ and compile the program
    cd "MP-SPDZ" # Compiling and execution must be done from within the MP-SPDZ directory
    echo "Compiling high-level code..."
    python3 "./compile.py" -R 64 $query_path >/dev/null
    echo "Executing the program..."
    
    output=$(eval "$path/MP-SPDZ/Scripts/ring.sh $query") # Execute the query

    echo "$output"
    echo "Done"
    cd ..
done