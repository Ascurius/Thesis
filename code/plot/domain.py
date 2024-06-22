import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import ScalarFormatter

# Set the metric to be plotted
metric = "rounds"

# Get current working directory
pwd = os.getcwd()

# Load data
binary = pd.read_csv(f"{pwd}/measurements/results/domains/binary.csv", delimiter=",")
prime = pd.read_csv(f"{pwd}/measurements/results/domains/prime.csv", delimiter=",")
ring = pd.read_csv(f"{pwd}/measurements/results/domains/ring.csv", delimiter=",")

# Plotting
plt.figure(figsize=(12, 6))  # Adjust size of the plot as needed

# Plot each series
line_binary, = plt.plot(binary["rows"], binary[metric], marker='o', linestyle='-', color='b', label='Binary')
line_prime, = plt.plot(prime["rows"], prime[metric], marker='o', linestyle='-', color='g', label='Modulo Prime')
line_ring, = plt.plot(ring["rows"], ring[metric], marker='o', linestyle='-', color='r', label='Modulo 2^k')

# Calculate max values for each series
max_values = {
    'Binary': binary[metric].max(),
    'Modulo Prime': prime[metric].max(),
    'Modulo 2^k': ring[metric].max()
}

# Sort the labels by max values
sorted_labels = sorted(max_values, key=max_values.get, reverse=True)

# Create legend handles in sorted order
handles = {
    'Binary': line_binary,
    'Modulo Prime': line_prime,
    'Modulo 2^k': line_ring
}
sorted_handles = [handles[label] for label in sorted_labels]

# Add labels and title
plt.xlabel('Number of Rows')
# plt.xscale('log')
plt.ylabel('Rounds')
# plt.yscale('log')
plt.title('Rounds per Rows')

# Add sorted legend
plt.legend(sorted_handles, sorted_labels)

plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='plain', axis='x')

# Show grid
plt.grid(True)

# Save and show plot
plt.savefig(f'./measurements/plot/domains_{metric}.png')
plt.show()
