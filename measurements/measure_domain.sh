#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments provided. Make sure you specify the name of the query to be measured."
    exit 1
fi

path=$(pwd)
domain=$1
query_path="$path/code/test.py"
n_tests=5
out_file="$path/measurements/results/domains/${domain}.csv"

if [ ! -f "$query_path" ]; then
    echo "Query file '$query_path' could not be found!"
    exit 1
fi

echo "Running performance test for secure query: $domain"

# # -- Generate new test data
echo "Generating test data..."
# python3 "$path/code/populate.py" "secure" "1000000"

case "$1" in
    binary)
        compile_option="-B"
        execute_script="replicated.sh"
        ;;
    prime)
        compile_option="-F"
        execute_script="rep-field.sh"
        ;;
    ring)
        compile_option="-R"
        execute_script="ring.sh"
        ;;
esac

rows=(100 200 300 400 500 600 700 800 900 1000)
for max_row in "${rows[@]}"; do
    echo "Measure performance for $max_row rows"

    # # -- Modify the high-level program
    sed -i -r "s/(max_rows\s*=\s*)[0-9]+/\1$max_row/" $query_path

    # -- Change to MP-SPDZ and compile the program
    cd "MP-SPDZ" # Compiling and execution must be done from within the MP-SPDZ directory
    echo "Compiling high-level code..."
    python3 "./compile.py" $compile_option 64 $query_path >/dev/null
    echo "Executing the program..."
    # Initialize variables to accumulate the values
    total_execution_time=0
    total_data_sent=0
    total_rounds=0
    total_global_sent=0

    # Run the command n times and accumulate the values
    for ((i=1; i<=$n_tests; i++))
    do
        output=$(eval "$path/MP-SPDZ/Scripts/$execute_script test") # Execute the query
        
        # Extract relevant lines
        time_line=$(echo "$output" | grep "Time =")
        data_line=$(echo "$output" | grep "Data sent =")
        global_line=$(echo "$output" | grep "Global data sent =")

        # Extract values using sed
        execution_time=$(echo "$time_line" | sed -n 's/Time = \([0-9\.]*\).*/\1/p')
        data_sent=$(echo "$data_line" | sed -n 's/Data sent = \([0-9\.]*\).*/\1/p')
        rounds=$(echo "$data_line" | sed -n 's/.*~\([0-9]*\).*/\1/p')
        global_sent=$(echo "$global_line" | sed -n 's/Global data sent = \([0-9\.]*\).*/\1/p')

        # Accumulate the values
        total_execution_time=$(echo "$total_execution_time + $execution_time" | bc)
        total_data_sent=$(echo "$total_data_sent + $data_sent" | bc)
        total_rounds=$(echo "$total_rounds + $rounds" | bc)
        total_global_sent=$(echo "$total_global_sent + $global_sent" | bc)
    done

    # Compute the averages
    avg_execution_time=$(echo "scale=6; $total_execution_time / $n_tests" | bc)
    avg_data_sent=$(echo "scale=6; $total_data_sent / $n_tests" | bc)
    avg_rounds=$(echo "scale=0; $total_rounds / $n_tests" | bc)
    avg_global_sent=$(echo "scale=6; $total_global_sent / $n_tests" | bc)

    echo "$max_row,$avg_execution_time,$avg_data_sent,$avg_rounds,$avg_global_sent" >> $out_file # Store the result of the execution in a text file
    echo "Done"
    cd ..
done