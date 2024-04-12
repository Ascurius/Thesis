# from Compiler.types import sint
from Compiler.library import for_range_opt, if_, print_ln

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
col_a = a.get_column(2)
size_a = len(col_a.elements())
arr_a = sint.Array(size_a).create_from(col_a.elements())

b = sint.Matrix(p1_row, p1_col)
b.input_from(1)
col_b = b.get_column(2)
size_b = len(col_b.elements())
arr_b = sint.Array(size_b).create_from(col_b.elements())

def isInArray(element, array, size):
    @for_range_opt(size)
    def _(i):
        @if_(array[i].equal(element).reveal())
        def _():
            return True
    return False

# for i in range(arr_a.length):
#     for j in range(arr_b.length):
#         dbit = arr_a[i].equal(arr_b[j])
#         @if_(dbit.reveal())
#         def _():
#             # result_size[0].update(result_size[0] + 1)
#             result.append(arr_a[i])
    
def get_shape(arr):
    if isinstance(arr, list):
        return [len(arr)] + get_shape(arr[0])
    else:
        return []

def groub_by(array):
    result = []
    count = sint(1)
    last_element = sint(0)
    for i in range(0, array.length-1):
        s_arr = sint.Array(2)
        dbit = array[i].not_equal(last_element)
        @if_e(dbit.reveal())
        def _():
            s_arr[0] = array[i]
            count.update(sint(1))
        @else_
        def _():
            count.update(count + sint(1))
        print_ln("%s", s_arr.reveal_list())
    s_arr = sint.Array(2)
    s_arr[0], s_arr[1] = array[i-1], count
    result.append(s_arr)
    # s_result = MultiArray(get_shape(result), sint)
    # s_result.assign(result)
    return result

dummy_data = [20, 99, 20, 20, 10, 11, 12, 12, 23, 24, 10, 11]
arr_test = sint.Array(len(dummy_data))
arr_test.assign(dummy_data)
arr_test.sort()

res = groub_by(arr_test)
# for i in :
    # print_ln("Element: %s has count %s", i[0].get_type, i[1].get_type)
    # print_ln("Element: %s has count %s", i[0].reveal(), i[1].reveal())
    # print_ln("Element: %s has count %s", element.reveal(), count.reveal())