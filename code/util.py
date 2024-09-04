import time
from Compiler.library import print_ln, print_ln_if
from Compiler.types import sint

def get_matrix_dimensions(filename):
    num_rows = 0
    num_cols = None

    with open(filename, 'r') as file:
        for line in file:
            # Increment row count for each line
            num_rows += 1

            # Split the line into integers
            row_data = line.strip().split()

            # Check if the number of columns is consistent
            if num_cols is None:
                num_cols = len(row_data)
            elif num_cols != len(row_data):
                raise ValueError("Inconsistent number of columns in the matrix")

    return num_rows, num_cols

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

def get_shape(arr):
    if isinstance(arr, list):
        return [len(arr)] + get_shape(arr[0])
    else:
        return []

def refill_matrix(target, source):
    assert target.shape[0] >= source.shape[0]
    for i in range(source.shape[0]):
        target[i].assign_vector(source[i])

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of '{func.__name__}': {execution_time:.6f} seconds")
        return result
    return wrapper

def measure():
    pwd = os.getcwd()
    # start_row = int(sys.argv[1])
    rows = [1000]#, 2000, 4000, 6000, 8000, 10000, 20000, 40000, 60000, 80000, 100000, 200000, 400000, 600000, 800000, 1000000]

    output_file = "./measurements/results/aspirin_plain.csv"

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header row
        writer.writerow(["Max Rows", "Avg Total Time", "WHERE_1", "WHERE_2", "JOIN", "WHERE_3", "DISTINCT", "DISTINCT (sort), COUNT"])

        for max_rows in rows:
            a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", max_rows)
            b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", max_rows)
            
            total_times = []
            operator_times = [0] * 6  # To store sums of individual operator times

            num_iterations = 5  # Number of times to repeat the measurement
            for _ in range(num_iterations):
                times = aspirin_count(a, b)
                total_times.append(times[0])  # Total time
                for i in range(1, 7):
                    operator_times[i-1] += times[i]  # Aggregate individual times

            # Calculate averages
            avg_total_time = sum(total_times) / num_iterations
            avg_operator_times = [op_time / num_iterations for op_time in operator_times]

            # Write row to CSV file
            writer.writerow([max_rows, avg_total_time] + avg_operator_times)