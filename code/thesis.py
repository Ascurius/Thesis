# from Compiler.types import cint
from Compiler.library import for_range_opt, print_ln

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
# p1_row, p1_col = get_matrix_dimensions("Player-Data/Input-P1-0")

a = sint.Matrix(p0_row, 5)
a.input_from(0)
a.sort((1,))

print_ln("%s", a.get_column(1).reveal())

def refill_matrix(target, source):
    assert target.shape[0] >= source.shape[0]
    for i in range(source.shape[0]):
        target[i].assign_vector(source[i])

def increase(count):
    count += 1
    return count

def groub_by(matrix, key):
    matrix.sort((key,))
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]+2
    )
    for i in range(matrix.shape[0]):
        result[i].assign_vector(matrix[i])

    count = sint(0)
    rel = matrix.shape[1] # index of the relevancy column
    agg = matrix.shape[1] + 1 # index of the aggregation column
    current_element = sint(0)
    for i in range(matrix.shape[0]-1):
        result[i][rel] = (matrix[i][key] == matrix[i+1][key]).if_else(sint(0), sint(1))
        count = (matrix[i][key] == current_element).if_else((count+sint(1)), sint(1))
        current_element = (matrix[i][key] != current_element).if_else(matrix[i][key], current_element)
        result[i][agg] = count
    result[-1][rel] = sint(1)
    result[-1][agg] = (matrix[-1][key] == current_element).if_else((count+sint(1)), sint(1))
    return result
        
# dummy_data = [20, 99, 20, 20, 10, 11, 12, 12, 23, 24, 10, 11]
# arr_test = sint.Array(len(dummy_data))
# arr_test.assign(dummy_data)
# arr_test.sort()

print_matrix(groub_by(a, 1))