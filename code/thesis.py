from Compiler.types import cint
# from Compiler.library import for_range_opt, if_, print_ln

# def print_matrix(matrix):
#     for i in range(matrix.shape[0]):
#         print_ln("%s", matrix[i].reveal())

# def get_matrix_dimensions(filename):
#     num_rows = 0
#     num_cols = None

#     with open(filename, 'r') as file:
#         for line in file:
#             # Increment row count for each line
#             num_rows += 1

#             # Split the line into integers
#             row_data = line.strip().split()

#             # Check if the number of columns is consistent
#             if num_cols is None:
#                 num_cols = len(row_data)
#             elif num_cols != len(row_data):
#                 raise ValueError("Inconsistent number of columns in the matrix")

#     return num_rows, num_cols

# p0_row, p0_col = get_matrix_dimensions("Player-Data/Input-P0-0")
# p1_row, p1_col = get_matrix_dimensions("Player-Data/Input-P1-0")

# a = sint.Matrix(p0_row, p0_col)
# a.input_from(0)
# col_a = a.get_column(2)
# size_a = len(col_a.elements())
# arr_a = sint.Array(size_a).create_from(col_a.elements())

# b = sint.Matrix(p1_row, p1_col)
# b.input_from(1)
# col_b = b.get_column(2)
# size_b = len(col_b.elements())
# arr_b = sint.Array(size_b).create_from(col_b.elements())

def groub_by(array):
    space = sint.Array(array.length)
    # result = MultiArray([arr_test.length, 2], sint)
    arr_count = sint.Array(None, address=space.address)
    arr_value = sint.Array(None, address=space.address)
    count = sint(1)
    current_element = sint(0)
    idx = regint(0)
    @for_range_opt(array.length)
    def _(i):
        dbit = (array[i] != current_element).if_else(1,0).reveal()
        @if_e(dbit)
        def _():
            @if_((current_element != sint(0)).if_else(1,0).reveal())
            def _():
                arr_value[idx] = current_element
                arr_count[idx] = count
                idx.update(idx + regint(1))
            current_element.update(array[i])
            count.update(sint(1))
        @else_
        def _():
            count.update(count + sint(1))
    @if_((current_element != sint(0)).if_else(1,0).reveal())
    def _():
        arr_value[idx+1] = current_element
        arr_count[idx+1] = count
    print_ln("%s", arr_value.reveal_list())
    result = sint.Matrix(rows=2, columns=arr_value.length)
    result.set_column(0, arr_value)
    result.set_column(1, arr_count)
    return arr_value, arr_count

dummy_data = [20, 99, 20, 20, 10, 11, 12, 12, 23, 24, 10, 11]
arr_test = sint.Array(len(dummy_data))
arr_test.assign(dummy_data)
arr_test.sort()

res = groub_by(arr_test)
# print_ln("%s", res.reveal_list())
# print_ln("%s", res)
# for i in res:
#     # print_ln("Element: %s has count %s", i[0].get_type, i[1].get_type)
    # print_ln("Element: %s has count %s", i[0].reveal(), i[1].reveal())
    # print_ln("%s", i)