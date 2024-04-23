import numpy as np
from itertools import groupby
from pprint import pprint

filename = "/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P1-0"

def print_matrix(matrix: np.ndarray) -> None:
    for row in matrix:
        print(row)

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

p0_row, p0_col = get_matrix_dimensions(filename)

data = np.loadtxt(filename)
m = data.reshape((p0_row, p0_col))
m = m.astype(int)

def select_columns(matrix: np.ndarray, columns: list) -> np.ndarray:
    columns.sort()
    return matrix[:, columns]

def group_by_count(matrix: np.ndarray, key: int) -> np.ndarray:
    column = sorted(matrix[:, key])
    return np.array(
        ([(k, len(list(g))) for k, g in groupby(column)])
    )

def order_by(matrix, key, reversed=False):
    sorted_matrix = sorted(matrix, key=lambda x: int(x[key]), reverse=reversed)
    return np.array(sorted_matrix)

def limit(matrix, maximum):
    return matrix[:maximum]

s = select_columns(m, [1])
g = group_by_count(s, 0)
o = order_by(g, 1, reversed=True)
l = limit(o, 5)

print_matrix(l)