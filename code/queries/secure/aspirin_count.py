from Compiler.library import start_timer, stop_timer, and_
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

def sort_merge_join_uu(
        left: sint.Matrix, 
        right: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: sintbit(1)
    ) -> sint.Matrix:
    left_sorted = Matrix.create_from(left)
    right_sorted = Matrix.create_from(right)

    start_timer(1000)
    left_sorted.sort((l_key,))
    right_sorted.sort((r_key,))
    stop_timer(1000)

    result = sint.Matrix(
        rows=right_sorted.shape[0],
        columns=left_sorted.shape[1] + right_sorted.shape[1] + 1
    )
    result.assign_all(0)

    i = regint(0)
    j = regint(0)
    cnt = regint(0)
    rel = sint.Array(1).create_from(sint(1))

    @while_do(lambda: (i < left_sorted.shape[0]) & (j < right_sorted.shape[0]))
    def _():
        lt = (left_sorted[i][l_key] < right_sorted[j][r_key]).if_else(1,0)
        gt = (left_sorted[i][l_key] > right_sorted[j][r_key]).if_else(1,0)
        eq = (left_sorted[i][l_key] == right_sorted[j][r_key]).if_else(1,0)

        eqc = (eq & condition(left_sorted[i], right_sorted[j])).if_else(1,0)

        result[cnt] = (eqc).if_else(left_sorted[i].concat(right_sorted[j]).concat(rel), result[cnt])
        cnt.update(cnt+1)

        i_lt = lt.if_else((i + 1), i)
        j_gt = gt.if_else((j + 1), j)

        i_eq = (eqc).if_else((i + 1), i_lt)
        j_eq = (eqc).if_else((j + 1), j_gt)

        i.update(i_eq.reveal())
        j.update(j_eq.reveal())
    return result

def sort_merge_join_un(
        left: sint.Matrix, 
        right: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: sint(1)
    ) -> sint.Matrix:
    left_sorted = Matrix.create_from(left)
    right_sorted = Matrix.create_from(right)

    start_timer(1000)
    left_sorted.sort((l_key,))
    right_sorted.sort((r_key,))
    stop_timer(1000)

    result = sint.Matrix(
        rows=right.shape[0],
        columns=left.shape[1] + right.shape[1] + 1
    )
    result.assign_all(0)

    i = regint(0)
    j = regint(0)
    cnt = regint(0)

    @while_do(lambda: (i < left_sorted.shape[0]) & (j < right_sorted.shape[0]))
    def _():
        left_row = left_sorted[i]
        left_value = left_row[l_key]

        lt = (left_sorted[i][l_key] < right_sorted[j][r_key]).if_else(1,0).reveal()
        gt = (left_sorted[i][l_key] > right_sorted[j][r_key]).if_else(1,0).reveal()
        eq = (left_sorted[i][l_key] == right_sorted[j][r_key]).if_else(1,0).reveal()

        @if_(lt)
        def _():
            i.update(i+1)
        @if_(gt)
        def _():
            j.update(j+1)
        @if_(eq)
        def _():
            @while_do(and_(lambda: (j < right_sorted.shape[0]), lambda: (right_sorted[j][r_key] == left_value).if_else(1,0).reveal()))
            def _():
                @if_(condition(left_row, right_sorted[j]).reveal())
                def _():
                    rel = sint.Array(1).create_from(sint(1))
                    result[cnt] = left_sorted[i].concat(right_sorted[j].concat(rel))
                cnt.update(cnt+1)
                j.update(j+1)
            i.update(i+1)
    return result

def sort_merge_join_nn(
        left: sint.Matrix, 
        right: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: sintbit(1)
    ) -> sint.Matrix:
    left_sorted = Matrix.create_from(left)
    right_sorted = Matrix.create_from(right)

    start_timer(1000)
    left_sorted.sort((l_key,))
    right_sorted.sort((r_key,))
    stop_timer(1000)

    result = sint.Matrix(
        rows=left.shape[0]*right.shape[0],
        columns=left.shape[1] + right.shape[1] + 1
    )
    result.assign_all(0)

    i = regint(0)
    j = regint(0)
    cnt = regint(0)

    @for_range_opt(left_sorted.shape[0])
    def _(i):
        @for_range_opt(right_sorted.shape[0])
        def _(j):
            result[cnt] = (
                (left_sorted[i][l_key] == right_sorted[j][r_key]) &
                condition(left_sorted[i], right_sorted[j])
            ).if_else(
                left_sorted[i].concat(right_sorted[j]).concat(
                    sint.Array(1).create_from(sint(1))
                ),
                result[cnt]
            )
            cnt.update(cnt+1)
            lt = (left_sorted[i][l_key] < right_sorted[j][r_key]).if_else(1,0)
            @if_(lt.reveal())
            def _():
                break_loop()
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

max_rows = 10
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
join = sort_merge_join_uu(aw, bw, 0, 0, condition=join_condition)
stop_timer(300)

# start_timer(400)
# wlt = where_less_then(join, 2, aw.shape[1]+2)
# stop_timer(400)

def distinct_condition(row):
    return (
        # row[-1] == 1
        (row[-1] == 1) &
        (row[-2] == 1) &
        # (row[-3] == 1) &
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