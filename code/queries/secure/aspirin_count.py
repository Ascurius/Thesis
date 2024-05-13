
def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matches(matrix: sint.Matrix, match_keys: list):
    for row in range(matrix.shape[0]):
        for column in match_keys:
            if matrix[row][column].reveal() == 1:
                println(matrix[row].reveal())

def select_distinct(matrix: sint.Matrix, column: int) -> sint.Matrix:
    matrix.sort((column, ))

    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])

    rel = matrix.shape[1] # index of the relevancy column
    @for_range_opt(matrix.shape[0]-1)
    def _(i):
        result[i][rel] = (matrix[i][column] == matrix[i+1][column]).if_else(sint(0), sint(1))
    result[-1][rel] = sint(1)
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

a = sint.Matrix(100, 13)
a.input_from(0)

b = sint.Matrix(100, 13)
b.input_from(1)

j = inner_join_nested_loop(a, b, 1, 1)

s = select_distinct(j, 1)


print_matrix(s)
# print_matches(s, [-1, ])