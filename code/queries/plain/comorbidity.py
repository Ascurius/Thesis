import time
import numpy as np
from itertools import groupby

player = 0
num_rows = 100000000
filename = "/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P{}-0".format(player)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # print(f"Number of rows: {num_rows}")
        # print(f"Execution time of '{func.__name__}': {execution_time:.6f} seconds")
        return result, execution_time
    return wrapper

def print_matrix(matrix: np.ndarray) -> None:
    for row in matrix:
        print(row)

@measure_time
def preprocess():
    m = np.fromfile(filename, sep=" ", dtype=int, count=num_rows*13)
    m = m.reshape((num_rows,13))
    return m

def select_columns(matrix: np.ndarray, columns: list) -> np.ndarray:
    columns.sort()
    return matrix[:, columns]

def group_by_count(matrix: np.ndarray, key: int) -> np.ndarray:
    column = sorted(matrix[:, key])
    return np.array(
        ([(k, len(list(g))) for k, g in groupby(column)])
    )

def order_by(matrix, keys, reversed=False):
    sorted_matrix = sorted(matrix, key=lambda x: (x[keys[1]], x[keys[0]]), reverse=reversed)
    return np.array(sorted_matrix)

def limit(matrix, maximum):
    return matrix[:maximum]

@measure_time
def comorbidity(matrix):
    m = matrix
    m = select_columns(m, [1])
    m = group_by_count(m, 0)
    m = order_by(m, [0,1], reversed=True)
    m = limit(m, 5)
    return m
    
data, pre_time = preprocess()
num_tests = 10
print(f"Number of rows: {num_rows}")
print(f"Time needed for preprocessing: {pre_time:.6f}")
total_time = 0
for _ in range(num_tests):
    _, single_time = comorbidity(data)
    # print(f"Average time needed for computation: {single_time:.6f}")
    total_time += single_time
print(f"Average time needed for computation: {(total_time/num_tests):.6f}")