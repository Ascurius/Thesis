from pprint import pprint
from typing import List, Callable, Tuple

def preprocess(filename: str) -> List[List[int]]:
    with open(filename, 'r') as file:
        list_of_lists = []
        for line in file:
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def select(matrix: List[List[int]], columns: List[int]) -> List[List[int]]:
    columns.sort()
    return [[row[i] for i in columns] for row in matrix]

def where(matrix: List[List[int]], key: int, value: int) -> Tuple[List[List[int]], int]:
    relevancy_column = len(matrix[0])
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix, relevancy_column

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

def row_number_over_partition_by(
        matrix: List[List[int]], 
        key: int, 
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> Tuple[List[List[int]], int]:
    matrix.sort(key=lambda row: row[key])

    relevancy_column = len(matrix[0])
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
    return matrix, relevancy_column

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

table1 = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P0-0")

w, match_col_where = where(table1, 8, 8)
w.sort(key=lambda row: (row[1], row[2]))

diags, match_col_partition = row_number_over_partition_by(w, 1, condition=lambda row: row[13] == 1)

join, match_col_join = nested_loop_join(
    diags, diags, 1, 1, 
    condition=lambda left, right: (abs(left[2] - right[2]) >= 15) and \
                                  (abs(left[2] - right[2]) <= 56) and \
                                  (left[match_col_partition]+1 == right[match_col_partition])
)

selection = select_distinct(join, 1, 
    condition=lambda row: row[match_col_join] == row[match_col_where] == row[-3] == 1
)
for row in selection:
    if row[-1]:
        print(row[1])