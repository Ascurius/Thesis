import os
import csv
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def read_plain(filename):
    left_column = []
    right_column = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            left_column.append(int(parts[0]))
            right_column.append(float(parts[1]))
    return left_column, right_column

pwd = os.getcwd()
query = "comorbidity"

plain_rows, plain_times = read_plain(f"{pwd}/results/measurements/{query}_plain.txt")
secure_rows, secure_times = read_plain(f"{pwd}/results/measurements/{query}_secure.txt")
sql_rows, sql_times = read_plain(f"{pwd}/results/measurements/{query}_db.txt")

# Perform linear regression
slope, intercept, _, _, _ = linregress(np.log(secure_rows), np.log(secure_times))

# Extrapolate the next data point (1,000,000 rows)
next_row = 1000000
next_time = np.exp(intercept + slope * np.log(next_row))
secure_rows.append(next_row)
secure_times.append(next_time)

# Data for SQL query

plt.figure(figsize=(10, 6))

# Plotting plain query
plt.plot(plain_rows, plain_times, marker='o', label='Python')

# Plotting secure query
plt.plot(secure_rows[:3], secure_times[:3], marker='o', linestyle='-', label='MP-SPDZ')
plt.plot(secure_rows[2:], secure_times[2:], marker='o', linestyle=':', color='orange')


# Plotting SQL query
plt.plot(sql_rows, sql_times, marker='o', label='DuckDB')

plt.title('Query Time Comparison')
plt.xlabel('Number of Rows')
plt.ylabel('Query Time (s)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.legend()
# plt.legend(['Measured Data', 'Extrapolated Data'], loc='upper left')
plt.tight_layout()
plt.savefig('query_time_comparison.png')