
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

def groub_by_count(matrix: sint.Matrix, key: int):
    matrix.sort((key,))
    result = sint.Matrix(
        rows=matrix.shape[0],
        columns=matrix.shape[1]+2
    )
    @for_range_opt(matrix.shape[0])
    def _(i):
        result[i].assign_vector(matrix[i])

    count = sint(0)
    rel = matrix.shape[1] # index of the relevancy column
    agg = matrix.shape[1] + 1 # index of the aggregation column
    current_element = sint(0)
    @for_range_opt(matrix.shape[0]-1)
    def _(i):
        nonlocal current_element
        result[i][rel] = (matrix[i][key] == matrix[i+1][key]).if_else(sint(0), sint(1))
        adder = (matrix[i][key] == current_element).if_else((count+sint(1)), sint(1))
        count.update(adder)
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

def limit(matrix: sint.Matrix, maximum: int) -> sint.Matrix:
    result = sint.Matrix(
        rows=maximum,
        columns=matrix.shape[1]
    )
    @for_range_opt(maximum)
    def _(i):
        result[i].assign_vector(matrix[i])
    return result


a = sint.Matrix(50, 13)
a.input_from(0)

columns = Array(1, regint)
columns[0] = 1

s = select_columns(a, columns)
g = groub_by_count(s, 0)
o = order_by(g, order_key=-1, relevance_key=-2, reverse=True)

l = limit(o, 5)