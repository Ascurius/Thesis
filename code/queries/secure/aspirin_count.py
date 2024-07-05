from Compiler.library import start_timer, stop_timer
from typing import Callable, List

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

max_rows = 700
print_ln("Executing aspirin_count with %s rows", max_rows)
start_timer(10)
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)
stop_timer(10)

start_timer(100)
aw = where(a, 8, 414)
stop_timer(100)
start_timer(200)
bw = where(b, 4, 0)
stop_timer(200)

def join_condition(left, right):
    return (
        # (left[8] == 414) &
        # (right[4] == 0) &
        # (left[2] <= right[2])
        left[2] <= right[2]
    ).if_else(1,0)

start_timer(300)
join = sort_merge_join(aw, bw, 1, 1)
stop_timer(300)

# start_timer(400)
# wlt = where_less_then(join, 2, aw.shape[1]+2)
# stop_timer(400)

def distinct_condition(row):
    return (
        # row[-1] == 1
        (row[-1] == 1) &
        (row[-2] == 1) &
        (row[-3] == 1) &
        (row[13] == 1)
    ).if_else(1,0)

start_timer(500)
select = select_distinct(join, 0, condition=distinct_condition)
stop_timer(500)

count = regint(0)
start_timer(700)
@for_range_opt(select.shape[0])
def _(i):
    dbit_5 = (select[i][-1] == 1).if_else(1,0) # select distinct
    @if_(dbit_5.reveal())
    def _():
        count.update(count + 1)
stop_timer(700)
print_ln("%s", count)