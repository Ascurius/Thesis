

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matched(matrix, match_key):
    for i in range(matrix.shape[0]):
        dbit = (matrix[i][match_key] == 1).if_else(1,0)
        @if_(dbit.reveal())
        def _():
            print_ln("%s", matrix[i].reveal())

def get_matrix_dimensions(filename):
    num_rows = 0
    num_cols = None

    with open(filename, 'r') as file:
        for line in file:
            # Increment row count for each line
            num_rows += 1

            # Split the line into integers
            row_data = line.strip().split()

            # Check if the number of columns is consistent
            if num_cols is None:
                num_cols = len(row_data)
            elif num_cols != len(row_data):
                raise ValueError("Inconsistent number of columns in the matrix")

    return num_rows, num_cols

def select_by_list(matrix: sint.Matrix, keys: list) -> sint.Matrix:
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

def limit(matrix: sint.Matrix, n_rows: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=n_rows,
        columns=matrix.shape[1]
    )
    for i in range(n_rows):
        print_ln("%s", matrix[i].reveal())
        result[i] = matrix[i]
    return result

p0_row, p0_col = get_matrix_dimensions("Player-Data/Input-P0-0")

a = sint.Matrix(p0_row, p0_col)
a.input_from(0)

def select_relevant(matrix: sint.Matrix, match_key: int) -> sint.Matrix:
    count = regint(0)
    vec = matrix.get_column(match_key)
    for i in range(len(vec.elements())):
        @if_(vec.elements()[i].reveal())
        def _():
            count.update(count+1)
    result = sint.Matrix(
        rows=count,
        columns=matrix.shape[1]
    )
    result_row = regint(0)
    for i in range(matrix.shape[0]):
        dbit = (matrix[i][match_key] == 1).if_else(1,0)
        @if_(dbit)
        def _():
            result[result_row] = matrix[i]
            result_row.update(result_row+1)
    return result


s = select_by_list(a, [0,2])
g = groub_by_count(s, 1)
o = order_by(g, -1, reverse=True)
l = limit(o, 5)
print_matched(l, 2)