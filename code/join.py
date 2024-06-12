from collections import defaultdict
from circuit import sha3_256

def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def hash_join_mpc(left, right, l_key, r_key):
    result = sint.Matrix(
        rows=left.shape[0] * right.shape[0],
        columns=left.shape[1] + right.shape[1]
    )
    result.assign_all(0)

    hash_map = defaultdict(list)
    @for_range_opt(left.shape[0])
    def _(i):
        secure_hash = left[i][l_key].reveal()
        # print_ln("%s", secure_hash)
        hash_map[secure_hash].append(left[i])
    
    @for_range_opt(right.shape[0])
    def _(i):
        secure_hash = right[i][r_key].reveal()
        values = hash_map[secure_hash]
        print_ln("%s", len(values))
        print_ln("%s", secure_hash)
        for l_row in range(len(values)):
            # result[i].assign(right[i] + right[i])
            # result[i].assign_part_vector(values[l_row], base=len(right[i]))
            result[i].assign_part_vector(values[l_row])
    return result


a = sint.Matrix(10, 13)
a.input_from(0)
b = sint.Matrix(10, 13)
b.input_from(1)

matrix = hash_join_mpc(a, b, 1, 1)