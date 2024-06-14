import os
import sys
import time
from typing import Callable, List

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

@measure_time
def select_distinct(
        matrix: List[List[int]], 
        column: int,
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    st = time.time()
    matrix.sort(key=lambda row: row[column])
    et = time.time()
    sort_time = et - st
    
    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) and condition(matrix[i]):
            matrix[i].append(1)
            prev_value = matrix[i][column]
        else:
            matrix[i].append(0)
    return matrix, sort_time

@measure_time
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

@measure_time
def where(matrix: List[List[int]], key: int, value: int) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            result.append(matrix[i] + [1])
        else:
            result.append(matrix[i] + [0])
    return result

@measure_time
def where_less_then(matrix: List[List[int]], col1: int, col2: int) -> List[List[int]]:
    for i in range(len(matrix)):
        if matrix[i][col1] <= matrix[i][col2]:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix

def aspirin_count(table1, table2):
    aw, aw_time = where(table1, 8, 414)
    bw, bw_time = where(table2, 4, 0)

    m, join_time = nested_loop_join(aw, bw, 1, 1)
                                    # condition=lambda left, right: left[2] <= right[2])
    m, wlt_time = where_less_then(m, 2, len(aw[0])+2)
    m, distinct_time = select_distinct(m, 0, condition=lambda row: row[-1] == row[-2] == row[-3] == row[13] == 1)

    c = 0
    st = time.time()
    for row in m[0]: # Access the actual query result
        if row[-1]:
            c += 1
    et = time.time()
    count_time = et-st
    sort_time = m[1]
    return [aw_time, bw_time, join_time, wlt_time, distinct_time, sort_time, count_time ]


if __name__ == "__main__":
    pwd = os.getcwd()
    max_rows = int(sys.argv[1])
    a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", max_rows)
    b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", max_rows)
    times = aspirin_count(a, b)

    print(f"Total time: {sum(times):.6f}")
    print(f"First filter: {times[0]:.6f}")
    print(f"Second filter: {times[1]:.6f}")
    print(f"Join: {times[2]:.6f}")
    print(f"Third filter: {times[3]:.6f}")
    print(f"Select distinct: {times[4]:.6f}")
    print(f"Select distinct (only sort): {times[5]:.6f}")
    print(f"Count: {times[6]:.6f}")