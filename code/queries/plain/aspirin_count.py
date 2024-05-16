from pprint import pprint
from collections import defaultdict
import numpy as np

def preprocess(filename, num_rows):
    m = np.fromfile(filename, sep=" ", dtype=int, count=num_rows*13)
    m = m.reshape((num_rows,13))
    return m

def select_distinct(matrix: np.ndarray, column: int) -> np.ndarray:
    # unique_values = np.unique(matrix[:, column], axis=0)
    unique_values = []
    for element in matrix[:, column]:
        if element not in unique_values:
            unique_values.append(element)
    return unique_values

def nested_loop_join(left, right, left_key, right_key):
    result = []
    for l_row in left:
        for r_row in right:
            if r_row[right_key] == l_row[left_key]:
                result.append(
                    np.concatenate((l_row, r_row))
                )
    return np.array(result)

def where(matrix, key, value):
    return matrix[matrix[:, key] == value]

a = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P0-0", 50)
b = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P1-0", 50)

aw = where(a, 8, 414)
bw = where(b, 4, 0)

j = nested_loop_join(aw, bw, 1, 1)

# result = []
# for row in j:
#     print(row[:8])
#     if row[2] <= row[len(bw[0])+2]:
#         result.append(np.concatenate((row[0], row[1])))
# result = np.array(result)

s = select_distinct(j, 0)
c = len(j)
print(c)