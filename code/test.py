from circuit import sha3_256

def print_matrix(matrix: sint.Matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def hash_join(left, right, left_key, right_key):
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
            new_row[:result.shape[1] // 2] = left[left_row]
            new_row[result.shape[1] // 2:] = right[right_row]
            result[current_idx].assign(new_row)
            current_idx.update(current_idx + regint(1))

    hash_map = {}
    @for_range_opt(left.shape[0])
    def _(l_row):
        key = sha3_256(left[l_row][left_key])
        hash_map[key] = l_row

    @for_range_opt(right.shape[0])
    def _(r_row):
        @for_range_opt(len(hash_map))
        def _(hash):
            key = hash_map.keys()[hash]
            result[r_row][-1] = (key == sha3_256(right[r_row][right_key]) ).if_else(sint(1), sint(0))

def concat_tables(left, right):
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
            new_row[:result.shape[1] // 2] = left[left_row]
            new_row[result.shape[1] // 2:] = right[right_row]
            result[current_idx].assign(new_row)
            current_idx.update(current_idx + regint(1))
    return result
    

max_rows = 50
a = sint.Matrix(max_rows, 13)
a.input_from(0)
b = sint.Matrix(max_rows, 13)
b.input_from(1)
# hash_join(a, b, 1, 1)
c = concat_tables(a, b)
print_matrix(c)