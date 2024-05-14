
def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matches(matrix: sint.Matrix, match_keys: list):
    for row in range(matrix.shape[0]):
        if all(matrix[row][col] for col in match_keys):
            print_ln("%s", matrix[row].reveal())

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

def where(matrix: sint.Matrix, key: int, value: int) -> sint.Matrix:
    pass


max_rows = 10
a = sint.Matrix(max_rows, 13)
a.input_from(0)

b = sint.Matrix(max_rows, 13)
b.input_from(1)

j = inner_join_nested_loop(a, b, 1, 1)

s = select_distinct(j, 1)

result = sint.Matrix(
    rows=a.shape[0],
    columns=a.shape[1] + 1
)
@for_range_opt(a.shape[0])
def _(i):
    result[i].assign_vector(a[i])

@for_range_opt(a.shape[0])
def _(i):
    dbit_1 = (a[i][8] == 414).if_else(sint(1), sint(0))
    dbit_2 = (b[i][4] == 0).if_else(sint(1), sint(0))
    dbit_3 = (a[i][2] <= b[i][2]).if_else(sint(1), sint(0))
    dbit_final = dbit_1.bit_and(dbit_2.bit_and(dbit_3))
    result[i][a.shape[1]] = dbit_final

# @for_range_opt(s.shape[0])
# def _(row):
#     dbit = ((s[row][s.shape[1]-1].reveal() == sint(1)) and (s[row][s.shape[1]-2].reveal() == sint(1))).if_else(0,1)
#     @if_(dbit.reveal())
#     def _():
#         print_ln("%s", s[row].reveal())