from pprint import pprint
from typing import Callable, List


def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def select_distinct(
        matrix: List[List[int]], 
        column: int,
        condition: Callable[[List[int]], bool] = lambda row: True
    ) -> List[List[int]]:
    matrix.sort(key=lambda row: row[column])
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
    result = []
    for i in range(len(matrix)):
        if matrix[i][col1] <= matrix[i][col2]:
            result.append(matrix[i] + [1])
        else:
            result.append(matrix[i] + [0])
    return result

def union_all(left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
    return left + right

max_rows = 50
a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", max_rows)
b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", max_rows)

union = union_all(a, b)

# def with_condition():
#     def join_condition(left, right):
#         return (
#             (left[8] == 414) and
#             (right[4] == 0) and
#             (left[2] <= right[2])
#         )
#     j = nested_loop_join(union_x, union_y, 1, 1, join_condition)
#     s = select_distinct(j, 0, condition=lambda row: row[-1] == 1)
#     return s

aw = where(union, 8, 414)
bw = where(union, 4, 0)

matrix = nested_loop_join(aw, bw, 1, 1)
matrix = where_less_then(matrix, 2, len(aw[0])+2)
matrix = select_distinct(matrix, 0, condition=lambda row: row[-1] == row[-2] == row[-3] == row[13] == 1)

c = 0
for row in matrix:
    if row[-1] == 1:
        c += 1
print(c)