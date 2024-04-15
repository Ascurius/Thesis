# a = sint(1)
# b = sint(2)

# dbit = (a != b).if_else(1,0)
# @if_(dbit)
# def _():
#     print_ln("Not equal")

def groub_by(matrix, key):
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
    for i in range(matrix.shape[0]-1):
        result[i][rel] = (matrix[i][key] == matrix[i+1][key]).if_else(sint(0),sint(1))
        adder = (matrix[i][key] == matrix[i+1][key]).if_else(1,0)
        count = (result[i][rel] == 1).if_else(sint(1), count)
        count = count + adder
        result[i+1][agg] = count
    return result