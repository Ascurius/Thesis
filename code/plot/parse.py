from collections import defaultdict
from pprint import pprint
import re

import numpy as np
import pandas as pd


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


def parse_data(query, filename):
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

def csvize(data):
    csv = ""
    csv = csv + "rows,total," + ",".join(data[0]["times"].keys()) + "\n"
    for i in data:
        # line = str(i["rows"]) + "," + str(i["total_time"]) + "," + ",".join(i["times"].values())
        line = str(i["rows"]) + "," + str(i["total_time"]) + ",".join(i["times"].values())
        csv = csv + line + "\n"
    return csv

query = "aspirin_count"

data = parse_data(query, filename = f"./measurements/results/misc/hashing.txt")["hashing"]
uu = parse_data(query, filename = f"./measurements/results/{query}/secure.txt")["sort-merge join-un"]

print(np.mean(data["total_time"]) / np.mean(uu["join"]))
