from Compiler.types import sint
from Compiler.library import for_range_opt, if_


########################
#### Secure operators
########################

def inner_join_nested_loop(left, right, left_key, right_key):
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

def order_by(table, key):
    table.sort((key,))

def groub_by_with_reveal(array):
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

def groub_by_count(matrix, key):
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

########################
#### Plaintext operators
########################

def group_by(arr):
    result = []
    count = 1
    current_element = None
    for i in range(len(arr)):
        if arr[i] != current_element:
            if current_element is not None:
                result.append([current_element, count])
            current_element = arr[i]
            count = 1
        else:
            count += 1
    if current_element is not None:
        result.append([current_element, count])
    return result