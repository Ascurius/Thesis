
def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        @if_(matrix[i][0].reveal())
        def _():
            print_ln("%s", matrix[i].reveal())

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

def count_relevant(matrix, relevancy_key):
    idx = regint(0)
    @for_range_opt(matrix.shape[0])
    def _(i):
        dbit = (matrix[i][relevancy_key] == 1).if_else(1,0)
        @if_(dbit.reveal())
        def _():
            idx.update(idx + 1)
    return idx


def select_distinct(matrix: sint.Matrix, key: int) -> sint.Matrix:
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
            (matrix[i][-1] == 1) &
            (matrix[i][-2] == 1) &
            (matrix[i][-3] == 1) &
            (matrix[i][13] == 1)
        ).if_else(sint(1),sint(0))
        result[i][-1] = dbit
        new_value = (dbit == 1).if_else(matrix[i][key], prev_value)
        prev_value.update(new_value)
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

def where(matrix, key, value):
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])
        result[i][-1] = (matrix[i][key] == value).if_else(1,0)
    return result

def where_less_then(matrix, col_1, col_2):
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

max_rows = 50
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)

aw = where(a, 8, 414)
bw = where(b, 4, 0)

join = inner_join_nested_loop(aw, bw, 1, 1)

wlt = where_less_then(join, 2, aw.shape[1]+2)

select = select_distinct(wlt, 0)

idx = regint(0)
@for_range_opt(select.shape[0])
def _(i):
    dbit_5 = (select[i][-1] == 1).if_else(1,0) # select distinct
    @if_(dbit_5.reveal())
    def _():
        print_ln("%s", select[i].reveal())
        idx.update(idx + 1)
print_ln("%s", idx)