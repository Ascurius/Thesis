from collections import defaultdict
from typing import Callable, List, Tuple
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

def select(matrix: List[List[int]], columns: List[int]) -> List[List[int]]:
    columns.sort()
    return [[row[i] for i in columns] for row in matrix]

def group_by(matrix: List[List[int]], key: int) -> List[List[int]]:
    matrix.sort(key=lambda row: row[key])
    count = 0
    current_element = -1

    for i in range(len(matrix)-1):
        matrix[i].extend([0,0])
        if matrix[i][key] == matrix[i+1][key]:
            matrix[i][-2] = 0
        else:
            matrix[i][-2] = 1
        if matrix[i][key] == current_element:
            count = count + 1
            current_element = current_element
        else:
            count = 1
            current_element = matrix[i][key]
        matrix[i][-1] = count
    matrix[-1][-2] = 1
    if matrix[-1][key] == current_element:
        matrix[-1][-1] = count + 1
    else:
        matrix[-1][-1] = 1
    return matrix

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

def select_distinct(
        matrix: List[List[int]], 
        column: int,
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    result = []
    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) and condition(matrix[i]):
            result.append(matrix[i] + [1])
            prev_value = matrix[i][column]
        else:
            result.append(matrix[i] + [0])
    return result

def nested_loop_join(
        left: List[List[int]],
        right: List[List[int]], 
        left_key: int, 
        right_key: int,
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> Tuple[List[List[int]], int]:
    relevancy_column = len(left[0]) + len(right[0])
    result = []
    for l_row in left:
        for r_row in right:
            if (r_row[right_key] == l_row[left_key]) and condition(l_row, r_row):
                result.append(l_row + r_row + [1])
            else:
                result.append(l_row + r_row + [0])
    return result, relevancy_column

def where(matrix: List[List[int]], key: int, value: int) -> Tuple[List[List[int]], int]:
    relevancy_column = len(matrix[0])
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix, relevancy_column

def where_less_then(matrix: List[List[int]], col1: int, col2: int) -> List[List[int]]:
    for i in range(len(matrix)):
        if matrix[i][col1] <= matrix[i][col2]:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix

def row_number_over_partition_by(
        matrix: List[List[int]], 
        key: int, 
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    matrix.sort(key=lambda row: row[key])

    row_number = 0
    prev_partition = -1

    for i in range(len(matrix)):
        matrix[i].append(0)
        partition = matrix[i][key]

        if partition != prev_partition:
            row_number = 0
        prev_partition = partition

        if condition(matrix[i]):
            row_number += 1
        matrix[i][-1] = row_number
    return matrix

def filter_and_mark(matrix: List[List[int]], comparison_func: Callable[[List[int]], bool]) -> Tuple[List[List[int]], int]:
    relevancy_column = len(matrix[0])
    for row in matrix:
        row.append(1 if comparison_func(row) else 0)
    return matrix, relevancy_column