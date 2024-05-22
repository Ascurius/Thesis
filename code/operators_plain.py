from typing import List
import numpy as np
from itertools import groupby

########################
#### Plaintext operators
########################

def preprocess(filename: str):
    with open(filename, 'r') as file:
        list_of_lists = []
        for line in file:
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

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

def hash_join(left, right, left_key, right_key):
    h = defaultdict(list)
    # hash phase
    for row in left:
        h[row[left_key]].append(row)
    # join phase
    return [(s, r) for r in right for s in h[r[right_key]]]

def select_distinct(matrix: List[List[int]], column: int) -> List[List[int]]:
    result = []
    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) & (matrix[i][-1] == matrix[i][-2] == matrix[i][-3] == matrix[i][13] == 1):
            result.append(matrix[i] + [1])
            prev_value = matrix[i][column]
        else:
            result.append(matrix[i] + [0])
    return result

def nested_loop_join(
        left: List[List[int]],
        right: List[List[int]], 
        left_key: int, 
        right_key: int
    ) -> List[List[int]]:
    result = []
    for l_row in left:
        for r_row in right:
            if r_row[right_key] == l_row[left_key]:
                result.append(l_row + r_row + [1])
            else:
                result.append(l_row + r_row + [0])
    return result

def where(matrix: List[List[int]], key: int, value: int) -> List[List[int]]:
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix

def where_less_then(matrix: List[List[int]], col1: int, col2: int) -> List[List[int]]:
    for i in range(len(matrix)):
        if matrix[i][col1] <= matrix[i][col2]:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix
