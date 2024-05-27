
from typing import Callable, List

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
        adder = (matrix[i][key] == current_element).if_else((count+sint(1)), sint(1))

        current_element.update(matrix[i][key])
        count.update(adder)

        result[i][-2] = (matrix[i][key] == matrix[i+1][key]).if_else(sint(0), sint(1))
        result[i][-1] = count
    result[-1][-2] = sint(1)
    result[-1][-1] = (matrix[-1][key] == current_element).if_else((count+sint(1)), sint(1))
    return result

def order_by(matrix: sint.Matrix, order_key: int, relevance_key: int = None, reverse: bool = False):
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i] = matrix[i]
        result[i][matrix.shape[1]] = matrix[i][order_key] * (matrix[i][relevance_key] if relevance_key is not None else 1)
    result.sort((matrix.shape[1],))
    if reverse:
        swap = result.same_shape()
        @for_range_opt(result.shape[0] // 2)
        def _(i):
            j = result.shape[0] - i - 1
            swap[i], swap[j] = result[j], result[i]
        return swap
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

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())


a = sint.Matrix(50, 13)
a.input_from(0)

g = group_by_count(a, 1)
o = order_by(g, order_key=-1, relevance_key=-2, reverse=True)

l = limit(o, 10)

print_matrix(l)