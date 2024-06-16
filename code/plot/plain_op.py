import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

pwd = os.getcwd()
query = "comorbidity"

times = pd.read_csv(f"{pwd}/measurements/results/{query}_plain.txt", delimiter=",")
if "total" in times.columns:
    times = times.drop(columns=["total"])

plt.figure(figsize=(12, 8))

# Plot each operator's time against the number of rows
for column in times.columns[1:]:
    plt.plot(times['rows'], times[column], label=column)

plt.xlabel('Number of rows')
plt.ylabel('Time (seconds)')
plt.title(f'Operator execution time in {query}')
plt.legend()
# plt.yscale('log')
plt.grid(True)

# Save the plot to a file
output_path = f"{pwd}/measurements/plot/{query}_operators_plain.png"
plt.savefig(output_path)