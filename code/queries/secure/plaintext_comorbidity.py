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
    start_timer(400)
    sort_by_two_cols(matrix, key, 2)
    stop_timer(400)
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
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    start_timer(600)
    result.sort((order_key,))
    stop_timer(600)
    if reverse:
        swap = result.same_shape()
        @for_range_opt(result.shape[0] // 2)
        def _(i):
            j = result.shape[0] - i - 1
            swap[i], swap[j] = result[j], result[i]
        return swap
    return result

def limit(matrix: sint.Matrix, maximum: int, relevancy_col: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]
    )
    count = sint(0)
    @for_range_opt(result.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        result[i][relevancy_col] = (count > maximum).if_else(0, result[i][relevancy_col])
        adder = (result[i][relevancy_col] == 1).if_else((count+1),count)
        count.update(adder)
    return result

def union_all(left, right):
    result = sint.Matrix(
        rows=left.shape[0] + right.shape[0],
        columns=left.shape[1]
    )
    @for_range_opt(left.shape[0])
    def _(i):
        result[i].assign_vector(left[i])
    @for_range_opt(right.shape[0])
    def _(j):
        result[left.shape[0] + j].assign_vector(right[j])
    return result

max_rows = 600000
print_ln("Executing plaintext_comorbidity with %s rows", max_rows)
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)

start_timer(100)
u = union_all(a,b)
stop_timer(100)

keys = Array.create_from(regint([1]))
start_timer(200)
s = select_columns(a, keys)
stop_timer(200)

start_timer(300)
g = group_by_count(s, 0)
stop_timer(300)

start_timer(500)
o = order_by(g, order_key=2, reverse=True)
stop_timer(500)

start_timer(700)
matrix = limit(o, 10, -2)
stop_timer(700)