#!/usr/bin/env python3

import csv
import os
import sys
import subprocess

if len(sys.argv) == 1:
    print("Error: No arguments provided!")
    sys.exit(1)

path = os.getcwd()
if not os.path.isdir(os.path.join(path, 'MP-SPDZ')):
    print("The 'MP-SPDZ' directory does not exist. Please make sure you are in the correct directory.")
    sys.exit(1)

print("Running performance test for plain queries")

num_tests = int(sys.argv[1])
query = "comorbidity"
out_file = os.path.join(path, "results", "measurements", "comorbidity_plain.txt")

if os.path.exists(out_file):
    os.remove(out_file)

rows = [1000, 2000, 4000, 6000, 8000, 10000, 20000, 40000, 60000, 80000, 100000, 200000, 400000, 600000, 800000, 1000000]

with open(f"{path}/results/measurements/{query}_plain.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Number of rows", "Execution time"])
    for max_rows in rows:
        total_preprocessing_time = 0.0
        total_execution_time = 0.0
        for i in range(1, num_tests + 1):
            populate_script = os.path.join(path, "code", "populate.py")
            populate_command = ["python3", populate_script, "secure", str(max_rows)]
            subprocess.run(populate_command)

            query_script = os.path.join(path, "code", "queries", "plain", f"{query}.py")
            query_command = ["python3", query_script, str(max_rows)]
            output = subprocess.check_output(query_command, universal_newlines=True)

            execution_time = float(output.split(': ')[1])
            total_execution_time += execution_time

        average_execution_time = total_execution_time / num_tests

        writer.writerow([max_rows, average_execution_time])