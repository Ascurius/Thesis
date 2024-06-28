from Compiler.library import start_timer, stop_timer
from typing import Callable, List

def select_distinct(
        matrix: sint.Matrix, 
        key: int, 
        condition: Callable[[sint.Array], bool] = lambda row: True
    ) -> sint.Matrix:
    start_timer(700)
    matrix.sort((key,))
    stop_timer(700)
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

def join_nested_loop(
        left: sint.Matrix, 
        right: sint.Matrix, 
        left_key: int, 
        right_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: True
    ) -> sint.Matrix:
    result = sint.Matrix(
        rows=left.shape[0] * right.shape[0],
        columns=left.shape[1] + right.shape[1] + 1
    )
    current_idx = regint(0)
    @for_range_opt(left.shape[0])
    def _(left_row):
        @for_range_opt(right.shape[0])
        def _(right_row):
            new_row = left[left_row].concat(right[right_row])
            result[current_idx].assign(new_row)
            result[current_idx][-1] = (
                (left[left_row][left_key] == right[right_row][right_key]) &
                condition(left[left_row], right[right_row])
            ).if_else(sint(1),sint(0))
            current_idx.update(current_idx + regint(1))
    return result

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

def where_less_then(matrix: sint.Matrix, col_1: int, col_2: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        result[i][-1] = (
            matrix[i][col_1] <= matrix[i][col_2]
        ).if_else(1,0)
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

max_rows = 10
print_ln("Executing plaintext_aspirin_count with %s rows", max_rows)
start_timer(10)
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)
stop_timer(10)

start_timer(100)
union = union_all(a, b)
stop_timer(100)

start_timer(200)
aw = where(union, 8, 414)
stop_timer(200)

start_timer(300)
bw = where(union, 4, 0)
stop_timer(300)

def join_condition(left, right):
    return (
        # (left[8] == 414) &
        # (right[4] == 0) &
        # (left[2] <= right[2])
        left[2] <= right[2]
    ).if_else(1,0)

start_timer(400)
join = join_nested_loop(aw, bw, 1, 1, join_condition)
stop_timer(400)

# start_timer(500)
# wlt = where_less_then(join, 2, aw.shape[1]+2)
# stop_timer(500)

def distinct_condition(row):
    return (
        row[-1] == 1
        # (row[-1] == 1) &
        # (row[-2] == 1) &
        # (row[-3] == 1) &
        # (row[13] == 1)
    ).if_else(1,0)

start_timer(600)
select = select_distinct(join, 0, condition=distinct_condition)
stop_timer(600)

count = regint(0)
start_timer(800)
@for_range_opt(select.shape[0])
def _(i):
    dbit_5 = (select[i][-1] == 1).if_else(1,0) # select distinct
    @if_(dbit_5.reveal())
    def _():
        count.update(count + 1)
stop_timer(800)
print_ln("%s", count)