from collections import defaultdict
import csv
import os
from pprint import pprint
import re
import sys
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

aspirin_times = {
    'Time10': 'read_data',
    'Time100': 'first_filter',
    'Time200': 'second_filter',
    'Time300': 'join',
    'Time500': 'distinct',
    'Time600': 'distinct_sort',
    'Time1000': 'join_sort'
}
plaintext_aspirin_times = {
    'Time10': 'read_data',
    'Time100': 'union_all',
    'Time200': 'first_filter',
    'Time300': 'second_filter',
    'Time400': 'join',
    'Time600': 'distinct',
    'Time700': 'distinct_sort',
    'Time1000': 'join_sort'
}
cdiff_times = {
    'Time10': 'read_data',
    'Time100': 'first_filter',
    'Time200': 'correctness_sort',
    'Time300': 'row_number_over_partition_by',
    'Time400': 'join',
    'Time500': 'distinct',
    'Time600': 'distinct_sort'
}
plaintext_cdiff_times = {
    'Time10': 'read_data',
    'Time100': 'union_all',
    'Time200': 'first_filter',
    'Time300': 'correctness_sort',
    'Time400': 'row_number_over_partition_by',
    'Time500': 'join',
    'Time600': 'distinct',
    'Time700': 'distinct_sort'
}
comorbidity_times = {
    "Time100": "select_columns",
    "Time200": "group_by",
    "Time300": "group_by_sort",
    "Time400": "order_by",
    "Time500": "order_by_sort",
    "Time600": "limit"
}
plaintext_comorbidity_times = {
    "Time100": "union_all",
    "Time200": "select_columns",
    "Time300": "group_by",
    "Time400": "group_by_sort",
    "Time500": "order_by",
    "Time600": "order_by_sort",
    "Time700": "limit"
}


def parse_data(query):
    filename = f"./measurements/results/{query}/secure.txt"
    data = defaultdict(list)
    current_entry = {}
    current_join_type = None
    if query == "aspirin_count":
        timer_keys = aspirin_times
    elif query == "cdiff":
        timer_keys = cdiff_times
    elif query == "comorbidity":
        timer_keys = comorbidity_times
    elif query == "plaintext_aspirin_count":
        timer_keys = plaintext_aspirin_times
    elif query == "plaintext_cdiff":
        timer_keys = plaintext_cdiff_times
    elif query == "plaintext_comorbidity":
        timer_keys = plaintext_comorbidity_times
    
    join_type_pattern = re.compile(r'### (.+)')

    with open(filename, 'r') as file:
        for line in file:
            # Check for the start of a new join type
            match = join_type_pattern.match(line)
            if match:
                if current_entry and current_join_type:
                    data[current_join_type].append(current_entry)
                current_join_type = match.group(1).strip()
                current_entry = {}
                continue

            # Check for the start of a new measurement
            match = re.match(r'Measure performance for (\d+) rows', line)
            if match:
                if current_entry:
                    data[current_join_type].append(current_entry)
                current_entry = {'rows': match.group(1), "times":{}}
                continue
            
            # Extract total time
            match = re.match(r'Time\s*=\s*(\d+\.?\d+)', line)
            if match:
                current_entry['total_time'] = match.group(1)
                continue
            
            # Extract times for specific timers
            match = re.match(r'(Time\d*)\s*=\s*([\d\.]+(?:e[+-]?\d+)?)', line)
            if match:
                timer_key = match.group(1)
                timer_value = match.group(2)
                if timer_key in timer_keys:
                    current_entry["times"][timer_keys[timer_key]] = timer_value
                continue
            
            # Extract data sent and rounds
            match = re.match(r'Data sent\s*=\s*([\d.]+) MB in ~(\d+) rounds', line)
            if match:
                current_entry['data_sent'] = match.group(1)
                current_entry['rounds'] = match.group(2)
                continue
            
            # Extract global data sent
            match = re.match(r'Global data sent\s*=\s*([\d.]+) MB', line)
            if match:
                current_entry['global_data_sent'] = match.group(1)
                continue
        
        # Append the last entry
        if current_entry and current_join_type:
            data[current_join_type].append(current_entry)

    # Flatten the data and create a DataFrame
    dataframes_dict = {}
    
    for join_type, entries in data.items():
        flattened_data = []
        for entry in entries:
            row = {
                "rows": entry.get('rows'),
                "total_time": entry.get('total_time'),
                "data_sent": entry.get('data_sent'),
                "rounds": entry.get('rounds'),
                "global_data_sent": entry.get('global_data_sent')
            }
            row.update(entry.get('times', {}))  # Add times as separate columns
            flattened_data.append(row)
        
        # Convert to DataFrame and add to the dictionary
        dataframes_dict[join_type] = pd.DataFrame(flattened_data)
    
    return dataframes_dict

def extrapolate_specific_rows(data, target_rows):
    # Ensure 'rows' and 'total_time' are numeric
    data["rows"] = pd.to_numeric(data["rows"], errors='coerce')
    data["total_time"] = pd.to_numeric(data["total_time"], errors='coerce')

    # Logarithmic transformation for linear regression
    data['log_rows'] = np.log(data['rows'])
    data['log_total'] = np.log(data['total_time'])

    # Perform linear regression on log-log data
    coefficients = np.polyfit(data['log_rows'], data['log_total'], 1)
    slope, intercept = coefficients

    # Predict for the given row counts
    predicted_rows = np.array(target_rows)
    predicted_total_log = slope * np.log(predicted_rows) + intercept
    predicted_total = np.exp(predicted_total_log)

    # Prepare the result in a DataFrame
    result = pd.DataFrame({
        "rows": predicted_rows,
        "total_time": predicted_total
    })

    # Append the new extrapolated data to the original dataset and sort
    secure_full = pd.concat([data, result]).drop_duplicates(subset=["rows"]).sort_values(by="rows").reset_index(drop=True)

    return secure_full

query = "comorbidity"
domain = "binary"

secure = parse_data(query)[domain]
plain = pd.read_csv(f"./measurements/results/{query}/plain.txt")
db = pd.read_csv(f"./measurements/results/{query}/db.txt", header=None, names=['Rows', 'Time'], skipinitialspace=True)

if len(secure["rows"]) < 34:
    secure = extrapolate_specific_rows(secure, target_rows=[400000, 600000, 800000, 1000000])
else:
    secure["rows"] = pd.to_numeric(secure["rows"], errors='coerce')
    secure["total_time"] = pd.to_numeric(secure["total_time"], errors='coerce')

# print("Secure Data Ranges:")
# print("Rows:", secure["rows"].min(), "-", secure["rows"].max())
# print("Total Time:", secure["total_time"].min(), "-", secure["total_time"].max())

# print("Plain Data Ranges:")
# print("Rows:", plain["rows"].min(), "-", plain["rows"].max())
# print("Total Time:", plain["total"].min(), "-", plain["total"].max())

# print("DB Data Ranges:")
# print("Rows:", db["Rows"].min(), "-", db["Rows"].max())
# print("Total Time:", db["Time"].min(), "-", db["Time"].max())

# sp = (sum(secure["total_time"]) / len(secure["total_time"])) / (sum(plain['total']) / len(plain['total']))
# sd = (sum(secure["total_time"]) / len(secure["total_time"])) / (sum(db['Time']) / len(db['Time']))

# print("Factor secure-plain", sp)
# print("Factor secure-db", sd)

plt.figure(figsize=(10, 6))

if len(secure["rows"]) < 34:
    plt.plot(secure["rows"][len(secure)-5:], secure["total_time"][len(secure)-5:], marker='o', linestyle='--', color='b',
            markerfacecolor='none', markeredgewidth=1)
    plt.plot(secure["rows"][:len(secure)-4], secure["total_time"][:len(secure)-4], marker='o', linestyle='-', color='b', label='MP-SPDZ')
plt.plot(secure["rows"], secure["total_time"], marker='o', linestyle='-', color='b', label='MP-SPDZ')
plt.plot(plain["rows"], plain["total"], marker='o', linestyle='-', color='g', label='Python')
plt.plot(db["Rows"], db["Time"], marker='o', linestyle='-', color='r', label='DuckDB')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Rows', fontsize=22)
plt.ylabel('Time (s)', fontsize=22)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=18, loc='upper left')

output_path = f"./measurements/plot/{query}_total_{domain}.png"
plt.savefig(output_path)