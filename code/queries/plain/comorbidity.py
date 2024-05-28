import os
from pprint import pprint
import sys
import time
from typing import List
import numpy as np

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # print(f"Number of rows: {num_rows}")
        # print(f"Execution time of '{func.__name__}': {execution_time:.6f} seconds")
        return result, execution_time
    return wrapper

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

def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

@measure_time
def comorbidity(matrix):
    m = matrix
    m = group_by_count(m, 1)
    m = order_by(m, order_key=-1, relevance_key=-2, reversed=True)
    m = limit(m, 10)
    return m
    
if __name__ == "__main__":
    pwd = os.getcwd()
    max_rows = int(sys.argv[1])
    input_file = f"{pwd}/MP-SPDZ/Player-Data/Input-P0-0"

    data = preprocess(input_file, max_rows)
    result, single_time = comorbidity(data)
    print(f"Time needed for executing the query: {single_time:.6f}")
    pprint(result)