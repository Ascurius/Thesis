from collections import defaultdict
import sys
import time
from typing import List, Callable

TOTAL_EXECUTION_TIME = 0.0

def measure_time(func):
    def wrapper(*args, **kwargs):
        global TOTAL_EXECUTION_TIME
        print(f"{func.__name__}:", end=" ")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        TOTAL_EXECUTION_TIME += execution_time
        if isinstance(result, tuple):
            print(f"{execution_time:.6f}")
            print(f"select_distinct_sorting: {result[1]:.6f}")
            return result[0]
        print(f"{execution_time:.6f}")
        return result
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
def where(matrix: List[List[int]], key: int, value: int) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            result.append(matrix[i] + [1])
        else:
            result.append(matrix[i] + [0])
    return result

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
def sort_merge_join(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int, 
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    result = []

    i, j = 0, 0

    while i < len(left) and j < len(right):
        l_value = left[i][l_key]
        r_value = right[j][r_key]

        if l_value < r_value:
            i += 1
        elif l_value > r_value:
            j += 1
        else:
            # Collect all rows from left that match l_value
            left_rows = []
            while i < len(left) and left[i][l_key] == l_value:
                left_rows.append(left[i])
                i += 1
            
            # Collect all rows from right that match r_value
            right_rows = []
            while j < len(right) and right[j][r_key] == r_value:
                right_rows.append(right[j])
                j += 1
            
            # Append all combinations of left_rows and right_rows to result
            for l_row in left_rows:
                for r_row in right_rows:
                    if condition(l_row, r_row):
                        result.append(l_row + r_row)

    return result

@measure_time
def hash_join(left, right, left_key, right_key, condition = lambda left, right: True):
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

@measure_time
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

@measure_time
def select_distinct(
        matrix: List[List[int]], 
        column: int,
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    st = time.time()
    matrix.sort(key=lambda row: row[column])
    et = time.time() - st

    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) and condition(matrix[i]):
            matrix[i].append(1)
            prev_value = matrix[i][column]
        else:
            matrix[i].append(0)
    return matrix, et

@measure_time
def union_all(left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
    return left + right


def plaintext_cdiff(a, b, join_type, l_key, r_key):
    if join_type == "h":
        join_function = hash_join
        dist_cond = lambda row: row[13] == row[-2] == 1
    elif join_type == "n":
        join_function = nested_loop_join
        dist_cond = lambda row: row[13] == row[-1] == row[-3] == 1
    elif join_type == "s":
        join_function = sort_merge_join
        dist_cond = lambda row: row[13] == row[-2] == 1
    else:
        print(f"Unknown join type: {join_type}")
        exit()
    union = union_all(a,b)
    m = where(union, 8, 8)
    st = time.time()
    m.sort(key=lambda row: (row[1], row[2]))
    print(f"correctness_sort: {time.time() - st:.6f}")
    m = row_number_over_partition_by(m, 1, condition=lambda row: row[13] == 1)
    m = join_function(
        m, m, l_key, r_key, 
        condition=lambda left, right: (abs(left[2] - right[2]) >= 15) and \
                                    (abs(left[2] - right[2]) <= 56) and \
                                    (left[14]+1 == right[14])
    )
    m = select_distinct(m, 1, 
        condition=dist_cond
    )
    result = []
    # c = 0
    # for row in m:
    #     if row[-1]:
    #         # result.append(row[1])
    #         c += 1
    # print(c)
    return result

if __name__ == "__main__":
    max_rows = int(sys.argv[1])
    left_key = int(sys.argv[3])
    right_key = int(sys.argv[4])

    a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", max_rows)
    b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", max_rows)

    _ = plaintext_cdiff(a, b, sys.argv[2], left_key, right_key)
    print(f"total: {TOTAL_EXECUTION_TIME:.6f}")