import os
from pprint import pprint
import sys
import time
from typing import List

TOTAL_EXECUTION_TIME=0.0

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

def select_columns(matrix: List[List[int]], columns: List[int]) -> List[List[int]]:
    columns.sort()
    selected_matrix = []
    for row in matrix:
        selected_row = [row[col] for col in columns]
        selected_matrix.append(selected_row)
    return selected_matrix

@measure_time
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

@measure_time
def order_by(matrix: List[List[int]], order_key: int, 
             relevance_key: int = None, reversed: bool = False
            ) -> List[List[int]]:
    result = [row + [0] for row in matrix]

    for i in range(len(matrix)):
        result[i][-1] = matrix[i][order_key] * (matrix[i][relevance_key] if relevance_key is not None else 1)
    result.sort(key=lambda row: row[-1], reverse=reversed)
    return result

@measure_time
def limit(matrix: List[List[int]], maximum) -> List[List[int]]:
    return matrix[:maximum]

def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def comorbidity(m):
    m = group_by_count(m, 1)
    m = order_by(m, order_key=-1, relevance_key=-2, reversed=True)
    m = limit(m, 10)
    return m 
    
if __name__ == "__main__":
    pwd = os.getcwd()
    max_rows = int(sys.argv[1])
    input_file = f"{pwd}/MP-SPDZ/Player-Data/Input-P0-0"

    data = preprocess(input_file, max_rows)
    _ = comorbidity(data)
    print(f"total: {TOTAL_EXECUTION_TIME:.6f}")