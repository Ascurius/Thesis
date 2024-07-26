from Compiler.library import start_timer, stop_timer
from typing import Callable, List
from Compiler.sorting import radix_sort_from_matrix
from Compiler.util import tuplify

def sort_by_two_cols(matrix: sint.Matrix, key1: int, key2: int):
    # Create key indices tuples
    col_1 = (None,) + tuplify((key1,))
    col_2 = (None,) + tuplify((key2,))

    # Retrieve vector from original matrix by key indices
    X = matrix.get_vector_by_indices(*col_1)
    Y = matrix.get_vector_by_indices(*col_2)

    # Decompose the matrices vectors to list of bits
    x_bits = X.bit_decompose(50)
    y_bits = Y.bit_decompose(50)

    # Create matrix from both bit
    bs = Matrix.create_from(y_bits + x_bits)
    # bs = Matrix.create_from(x_bits)
    bs[-1][:] = bs[-1][:].bit_not() # Because len(bs) > 1

    radix_sort_from_matrix(bs, matrix)

def select_columns(matrix: sint.Matrix, keys: sint.Array) -> sint.Matrix:
    # keys.sort()
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=len(keys)
    )
    @for_range_opt(keys.length)
    def _(i):
        result.set_column(
            i,
            matrix.get_column(keys[i])
        )
    return result

def group_by_count(matrix: sint.Matrix, key: int) -> sint.Matrix:
    # matrix.sort((key,2))
    # matrix.sort((key,))
    start_timer(300)
    sort_by_two_cols(matrix, key, 2)
    stop_timer(300)
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 2
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])

    count = sint(0)
    current_element = sint(0)
    @for_range_opt(matrix.shape[0]-1)
    def _(i):
        adder = (matrix[i][key] == current_element).if_else(
            (count+sint(1)), sint(1)
        )
        current_element.update(matrix[i][key])
        count.update(adder)
        result[i][-2] = (matrix[i][key] == matrix[i+1][key]).if_else(
            sint(0), sint(1)
        )
        result[i][-1] = count
    result[-1][-2] = sint(1)
    result[-1][-1] = (matrix[-1][key] == current_element).if_else(
        (count+sint(1)), sint(1)
    )
    return result

def order_by(matrix: sint.Matrix, order_key: int, reverse: bool = False):
    start_timer(500)
    matrix.sort((order_key,))
    stop_timer(500)
    if reverse:
        swap = sint.Matrix(
            rows=matrix.shape[0],
            columns=matrix.shape[1]
        )
        @for_range_opt(matrix.shape[0] // 2)
        def _(i):
            j = matrix.shape[0] - i - 1
            swap[i], swap[j] = matrix[j], matrix[i]
        return swap
    return matrix

def limit(matrix: sint.Matrix, maximum: int, relevancy_col: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]
    )
    count = sint(0)
    @for_range_opt(result.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        adder = (result[i][relevancy_col] == 1).if_else(1, 0)
        new_count = count + adder
        result[i][relevancy_col] = (new_count > maximum).if_else(0, result[i][relevancy_col])
        next_count = (new_count > maximum).if_else(count, new_count)
        count.update(next_count)
    return result

max_rows = 100
print_ln("Executing comorbidity with %s rows", max_rows)
start_timer(10)
a = sint.Matrix(max_rows, 13)
a.input_from(0)
stop_timer(10)

keys = Array.create_from(regint([1]))
start_timer(100)
s = select_columns(a, keys)
stop_timer(100)

start_timer(200)
g = group_by_count(s, 0)
stop_timer(200)

start_timer(400)
o = order_by(g, order_key=2, reverse=True)
stop_timer(400)

start_timer(600)
matrix = limit(o, 10, -2)
stop_timer(600)