import os
import sys
import time
from typing import List, Callable

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def where(matrix: List[List[int]], key: int, value: int) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            result.append(matrix[i] + [1])
        else:
            result.append(matrix[i] + [0])
    return result

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

@measure_time
def cdiff(data):
    w = where(data, 8, 8)
    w.sort(key=lambda row: (row[1], row[2]))
    diags = row_number_over_partition_by(w, 1, condition=lambda row: row[13] == 1)
    join = nested_loop_join(
        diags, diags, 1, 1, 
        condition=lambda left, right: (abs(left[2] - right[2]) >= 15) and \
                                    (abs(left[2] - right[2]) <= 56) and \
                                    (left[14]+1 == right[14])
    )
    selection = select_distinct(join, 1, 
        condition=lambda row: row[13] == row[-1] == row[-3] == 1
    )
    result = []
    c = 0
    for row in selection:
        if row[-1]:
            result.append(row)
            c += 1
    return result

if __name__ == "__main__":
    pwd = os.getcwd()
    max_rows = int(sys.argv[1])
    input_file = f"{pwd}/MP-SPDZ/Player-Data/Input-P0-0"

    data = preprocess(input_file, max_rows)
    result, single_time = cdiff(data)
    print(f"{single_time:.6f}")