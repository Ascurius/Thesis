# !/usr/bin/env python

# from circuit import sha3_256

# def print_matrix(matrix: sint.Matrix):
#     for i in range(matrix.shape[0]):
#         print_ln("%s", matrix[i].reveal())

# def hash_join(left, right, left_key, right_key):
#     result = sint.Matrix(
#         rows=left.shape[0] * right.shape[0],
#         columns=left.shape[1] + right.shape[1] + 1
#     )
#     current_idx = regint(0)
#     @for_range_opt(left.shape[0])
#     def _(left_row):
#         @for_range_opt(right.shape[0])
#         def _(right_row):
#             new_row = sint.Array(result.shape[1])
#             new_row[:result.shape[1] // 2] = left[left_row]
#             new_row[result.shape[1] // 2:] = right[right_row]
#             result[current_idx].assign(new_row)
#             current_idx.update(current_idx + regint(1))

#     hash_map = {}
#     @for_range_opt(left.shape[0])
#     def _(l_row):
#         key = sha3_256(left[l_row][left_key])
#         hash_map[key] = l_row

#     @for_range_opt(right.shape[0])
#     def _(r_row):
#         @for_range_opt(len(hash_map))
#         def _(hash):
#             key = hash_map.keys()[hash]
#             result[r_row][-1] = (key == sha3_256(right[r_row][right_key]) ).if_else(sint(1), sint(0))

# def concat_tables(left, right):
#     result = sint.Matrix(
#         rows=left.shape[0] * right.shape[0],
#         columns=left.shape[1] + right.shape[1] + 1
#     )
#     current_idx = regint(0)
#     @for_range_opt(left.shape[0])
#     def _(left_row):
#         @for_range_opt(right.shape[0])
#         def _(right_row):
#             new_row = sint.Array(result.shape[1])
#             new_row[:result.shape[1] // 2] = left[left_row]
#             new_row[result.shape[1] // 2:] = right[right_row]
#             result[current_idx].assign(new_row)
#             current_idx.update(current_idx + regint(1))
#     return result
    

# max_rows = 50
# a = sint.Matrix(max_rows, 13)
# a.input_from(0)
# b = sint.Matrix(max_rows, 13)
# b.input_from(1)
# # hash_join(a, b, 1, 1)
# c = concat_tables(a, b)
# print_matrix(c)

import pandas as pd

db_data = pd.read_csv("./duckdb/output.csv")
plain_data = pd.read_csv("./results/plaintext_aspirin_count.txt", header=None)
remove_columns = plain_data.columns[[13,-1,-2,-3]]
plain_data = plain_data.drop(columns=remove_columns)
plain_data.columns = db_data.columns

plain_data_list = plain_data.values.tolist()
db_data_list = db_data.values.tolist()

c = 0
for row in db_data_list:
    if row in plain_data_list:
        c += 1
    else:
        print(row)
print(c)