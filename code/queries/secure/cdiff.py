from Compiler.library import start_timer, stop_timer
from typing import Callable
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

def where(matrix: sint.Matrix, key: int, value: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        result[i][-1] = (matrix[i][key] == value).if_else(1,0)
    return result

def sort_merge_join(
        left: sint.Matrix, 
        right: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: True
    ) -> sint.Matrix:
    start_timer(1000)
    left.sort((l_key,))
    right.sort((r_key))
    stop_timer(1000)

    result = sint.Matrix(
        rows=left.shape[0]*right.shape[0],
        columns=left.shape[1] + right.shape[1] + 1
    )
    result.assign_all(0)

    i = regint(0)
    j = regint(0)
    mark = regint(-1)
    cnt = regint(0)

    @while_do(lambda: (i < left.shape[0]) & (j < right.shape[0]+1))
    def _():
        @if_(j >= right.shape[0])
        def _():
            j.update(mark)
            i.update(i+1)
            mark.update(-1)
            @if_(i >= len(left))
            def _():
                break_loop()
        @if_(mark == -1)
        def _():
            @while_do(lambda: (left[i][l_key] < right[j][l_key]).if_else(1,0).reveal())
            def _():
                i.update(i+1)
            @while_do(lambda: (left[i][l_key] > right[j][l_key]).if_else(1,0).reveal())
            def _():
                j.update(j+1)
            mark.update(j)
        @if_e((left[i][l_key] == right[j][l_key]).if_else(1,0).reveal())
        def _():
            @if_(condition(left[i], right[j]).reveal())
            def _():
                rel = sint.Array(1).create_from(sint(1))
                result[cnt] = left[i].concat(right[j].concat(rel))
                cnt.update(cnt+1)
            j.update(j+1)
        @else_
        def _():
            j.update(mark)
            i.update(i+1)
            mark.update(-1)
    return result

def row_number_over_partition_by(
        matrix: sint.Matrix, 
        key: int, 
        condition: Callable[[sint.Array], bool] = lambda row: True
    ) -> sint.Matrix:
    matrix.sort((key,))
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])

    count = sint(0)
    current_element = sint(0)
    @for_range_opt(matrix.shape[0]-1)
    def _(i):
        new_count = (matrix[i][key] != current_element).if_else(0,count)
        count.update(new_count)

        current_element.update(matrix[i][key])

        adder = (condition(matrix[i])).if_else((count+1), count)
        count.update(adder)
        result[i][-1] = count
    return result

def select_distinct(
        matrix: sint.Matrix, 
        key: int, 
        condition: Callable[[sint.Array], bool] = lambda row: True
    ) -> sint.Matrix:
    start_timer(600)
    matrix.sort((key,))
    stop_timer(600)
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )

    prev_value = sint(-1)
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        dbit = (
            (matrix[i][key] != prev_value) &
            condition(matrix[i])
        ).if_else(sint(1),sint(0))
        result[i][-1] = dbit
        new_value = (dbit == 1).if_else(matrix[i][key], prev_value)
        prev_value.update(new_value)
    return result

max_rows = 100
print_ln("Executing cdiff with %s rows", max_rows)
start_timer(10)
a = sint.Matrix(max_rows, 13)
a.input_from(0)
stop_timer(10)

start_timer(100)
w = where(a, 8, 8)
stop_timer(100)

start_timer(200)
# w.sort((1,2))
sort_by_two_cols(w, 1, 2)
stop_timer(200)


start_timer(300)
diags = row_number_over_partition_by(w, 1, condition=lambda row: row[13] == 1)
stop_timer(300)

def join_condition(left, right):
    return (
        (abs(left[2] - right[2]) >= 15) &
        (abs(left[2] - right[2]) <= 56) &
        (left[14]+1 == right[14])
    ).if_else(1,0)

start_timer(400)
join = sort_merge_join(
    diags, diags, 1, 1,
    condition=join_condition
)
stop_timer(400)

def distinct_condition(row):
    dbit = (
        (row[13] == 1) & # where left
        (row[-1] == 1) & # join
        (row[-3] == 1) # where right
    ).if_else(1,0)
    return dbit

start_timer(500)
selection = select_distinct(join, 1, condition=distinct_condition)
stop_timer(500)

c = sint(0)
@for_range(selection.shape[0])
def _(i):
    dbit = (selection[i][-1] == 1).if_else(1,0)
    @if_(dbit.reveal())
    def _():
        c.update(c+1)
print_ln("%s", c.reveal())

