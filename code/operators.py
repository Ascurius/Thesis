import numpy as np
from itertools import groupby
from Compiler.types import sint, regint
from Compiler.library import for_range_opt, if_

########################
#### Secure operators
########################

def select_columns(matrix: sint.Matrix, keys: list) -> sint.Matrix:
    keys.sort()
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=len(keys)
    )
    for i in range(len(keys)):
        result.set_column(
            i,
            matrix.get_column(keys[i])
        )
    return result

def select_by_array(matrix: sint.Matrix, keys: regint.Array) -> sint.Matrix:
    keys.sort()
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=keys.length
    )
    @for_range_opt(keys.length)
    def _(i):
        result.set_column(
            i,
            matrix.get_column(keys[i])
        )
    return result

def inner_join_nested_loop(
        left: sint.Matrix, 
        right: sint.Matrix, 
        left_key: int, 
        right_key: int
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
            new_row = sint.Array(result.shape[1])
            @for_range_opt(left.shape[1])
            def _(left_col):
                new_row[left_col] = left[left_row][left_col]
            @for_range_opt(right.shape[1])
            def _(right_col):
                new_row[left.shape[1]+right_col] = right[right_row][right_col]
            result[current_idx].assign(new_row)
            result[current_idx][-1] = (left[left_row][left_key] == right[right_row][right_key]).if_else(sint(1),sint(0))
            current_idx.update(current_idx + regint(1))
    return result

def order_by(matrix: sint.Matrix, key: int, reverse: bool = False):
    matrix.sort((key,))
    if reverse:
        result = sint.Matrix(
            rows=matrix.shape[0],
            columns=matrix.shape[1]
        )
        for i in range(matrix.shape[0] // 2):
            j = matrix.shape[0] - i - 1
            result[i], result[j] = matrix[j], matrix[i]
        return result

def groub_by_count_with_reveal(array: sint.Matrix):
    result = MultiArray([arr_test.length, 2], sint)
    count = sint(1)
    current_element = sint(0)
    @for_range_opt(array.length)
    def _(i):
        dbit = (array[i] != current_element).if_else(1,0).reveal()
        @if_e(dbit)
        def _():
            @if_((current_element != sint(0)).if_else(1,0).reveal())
            def _():
                result[i][0] = current_element
                result[i][1] = count
            current_element.update(array[i])
            count.update(sint(1))
        @else_
        def _():
            count.update(count + sint(1))
    @if_((current_element != sint(0)).if_else(1,0).reveal())
    def _():
        result[-1][0] = current_element
        result[-1][1] = count
    return result

def groub_by_count(matrix: sint.Matrix, key: int):
    matrix.sort((key,))
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]+2
    )
    for i in range(matrix.shape[0]):
        result[i].assign_vector(matrix[i])

    count = sint(0)
    rel = matrix.shape[1] # index of the relevancy column
    agg = matrix.shape[1] + 1 # index of the aggregation column
    current_element = sint(0)
    for i in range(matrix.shape[0]-1):
        result[i][rel] = (matrix[i][key] == matrix[i+1][key]).if_else(sint(0), sint(1))
        count = (matrix[i][key] == current_element).if_else((count+sint(1)), sint(1))
        current_element = (matrix[i][key] != current_element).if_else(matrix[i][key], current_element)
        result[i][agg] = count
    result[-1][rel] = sint(1)
    result[-1][agg] = (matrix[-1][key] == current_element).if_else((count+sint(1)), sint(1))
    return result

def limit(matrix: sint.Matrix, maximum: int, match_col: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    cnt = sint(0)
    for i in range(matrix.shape[0]):
        result[i].assign_vector(matrix[i])
        cnt = (matrix[i][match_col] == sint(1)).if_else(
            (cnt+sint(1)), cnt
        )
        result[i][matrix.shape[1]] = (
            (matrix[i][match_col] == sint(1)) & (cnt <= sint(5))
        ).if_else(sint(1), sint(0))
    return result

########################
#### Plaintext operators
########################

def select_columns(matrix: np.ndarray, columns: list) -> np.ndarray:
    columns.sort()
    return matrix[:, columns]

def group_by_count(matrix: np.ndarray, key: int) -> np.ndarray:
    column = sorted(matrix[:, key])
    return np.array(
        ([(k, len(list(g))) for k, g in groupby(column)])
    )

def order_by(matrix, keys, reversed=False):
    sorted_matrix = sorted(matrix, key=lambda x: (x[keys[1]], x[keys[0]]), reverse=reversed)
    return np.array(sorted_matrix)

def limit(matrix, maximum):
    return matrix[:maximum]