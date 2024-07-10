from collections import defaultdict
from typing import Callable, List, Tuple
import numpy as np

########################
#### Plaintext operators
########################

def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def select_columns(matrix: List[List[int]], columns: List[int]) -> List[List[int]]:
    columns.sort()
    selected_matrix = []
    for row in matrix:
        selected_row = [row[col] for col in columns]
        selected_matrix.append(selected_row)
    return selected_matrix

def group_by_count(matrix: List[List[int]], key: int) -> List[List[int]]:
    matrix.sort(key=lambda row: (row[key], row[2]))
    result = [row + [0, 0] for row in matrix]

    count = 0
    current_element = None
    for i in range(len(matrix) - 1):
        if matrix[i][key] != current_element:
            count = 1
        else:
            count += 1    
        current_element = matrix[i][key]
        result[i][-2] = int(matrix[i][key] != matrix[i + 1][key])  # Relevancy column
        result[i][-1] = count                                      # Count column
    
    result[-1][-2] = 1
    if matrix[-1][key] == current_element:
        result[-1][-1] = count + 1
    else:
        result[-1][-1] = 1
    return result

def order_by(matrix: List[List[int]], order_key: int, 
             relevance_key: int = None, reversed: bool = False
            ) -> List[List[int]]:
    result = [row + [0] for row in matrix]

    for i in range(len(matrix)):
        result[i][-1] = matrix[i][order_key] * (matrix[i][relevance_key] if relevance_key is not None else 1)
    result.sort(key=lambda row: row[-1], reverse=reversed)
    return result

def limit(matrix: List[List[int]], maximum) -> List[List[int]]:
    return matrix[:maximum]

def hash_join(
        left: List[List[int]], 
        right: List[List[int]], 
        left_key: int, 
        right_key: int, 
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    hash_map = defaultdict(list)

    # Hash phase
    for l_row in left:
        secure_hash = l_row[left_key]
        hash_map[secure_hash].append(l_row)
    
    # Join phase
    result = []
    for r_row in right:
        secure_hash = r_row[right_key]
        for l_row in hash_map[secure_hash]:
            if condition(l_row, r_row):
                result.append(l_row + r_row)
    
    return result

def sort_merge_join_nn(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int, 
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    result = []

    i, j = 0,0
    mark = None

    while i < len(left) and j < len(right)+1:
        if j >= len(right):
            j = mark
            i += 1
            mark = None
            if not i < len(left):
                break
        if mark is None:
            while left[i][l_key] < right[j][l_key]:
                i += 1
            while left[i][l_key] > right[j][l_key]:
                j += 1
            mark = j
        if left[i][l_key] == right[j][l_key]:
            if condition(left[i], right[j]):
                result.append(left[i] + right[j] + [1])
            j += 1
        else:
            j = mark
            i += 1
            mark = None
    return result

def sort_merge_join_un(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    # result = []
    n_rows = len(right)
    n_cols = len(left[0]) + len(right[0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    i, j, cnt = 0,0,0

    while i < len(left) and j < len(right):
        left_value = left[i][l_key]

        lt = 1 if left[i][l_key] < right[j][r_key] else 0
        gt = 1 if left[i][l_key] > right[j][r_key] else 0
        eq = 1 if left[i][l_key] == right[j][r_key] else 0

        if lt:
            i += 1
        if gt:
            j += 1
        if eq:
            # Collect all matches from the right table
            while j < len(right) and right[j][r_key] == left_value:
                result[cnt] = left[i] + right[j]
                j += 1
                cnt += 1
            # Move to the next element in the left table
            i += 1
    return result

def select_distinct(
        matrix: List[List[int]], 
        column: int,
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) and condition(matrix[i]):
            matrix[i].append(1)
            prev_value = matrix[i][column]
        else:
            matrix[i].append(0)
    return matrix

def nested_loop_join(
        left: List[List[int]],
        right: List[List[int]], 
        left_key: int, 
        right_key: int,
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    result = []
    for l_row in left:
        for r_row in right:
            if (r_row[right_key] == l_row[left_key]) and condition(l_row, r_row):
                result.append(l_row + r_row + [1])
            else:
                result.append(l_row + r_row + [0])
    return result

def where(matrix: List[List[int]], key: int, value: int) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            result.append(matrix[i] + [1])
        else:
            result.append(matrix[i] + [0])
    return result

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

def where_condition(matrix: List[List[int]], comparison_func: Callable[[List[int]], bool]) -> Tuple[List[List[int]], int]:
    relevancy_column = len(matrix[0])
    for row in matrix:
        row.append(1 if comparison_func(row) else 0)
    return matrix, relevancy_column