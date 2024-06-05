from Compiler.sorting import radix_sort_from_matrix
from Compiler.types import Matrix
from Compiler.util import tuplify
from Compiler.library import for_range

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

max_rows = 50
D = sint.Matrix(max_rows, 13)
D.input_from(0)

print_matrix(D)

D.sort((1,))

print_matrix(D)

# # Create key indices tuples
# col_1 = (None,) + tuplify((1,))
# col_2 = (None,) + tuplify((2,))

# # Retrieve vector from original matrix by key indices
# X = D.get_vector_by_indices(*col_1)
# Y = D.get_vector_by_indices(*col_2)

# # Decompose the matrices vectors to list of bits
# x_bits = X.bit_decompose(50)
# y_bits = Y.bit_decompose(50)

# # Create matrix from both bit
# bs = Matrix.create_from([x_bits, y_bits])
# bs[-1][:] = bs[-1][:].bit_not() # Because len(bs) > 1

# @library.for_range(len(bs))
# def _(i):
#     b = bs[i]
#     print_ln("%s", b.get_vector())

# radix_sort_from_matrix(bs, D)