# from Compiler.types import sint
from Compiler.library import for_range_opt, print_ln, print_ln_if

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def get_matrix_dimensions(filename):
    num_rows = 0
    num_cols = None

    with open(filename, 'r') as file:
        for line in file:
            # Increment row count for each line
            num_rows += 1

            # Split the line into integers
            row_data = line.strip().split()

            # Check if the number of columns is consistent
            if num_cols is None:
                num_cols = len(row_data)
            elif num_cols != len(row_data):
                raise ValueError("Inconsistent number of columns in the matrix")

    return num_rows, num_cols

p0_row, p0_col = get_matrix_dimensions("Player-Data/Input-P0-0")
p1_row, p1_col = get_matrix_dimensions("Player-Data/Input-P1-0")

a = sint.Matrix(p0_row, p0_col)
a.input_from(0)

b = sint.Matrix(p1_row, p1_col)
b.input_from(1)

# def select(matrix, keys):
#     result = sint.Matrix(
#         rows=matrix.shape[0],
#         columns=keys.length
#     )
#     @for_range(keys.length)
#     def _(i):
#         result.set_column(
#             i,
#             matrix.get_column(keys[i])
#         )
#     return result

# def select(matrix, keys):
#     result = sint.Matrix(
#         rows=matrix.shape[0],
#         columns=len(keys)
#     )
#     for i in range(len(keys)):
#         result.set_column(
#             i,
#             matrix.get_column(keys[i])
#         )
#     return result
        
# keys = [1,2,3]
# arr_keys = regint.Array(len(keys))
# arr_keys.assign(keys)

