from collections import defaultdict
from pprint import pprint
import time
from typing import Callable, List

def measure_time(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__}:", end=" ")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
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
def nested_loop_join(
        left: List[List[int]],
        right: List[List[int]], 
        left_key: int, 
        right_key: int,
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:

    n_rows = len(left)*len(right)
    n_cols = len(left[0]) + len(right[0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    cnt = 0

    for l_row in left:
        for r_row in right:
            if (r_row[right_key] == l_row[left_key]) and condition(l_row, r_row):
                # result.append(l_row + r_row + [1])
                result[cnt] = l_row + r_row + [1]
            else:
                # result.append(l_row + r_row + [0])
                result[cnt] = l_row + r_row + [0]
            cnt += 1
    return result

@measure_time
def sort_merge_join_un(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int,
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    n_rows = len(right)
    n_cols = len(left[0]) + len(right[0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    i, j, cnt = 0,0,0

    while (i < len(left)) & (j < len(right)):
        left_value = left[i][l_key]
        left_row = left[i]

        lt = 1 if left[i][l_key] < right[j][r_key] else 0
        gt = 1 if left[i][l_key] > right[j][r_key] else 0
        eq = 1 if left[i][l_key] == right[j][r_key] else 0

        i = i+1 if lt else i
        j = j+1 if gt else j

        while j < len(right) and right[j][r_key] == left_value:
            result[cnt] = left[i] + right[j] if condition(left_row, right[j]) & eq else result[cnt]
            cnt = cnt+1 if condition(left_row, right[j]) & eq else cnt
            j = j+1 if eq else j
        i = i+1 if eq else i

        # if lt:
        #     i += 1
        # if gt:
        #     j += 1
        # if eq:
        #     while j < len(right) and right[j][r_key] == left_value:
        #         if condition(left_row, right[j]):
        #             result[cnt] = left[i] + right[j]
        #             cnt += 1
        #         j += 1
        #     i += 1
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
            # if condition(l_row, r_row):
            result.append(l_row + r_row)
    
    return result

@measure_time
def sort_merge_join_uu(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int, 
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    n_rows = len(right)
    n_cols = len(left[0]) + len(right[0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    i, j, cnt = 0, 0, 0

    while (i < len(left)) & (j < len(right)):
        lt = left[i][l_key] < right[j][r_key]
        gt = left[i][l_key] > right[j][r_key]
        eq = left[i][l_key] == right[j][r_key]

        result[cnt] = left[i] + right[j] if eq & condition(left[i],right[j]) else result[cnt]
        cnt += 1

        i = i+1 if lt else i
        j = j+1 if gt else j

        i = i+1 if eq & condition(left[i],right[j]) else i
        j = i+1 if eq & condition(left[i],right[j]) else j

        # i_lt = i+1 if lt else i
        # j_gt = j+1 if gt else j

        # i_eq = i+1 if eq & condition(left[i],right[j]) else i_lt
        # j_eq = i+1 if eq & condition(left[i],right[j]) else j_gt

        # i = i_eq
        # j = j_eq
    return result

@measure_time
def sort_merge_join_nn(
        left: List[List[int]], 
        right: List[List[int]], 
        l_key: int, 
        r_key: int, 
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    left = sorted(left, key=lambda row: row[l_key])
    right = sorted(right, key=lambda row: row[r_key])

    n_rows = len(left)*len(right)
    n_cols = len(left[0]) + len(right[0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    i, j, cnt = 0, 0, 0

    while (i < len(left)) & (j < len(right)):
        c_l = i # Is the currently processed element in left table
        c_r = j # Is the currently processed element in right table

        lt = 1 if left[i][l_key] < right[j][r_key] else 0
        gt = 1 if left[i][l_key] > right[j][r_key] else 0
        eq = 1 if left[i][l_key] == right[j][r_key] else 0

        i = i+1 if lt else i
        j = j+1 if gt else j

        while i < len(left) and left[i][l_key] == right[c_r][r_key]:
            j = c_r
            while j < len(right) and right[j][r_key] == left[c_l][l_key]:
                new_row = left[i] + right[j] if condition(left[c_l], right[j]) & eq else result[cnt]
                # result.append(new_row)
                result[cnt] = new_row
                cnt = cnt+1 if condition(left[c_l], right[j]) & eq else cnt
                j = j+1 if eq else j
            i = i+1 if eq else i

    # result = []
    # i, j = 0, 0
    # len_left, len_right = len(left), len(right)
    
    # while i < len_left and j < len_right:
    #     c_l = i
    #     c_r = j
        
    #     lt = 1 if left[i][l_key] < right[j][r_key] else 0
    #     gt = 1 if left[i][l_key] > right[j][r_key] else 0
    #     eq = 1 if left[i][l_key] == right[j][r_key] else 0

    #     i = i+1 if lt else i
    #     j = j+1 if gt else j

    #     while c_r < len_right and right[c_r][r_key] == left[i][l_key]:
    #         result[cnt] = left[i] + right[c_r]
    #         c_r += 1
        
    #     # Finde alle weiteren übereinstimmenden Zeilen in der linken Tabelle
    #     # und füge sie zum Ergebnis hinzu
    #     while c_l < len(left) and left[c_l][l_key] == right[c_r][r_key]:

    #     temp_i = i + 1
    #     while temp_i < len_left and left[temp_i][key] == left_key:
    #         result.append({**left[temp_i], **right[j]})
    #         temp_i += 1
        
    #     # Beide Indizes erhöhen
    #     i += 1
    #         j += 1


    return result

@measure_time
def sort_merge_join(left, right, l_key, r_key):
    # Sort both datasets on the respective keys
    left_sorted = sorted(left, key=lambda row: row[l_key])
    right_sorted = sorted(right, key=lambda row: row[r_key])

    # Initialize pointers for both sorted lists
    i, j = 0, 0
    result = []

    # Use a for loop to iterate through the elements
    for _ in range(len(left_sorted) + len(right_sorted)):
        # Break the loop if either pointer has reached the end of its respective list
        if i >= len(left_sorted) or j >= len(right_sorted):
            break

        left_row = left_sorted[i]
        right_row = right_sorted[j]

        # Compare the join keys
        if left_row[l_key] < right_row[r_key]:
            i += 1
            if i >= len(left_sorted):
                i = len(left_sorted)-1
        elif left_row[l_key] > right_row[r_key]:
            j += 1
            if j >= len(right_sorted):
                j = len(right_sorted)-1
        else:
            merged_row = left_row + right_row
            result.append(merged_row)
            j += 1
            i += 1

    return result

@measure_time
def merge_sort_join(list1, list2, key1, key2):
    # sort the lists based on the given keys
    # sorted_list1 = sorted(list1, key=lambda x: x[key1])
    # sorted_list2 = sorted(list2, key=lambda x: x[key2])

    sorted_list1 = list1
    sorted_list2 = list2
    
    # joined_list = []
    n_rows = len(sorted_list2)*len(sorted_list1)
    n_cols = len(sorted_list1[0]) + len(sorted_list2[0])
    joined_list = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
    i, j = 0, 0
    cnt = 0
    n = len(sorted_list1)
    m = len(sorted_list2)

    for i in range(n):
        for j in range(m):
            if sorted_list1[i][key1] == sorted_list2[j][key2]:
                # joined_list.append(sorted_list1[i] + sorted_list2[j])
                joined_list[cnt] = sorted_list1[i] + sorted_list2[j]
            if sorted_list1[i][key1] < sorted_list2[j][key2]:
                break
            cnt += 1
        
    return joined_list


def print_results(data: List[List[int]]):
    c = 0
    for i in data:
        if i[0] != 0:
        # if i[-1] == 1:
            # print(i)
            c += 1
        # print(i)
    print(c)


max_rows=500
a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", max_rows)
b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", max_rows)

# uu = sort_merge_join_uu(a, b, 0, 0)
# un = sort_merge_join_un(a, b, 0, 1)
nn = sort_merge_join_nn(a, b, 1, 1)

h = hash_join(a, b, 1, 1)

# s = merge_sort_join(a, b, 1, 1)
# sm = sort_merge_join_uu(a, b, 1, 1)
n = nested_loop_join(a, b, 1, 1)
# sm = sort_merge_join(a, b, 1, 1)

print_results(h)
# print_results(uu)
print_results(nn)
# print_results(sm)

# for i in un:
#     print(i)