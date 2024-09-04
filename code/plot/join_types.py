import numpy as np
import re

from collections import defaultdict
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from pprint import pprint
from matplotlib import pyplot as plt

# query = "aspirin_count"

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
                current_entry = {'rows': int(match.group(1)), 'times': {}}
                continue
            
            # Extract total time
            match = re.match(r'Time\s*=\s*(\d+\.?\d+)', line)
            if match:
                current_entry['total_time'] = float(match.group(1))
                continue
            
            # Extract times for specific timers
            match = re.match(r'(Time\d+)\s*=\s*(\d+\.\d+)', line)
            if match:
                timer_key = match.group(1)
                timer_value = float(match.group(2))
                if timer_key in timer_keys:
                    current_entry['times'][timer_keys[timer_key]] = timer_value
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

def polynomial_extrapolation(rows, times, rows_to_extrapolate, degree=2):
    poly = PolynomialFeatures(degree)
    model = make_pipeline(poly, LinearRegression())
    rows_reshaped = rows.reshape(-1, 1)
    model.fit(rows_reshaped, times)
    
    # Vorhersagen für die extrapolierten Werte
    rows_to_extrapolate_reshaped = rows_to_extrapolate.reshape(-1, 1)
    times_extrapolate = model.predict(rows_to_extrapolate_reshaped)
    
    return dict(zip(rows_to_extrapolate, times_extrapolate))

def plot_operator_times(parsed_data):
    join_types = list(parsed_data.keys())
    # Define operators and their corresponding labels
    operators = ['first_filter', 'second_filter', 'join', 'distinct', 'distinct_sort', 'join_sort']
    operator_labels = ["First Filter", "Second Filter", "Join", "Distinct", "Sort (Distinct)", "Sort (Join)"]
    
    # Collect average times for each operator and join type
    operator_times = {label: [np.mean([entry['times'].get(op, 0) for entry in parsed_data[join_type]]) for join_type in join_types] for op, label in zip(operators, operator_labels)}
    
    # Filter out operators with no data
    operator_labels = [label for label in operator_labels if any(operator_times[label])]
    operator_times = {label: operator_times[label] for label in operator_labels}

    bar_width = 0.35
    y_positions = np.arange(len(join_types))
    
    plt.figure(figsize=(12, 10))

    # Stack the bars horizontally
    bottom = np.zeros(len(join_types))
    for label in operator_labels:
        plt.barh(y_positions, operator_times[label], bar_width, left=bottom, label=label)
        bottom += np.array(operator_times[label])

    print(operator_times["First Filter"])

    plt.xlabel('Time (s)')
    plt.xscale("log")
    plt.ylabel('Join Type')
    plt.title('Mean Operator Times for Different Join Types')
    plt.yticks(y_positions, join_types)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'./measurements/plot/{query}_join_types.png')

def plot_operator_times_over_rows(parsed_data, hashing=False):
    plt.figure(figsize=(9, 8))

    rows_to_extrapolate = np.array([4000, 6000, 8000, 10000, 20000, 40000, 60000, 80000, 100000, 200000, 400000, 600000, 800000, 1000000])

    for join_type, df in parsed_data.items():
        if 'rows' in df.columns and 'total_time' in df.columns:
            rows = df['rows'].values
            total_times = df['join'].values

            # Plot original data
            plt.plot(rows, total_times, marker='o', linestyle='-', label=join_type)
            
            if rows[-1] <= 2000:
                # Polynomial extrapolation
                polynomial_extrapolated_times = polynomial_extrapolation(np.array(rows), np.array(total_times), rows_to_extrapolate, degree=2)
                
                # Plot extrapolated data with dashed line and empty markers
                plt.plot(rows_to_extrapolate, [polynomial_extrapolated_times[row] for row in rows_to_extrapolate],
                         linestyle='--', marker='o', markerfacecolor='none', color=plt.gca().lines[-1].get_color())
                
                # Draw dashed line between the last original point and the first extrapolated point
                plt.plot([rows[-1], rows_to_extrapolate[0]], [total_times[-1], polynomial_extrapolated_times[rows_to_extrapolate[0]]],
                         linestyle='--', color=plt.gca().lines[-1].get_color())
        else:
            print(f"DataFrame for join type {join_type} does not have the required columns 'rows' and 'total_time'.")

    if hashing:
        hashing_data = parse_data(query, filename=f"./measurements/results/misc/hashing.txt")["hashing"]
        plt.plot(hashing_data["rows"], hashing_data["total_time"], marker='o', linestyle='-', label="hashing")

    plt.xlabel('Rows', fontsize=22)
    plt.xscale("log")
    plt.xticks(fontsize=20)

    plt.yscale("log")
    plt.ylabel('Time (s)', fontsize=22)
    plt.yticks(fontsize=20)

    plt.legend(fontsize=18, loc='upper left')
    plt.grid(True)

    if hashing:
        plt.savefig(f'./measurements/plot/{query}_join_types_hashing.png')
    else:
        plt.savefig(f'./measurements/plot/{query}_join_types.png')

query = "cdiff"

data = parse_data(query, filename = f"./measurements/results/{query}/secure.txt")

# pprint(data["arithmetic"])

plot_operator_times_over_rows(data, hashing=False)