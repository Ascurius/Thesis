
def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        @if_(matrix[i][0].reveal())
        def _():
            print_ln("%s", matrix[i].reveal())

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

def select_relevant(matrix):
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]
    )
    idx = regint(0)
    @for_range_opt(matrix.shape[0])
    def _(i):
        dbit = (matrix[i][-1] & matrix[i][-2]).if_else(1,0)
        @if_(dbit.reveal())
        def _():
            result[idx].assign_vector(matrix[i])
            idx.update(idx + 1)
    return result

def count_relevant(matrix, relevancy_key):
    idx = regint(0)
    @for_range_opt(matrix.shape[0])
    def _(i):
        dbit = (matrix[i][relevancy_key] == 1).if_else(1,0)
        @if_(dbit.reveal())
        def _():
            idx.update(idx + 1)
    return idx


def select_distinct(matrix: sint.Matrix, column: int) -> sint.Matrix:
    # matrix.sort((column,))
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
        dbit_join = (matrix[i][-1] == 1).if_else(1,0)
        dbit_wa = (matrix[i][a.shape[1]] == 1).if_else(1,0)
        dbit_wb = (matrix[i][-2] == 1).if_else(1,0)
        dbit_rel = (matrix[i][column] == matrix[i+1][column]).if_else(0,1)
        result[i][rel] = (dbit_join & dbit_wa & dbit_wb & dbit_rel).if_else(1,0)

        # print_ln("i: %s, i+1: %s", matrix[i][column].reveal(), matrix[i+1][column].reveal())
        # print_ln("JOIN: %s", matrix[i][-1].reveal())
        # print_ln("WHERE (for table a): %s", matrix[i][a.shape[1]].reveal())
        # print_ln("WHERE (for table b): %s", matrix[i][-2].reveal())
        # print_ln("i: %s, i+1: %s, dbit: %s", matrix[i][column].reveal(), matrix[i+1][column].reveal(), result[i][rel].reveal())
        # result[i][rel] = dbit
        # @if_(dbit.reveal())
        # def _():
        #     print_ln("i: %s, i+1: %s", matrix[i][column].reveal(), matrix[i+1][column].reveal())
        #     print_ln("JOIN: %s", matrix[i][-1].reveal())
        #     print_ln("WHERE (for table b): %s", matrix[i][a.shape[1]-1].reveal())
        #     print_ln("WHERE (for table a): %s", matrix[i][-2].reveal())
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


max_rows = 50
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)

aw = where(a, 8, 414)
bw = where(b, 4, 0)

matrix = inner_join_nested_loop(a, b, 1, 1)

# matrix = select_distinct(matrix, 0)

idx = regint(0)
@for_range_opt(matrix.shape[0])
def _(i):
    join = (matrix[i][-1] == 1).if_else(1,0)
    where_a = (matrix[i][aw.shape[1]] == 1).if_else(1,0)
    where_b = (matrix[i][-2] == 1).if_else(1,0)
    # dbit = (join & where_a & where_b).if_else(1,0)
    dbit = (matrix[i][-1] == 1).if_else(1,0)
    @if_(dbit.reveal())
    def _():
        # print_ln("%s %s %s", join.reveal(), where_a.reveal(), where_b.reveal())
        print_ln("%s", matrix[i].reveal())
        idx.update(idx + 1)
print_ln("%s", idx)