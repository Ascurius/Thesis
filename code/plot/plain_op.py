import csv
import os
import sys
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import matplotlib.pyplot as plt

pwd = os.getcwd()
query = sys.argv[1]
join_type = "n"

times = pd.read_csv(f"{pwd}/measurements/results/{query}_plain_{join_type}.txt", delimiter=",")
if "total" in times.columns:
    times = times.drop(columns=["total"])

plt.figure(figsize=(12, 8))

# Calculate the maximum value for each column (excluding the 'rows' column)
max_values = {column: times[column].max() for column in times.columns[1:]}

# Sort the columns based on the maximum values in descending order
sorted_columns = sorted(max_values, key=max_values.get, reverse=True)

# Plot each operator's time against the number of rows in the sorted order
lines = {}
for column in sorted_columns:
    line, = plt.plot(times['rows'], times[column], label=column, marker='o')
    lines[column] = line

plt.xlabel('Number of rows')
plt.ylabel('Time (seconds)')
plt.title(f'Python operator execution time of {query}')

# Create custom legend handles sorted by the maximum value of each series
sorted_handles = [lines[column] for column in sorted_columns]
sorted_labels = [column for column in sorted_columns]

plt.legend(sorted_handles, sorted_labels)
# plt.yscale('log')
plt.xscale('log')
plt.grid(True)

plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='plain', axis='x')

# Save the plot to a file
output_path = f"{pwd}/measurements/plot/{query}_operators_plain_{join_type}.png"
plt.savefig(output_path)
plt.show()
