import numpy as np
import re

from collections import defaultdict
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from pprint import pprint
from matplotlib import pyplot as plt

query = "aspirin_count"

def parse_data():
    filename = f"./measurements/results/{query}/secure.txt"
    data = defaultdict(list)
    current_entry = {}
    current_join_type = None
    timer_keys = {
        'Time10': 'read_data',
        'Time100': 'first_filter',
        'Time200': 'second_filter',
        'Time300': 'join',
        'Time500': 'distinct',
        'Time600': 'distinct_sort',
        'Time1000': 'join_sort'
    }
    
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
    
    return dict(data)

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

def plot_operator_times_over_rows(parsed_data):
    plt.figure(figsize=(12, 8))

    rows_to_extrapolate = np.array([4000, 6000, 8000, 10000, 20000, 40000, 60000, 80000, 100000, 200000, 400000, 600000, 800000, 1000000])

    for join_type, entries in parsed_data.items():
        rows = [entry['rows'] for entry in entries if 'total_time' in entry]
        total_times = [entry['total_time'] for entry in entries if 'total_time' in entry]
        
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


    plt.xlabel('Number of Rows')
    plt.xscale("log")
    # plt.yscale("log")
    plt.ylabel('Total Time (s)')
    plt.title('Total Time vs. Number of Rows for Different Join Types')
    # plt.ticklabel_format(style='plain', axis='x')
    plt.legend()
    # plt.ticklabel_format(style='plain', axis='x')
    plt.grid(True)

    plt.savefig(f'./measurements/plot/{query}_join_types.png')

data = parse_data()

plot_operator_times_over_rows(data)