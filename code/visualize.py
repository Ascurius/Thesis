import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def read_plain(filename):
    rows = []
    query_times = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            rows.append(int(row[0]))
            query_times.append(float(row[1]))

    return rows, query_times

pwd = os.getcwd()
query = "comorbidity"

# Data for plain query
filename_plain = f"{pwd}/measurements/"
plain_rows, plain_times = read_plain(filename_plain)

# Data for secure query
secure_rows = [1000, 10000, 100000]
secure_times = [0.04807, 1.36505, 17.435]

# Perform linear regression
slope, intercept, _, _, _ = linregress(np.log(secure_rows), np.log(secure_times))

# Extrapolate the next data point (1,000,000 rows)
next_row = 1000000
next_time = np.exp(intercept + slope * np.log(next_row))
secure_rows.append(next_row)
secure_times.append(next_time)

# Data for SQL query
sql_rows = [1000, 10000, 100000, 1000000]
sql_times = [0.0055, 0.0058, 0.0110, 0.0144]

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
plt.legend(['Measured Data', 'Extrapolated Data'], loc='upper left')
plt.tight_layout()
plt.savefig('query_time_comparison.png')