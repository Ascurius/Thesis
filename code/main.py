

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

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

def order_by(matrix: sint.Matrix, order_key: int, relevance_key: int, reverse: bool = False):
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1] + 1
    )
    for i in range(matrix.shape[0]):
        result[i] = matrix[i]
        result[i][matrix.shape[1]] = matrix[i][order_key] * matrix[i][relevance_key]
    result.sort((matrix.shape[1],))
    if reverse:
        swap = result.same_shape()
        for i in range(result.shape[0] // 2):
            j = result.shape[0] - i - 1
            swap[i], swap[j] = result[j], result[i]
        return swap
    return result

def limit(matrix: sint.Matrix, maximum: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=maximum,
        columns=matrix.shape[1]
    )
    for i in range(maximum):
        result[i].assign_vector(matrix[i])
    return result


p0_row, p0_col = get_matrix_dimensions("Player-Data/Input-P1-0")

a = sint.Matrix(p0_row, p0_col)
a.input_from(1)

s = select_by_list(a, [1])
g = groub_by_count(s, 0)
o = order_by(g, order_key=-1, relevance_key=-2, reverse=True)

l = limit(o, 5)
print_matrix(select_by_list(l, [0,3]))