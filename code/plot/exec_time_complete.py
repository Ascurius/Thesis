import os
import csv
from pprint import pprint
import sys
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import linregress
from scipy.interpolate import interp1d

pwd = os.getcwd()

# Read the data for plain and secure
query = sys.argv[1]
join_type = sys.argv[2] 
plain = pd.read_csv(f"{pwd}/measurements/results/{query}_plain_{join_type}_micro.txt", delimiter=",")
secure = pd.read_csv(f"{pwd}/measurements/results/{query}_secure.txt", delimiter=",")
sql = pd.read_csv(f"{pwd}/measurements/results/{query}_db_micro.txt", header=None, names=['rows', 'time'])

# Plotting
plt.figure(figsize=(12, 6))  # Adjust size of the plot as needed

# Plot for plain
line_plain, = plt.plot(plain['rows'], plain['total'], marker='o', linestyle='-', color='b', label='Python')

# Plot for secure
line_secure, = plt.plot(secure["rows"], secure["total"], marker='o', linestyle='-', label='MP-SPDZ', color="g")

# Plot for sql (DuckDB)
line_sql, = plt.plot(sql['rows'], sql['time'], marker='o', linestyle='-', color='r', label='SQL (DuckDB)')

# Add labels and title
plt.xlabel('Number of Rows')
plt.xscale('log')
plt.ylabel('Time (seconds)')
plt.yscale('log')
plt.title('Total Execution Time per Maximum Rows')

# Create custom legend handles
custom_legend_handles = [
    Line2D([0], [0], color='g', lw=2, label='MP-SPDZ'),
    Line2D([0], [0], color='b', lw=2, label='Python'),
    Line2D([0], [0], color='r', lw=2, label='SQL (DuckDB)')
]

# Add custom legend
plt.legend(handles=custom_legend_handles)

plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='plain', axis='x')

# Show grid
plt.grid(True)

plt.savefig(f'./measurements/plot/{query}_exec_time_complete.png')
plt.show()