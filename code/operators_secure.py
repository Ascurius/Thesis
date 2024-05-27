from Compiler.types import sint, regint
from Compiler.library import for_range_opt, if_

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

def join_nested_loop(
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

def order_by(matrix: sint.Matrix, order_key: int, relevance_key: int, reverse: bool = False) -> sint.Matrix:
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

def distinct_relevancy(matrix: sint.Matrix, key: int) -> sint.Matrix:
    """
    This variant of the DISTINCT operator varies from the normal
    implementation because it is not applied independently but rather
    at the end of a query with multiple preceeding operators where
    the relevancy column of each operator must be included when computing
    the DISTINCT operator.
    """
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
            (matrix[i][-1] == 1) & # Example of additional relevancy columns that need to be checked
            (matrix[i][-2] == 1) & # Example of additional relevancy columns that need to be checked
            (matrix[i][-3] == 1) & # Example of additional relevancy columns that need to be checked
            (matrix[i][13] == 1) # Example of additional relevancy columns that need to be checked
        ).if_else(sint(1),sint(0))
        result[i][-1] = dbit
        new_value = (dbit == 1).if_else(matrix[i][key], prev_value)
        prev_value.update(new_value)
    return result

def distinct(matrix: sint.Matrix, key: int) -> sint.Matrix:
    matrix.sort((key,))
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )

    prev_value = sint(-1)
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        dbit = (matrix[i][key] != prev_value).if_else(sint(1),sint(0))
        result[i][-1] = dbit
        new_value = (dbit == 1).if_else(matrix[i][key], prev_value)
        prev_value.update(new_value)
    return result

def row_number_over_partition_by(matrix: sint.Matrix, key: int, condition: Callable[[List[int]], bool] = lambda row: True):
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
        ## ...or a hardcoded condition like the one below (commented out)
        # adder = (matrix[i][13] == 1).if_else((count+1), count)
        count.update(adder)
        result[i][-1] = count
    return result