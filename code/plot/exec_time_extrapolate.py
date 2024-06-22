import os
import csv
from pprint import pprint
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import linregress
from scipy.interpolate import interp1d

pwd = os.getcwd()

# Read the data for plain and secure
query = 'comorbidity'
plain = pd.read_csv(f"{pwd}/measurements/results/{query}_plain.txt", delimiter=",")
secure = pd.read_csv(f"{pwd}/measurements/results/{query}_secure.txt", delimiter=",")
sql = pd.read_csv(f"{pwd}/measurements/results/{query}_db.txt", header=None, names=['rows', 'time'])

# Perform linear regression
slope, intercept, _, _, _ = linregress(np.log(secure['rows']), np.log(secure['total']))

# Extrapolate for additional data points
extrapolated_data_points = [
    slope * 400000 + intercept,
    slope * 600000 + intercept,
    slope * 800000 + intercept,
    slope * 1000000 + intercept
]

extra_data = {
    "rows": [400000, 600000, 800000, 1000000],
    "total": extrapolated_data_points
}

# Create a new DataFrame with the new data
extra_df = pd.DataFrame(extra_data)

# Add missing columns with NaN or a default value
extra_df["data_sent"] = np.nan
extra_df["round"] = np.nan
extra_df["global_data_sent"] = np.nan

# Reorder columns to match the existing DataFrame
extra_df = extra_df[["rows", "total", "data_sent", "round", "global_data_sent"]]

# Append the new data to the existing DataFrame
secure = secure._append(extra_df, ignore_index=True)

# Plotting
plt.figure(figsize=(12, 6))  # Adjust size of the plot as needed

# Plot for plain
line_plain, = plt.plot(plain['rows'], plain['total'], marker='o', linestyle='-', color='b', label='Python')

# Plot for secure
line_secure_1, = plt.plot(secure["rows"][:13], secure["total"][:13], marker='o', linestyle='-', label='MP-SPDZ', color="g")
line_secure_2, = plt.plot(secure["rows"][12:], secure["total"][12:], marker='o', linestyle=':', color='g')

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

plt.savefig(f'./measurements/plot/{query}_exec_time.png')
plt.show()
