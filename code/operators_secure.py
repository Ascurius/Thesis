from typing import Callable, List, Tuple
from Compiler.types import sint, regint
from Compiler.library import for_range_opt, while_do, break_loop, if_, if_e, else_, start_timer, stop_timer

########################
#### Secure operators
########################

def select_columns(matrix: sint.Matrix, keys: regint.Array) -> sint.Matrix:
    keys.sort()
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=len(keys)
    )
    @for_range_opt(len(keys))
    def _(i):
        result.set_column(
            i,
            matrix.get_column(keys[i])
        )
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

def sort_merge_join_uu(
        left_in: sint.Matrix, 
        right_in: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: sint(1)
    ) -> sint.Matrix:
    left = left_in.same_shape()
    right = right_in.same_shape()

    @for_range_opt(left_in.shape[0])
    def _(i):
        left[i].assign(left_in[i])

    @for_range_opt(right_in.shape[0])
    def _(i):
        right[i].assign(right_in[i])

    start_timer(1000)
    left.sort((l_key,))
    right.sort((r_key,))
    stop_timer(1000)

    result = sint.Matrix(
        rows=right.shape[0],
        columns=left.shape[1] + right.shape[1] + 1
    )
    result.assign_all(0)

    i = regint(0)
    j = regint(0)
    cnt = regint(0)
    rel = sint.Array(1).create_from(sint(1))

    @while_do(lambda: (i < left.shape[0]) & (j < right.shape[0]))
    def _():
        lt = (left[i][l_key] < right[j][r_key]).if_else(1,0)
        gt = (left[i][l_key] > right[j][r_key]).if_else(1,0)
        eq = (left[i][l_key] == right[j][r_key]).if_else(1,0)

        @if_(lt.reveal())
        def _():
            i.update(i+1)
        @if_(gt.reveal())
        def _():
            j.update(j+1)
        @if_(eq.reveal())
        def _():
            result[cnt] = left[i].concat(right[j]).concat(rel)
            cnt.update(cnt+1)
            i.update(i+1)
            j.update(j+1)
    return result

def sort_merge_join_un(
        left: sint.Matrix, 
        right: sint.Matrix, 
        l_key: int, 
        r_key: int,
        condition: Callable[[sint.Array, sint.Array], bool] = lambda left, right: sint(1)
    ) -> sint.Matrix:
    left_sorted = left.same_shape()
    right_sorted = right.same_shape()

    @for_range_opt(left.shape[0])
    def _(i):
        left_sorted[i].assign(left[i])

    @for_range_opt(right.shape[0])
    def _(i):
        right_sorted[i].assign(right[i])

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

def order_by(matrix: sint.Matrix, order_key: int, relevance_key: int, reverse: bool = False):
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i] = matrix[i]
        result[i][matrix.shape[1]] = matrix[i][order_key] * matrix[i][relevance_key]
    result.sort((matrix.shape[1],))
    if reverse:
        swap = result.same_shape()
        @for_range_opt(result.shape[0] // 2)
        def _(i):
            j = result.shape[0] - i - 1
            swap[i], swap[j] = result[j], result[i]
        return swap
    return result

def group_by_count(matrix: sint.Matrix, key: int) -> sint.Matrix:
    matrix.sort((key,))
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

def limit(matrix: sint.Matrix, maximum: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=maximum,
        columns=matrix.shape[1]
    )
    @for_range_opt(maximum)
    def _(i):
        result[i].assign_vector(matrix[i])
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

def select_distinct(
        matrix: sint.Matrix, 
        key: int, 
        condition: Callable[[sint.Array], bool] = lambda row: True
    ) -> sint.Matrix:
    matrix.sort((key,))
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

def where_condition(
        matrix: sint.Matrix, 
        comparison_func: Callable[[sint.Array], bool]
    ) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        result[i][-1] = (comparison_func(matrix[i])).if_else(1,0)
    return matrix