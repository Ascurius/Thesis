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

times = {
    "aspirin": {
        'Time10': 'read_data',
        'Time100': 'first_filter',
        'Time200': 'second_filter',
        'Time300': 'join',
        'Time500': 'distinct',
        'Time600': 'distinct_sort',
        'Time1000': 'join_sort'
    },
    "plaintext_aspirin": {
        'Time10': 'read_data',
        'Time100': 'union_all',
        'Time200': 'first_filter',
        'Time300': 'second_filter',
        'Time400': 'join',
        'Time600': 'distinct',
        'Time700': 'distinct_sort',
        'Time1000': 'join_sort'
    },
    "cdiff": {
        'Time10': 'read_data',
        'Time100': 'first_filter',
        'Time200': 'correctness_sort',
        'Time300': 'row_number_over_partition_by',
        'Time400': 'join',
        'Time500': 'distinct',
        'Time600': 'distinct_sort'
    },
    "plaintext_cdiff": {
        'Time10': 'read_data',
        'Time100': 'union_all',
        'Time200': 'first_filter',
        'Time300': 'correctness_sort',
        'Time400': 'row_number_over_partition_by',
        'Time500': 'join',
        'Time600': 'distinct',
        'Time700': 'distinct_sort'
    },
    "comorbidity": {
        "Time100": "select_columns",
        "Time200": "group_by",
        "Time300": "group_by_sort",
        "Time400": "order_by",
        "Time500": "order_by_sort",
        "Time600": "limit"
    },
    "plaintext_comorbidity": {
        "Time100": "union_all",
        "Time200": "select_columns",
        "Time300": "group_by",
        "Time400": "group_by_sort",
        "Time500": "order_by",
        "Time600": "order_by_sort",
        "Time700": "limit"
    }
}

labels = {
    "union_all": "UNION ALL",
    "select_columns": "SELECTION",
    "group_by": "GROUP BY",
    "group_by_sort": "GROUP BY (sort)",
    "order_by": "ORDER BY",
    "order_by_sort": "ORDER BY (sort)",
    "limit": "LIMIT",
    "distinct": "DISTINCT",
    "distinct_sort": "DISTINCT (sort)",
    "join": "JOIN",
    "join_sort": "JOIN (sort)",
    "row_number_over_partition_by": "PARTITION BY",
    "first_filter": "WHERE (1st)",
    "second_filter": "WHERE (2nd)",
    "third_filter": "WHERE (3rd)"
}
exclude = ["join_sort", "read_data", "correctness_sort"]


def parse_data(query):
    filename = f"./measurements/results/{query}/secure.txt"
    data = defaultdict(list)
    current_entry = {}
    current_join_type = None
    if query == "aspirin_count":
        timer_keys = times["aspirin_count"]
    elif query == "cdiff":
        timer_keys = times["cdiff"]
    elif query == "comorbidity":
        timer_keys = times["comorbidity"]
    elif query == "plaintext_aspirin_count":
        timer_keys = times["plaintext_aspirin_count"]
    elif query == "plaintext_cdiff":
        timer_keys = times["plaintext_cdiff"]
    elif query == "plaintext_comorbidity":
        timer_keys = times["plaintext_comorbidity"]
    
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
                current_entry = {'rows': int(match.group(1)), "times":{}}
                continue
            
            # Extract total time
            match = re.match(r'Time\s*=\s*(\d+\.?\d+)', line)
            if match:
                current_entry['total_time'] = float(match.group(1))
                continue
            
            # Extract times for specific timers
            match = re.match(r'(Time\d*)\s*=\s*([\d\.]+(?:e[+-]?\d+)?)', line)
            if match:
                timer_key = match.group(1)
                timer_value = match.group(2)
                if timer_key in timer_keys:
                    current_entry["times"][timer_keys[timer_key]] = float(timer_value)
                continue
            
            # Extract data sent and rounds
            match = re.match(r'Data sent\s*=\s*([\d.]+) MB in ~(\d+) rounds', line)
            if match:
                current_entry['data_sent'] = float(match.group(1))
                current_entry['rounds'] = int(match.group(2))
                continue
            
            # Extract global data sent
            match = re.match(r'Global data sent\s*=\s*([\d.]+) MB', line)
            if match:
                current_entry['global_data_sent'] = float(match.group(1))
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
domain = "arithmetic"

secure = parse_data(query)[domain]

if len(secure["rows"]) < 34:
    secure = extrapolate_specific_rows(secure, target_rows=[400000, 600000, 800000, 1000000])

secure["rows"] = pd.to_numeric(secure["rows"], errors='coerce')

graphs = []
for op in times[query].values():
    if op not in exclude:
        secure[op] = pd.to_numeric(secure[op], errors='coerce')
        graphs.append(
            (np.max(secure[op]), op, labels[op])
        )

plt.figure(figsize=(10, 8))

if len(secure["rows"]) < 34:
    plt.plot(secure["rows"][len(secure)-5:], secure["total_time"][len(secure)-5:], marker='o', linestyle='--', color='b',
            markerfacecolor='none', markeredgewidth=1)
    plt.plot(secure["rows"][:len(secure)-4], secure["total_time"][:len(secure)-4], marker='o', linestyle='-', color='b', label='MP-SPDZ')

# Sortiere die Graphen nach den maximalen Werten
graphs.sort(reverse=True, key=lambda x: x[0])

# Zeichne die Graphen in der sortierten Reihenfolge
for max, operator, label in graphs:
    plt.plot(secure["rows"], secure[operator], marker='o', linestyle='-', label=label)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Rows', fontsize=22)
plt.ylabel('Time (s)', fontsize=22)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=16, loc='upper left')

output_path = f"./measurements/plot/{query}_operators_{domain}.png"
plt.savefig(output_path)