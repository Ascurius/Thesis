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
query = "aspirin_count"

plain_rows, plain_times = read_plain(f"{pwd}/results/measurements/{query}_plain.txt")
secure_rows, secure_times = read_plain(f"{pwd}/results/measurements/{query}_secure.txt")
sql_rows, sql_times = read_plain(f"{pwd}/results/measurements/{query}_db.txt")

# Perform linear regression
slope, intercept, _, _, _ = linregress(np.log(secure_rows), np.log(secure_times))

# Extrapolate for additional data points
extrapolated_data_points = [
    slope * 400000 + intercept,
    slope * 600000 + intercept,
    slope * 800000 + intercept,
    slope * 1000000 + intercept
]
secure_rows.extend([400000, 600000, 800000, 1000000])
secure_times.extend(extrapolated_data_points)

# Data for SQL query

plt.figure(figsize=(10, 6))

# Plotting plain query
plt.plot(plain_rows, plain_times, marker='o', label='Python')

# Plotting secure query
# plt.plot(secure_rows, secure_times, marker='o', linestyle='-', label='MP-SPDZ')
plt.plot(secure_rows[:13], secure_times[:13], marker='o', linestyle='-', label='MP-SPDZ')
plt.plot(secure_rows[12:], secure_times[12:], marker='o', linestyle=':', color='orange')


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
plt.savefig('./results/img/query_time_comparison.png')