# from Compiler.types import sint
# from Compiler.library import for_range_opt, if_

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
p2_row, p2_col = get_matrix_dimensions("Player-Data/Input-P2-0")

a = sint.Matrix(p0_row, p0_col)
a.input_from(0)

# a = Matrix(p0_row, p0_col, sint)
# a.input_from(0)

# b = sint.Matrix(p1_row, p1_col)
# b.input_from(1)

# c = sint.Matrix(p2_row, p2_col)
# c.input_from(2)

def order_by(table, key):
    table.sort((key,))

order_by(a, 4)
print_matrix(a)