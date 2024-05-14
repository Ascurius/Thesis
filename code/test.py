from circuit import sha3_256

max_rows = 10
a = sint.Matrix(max_rows, 13)
a.input_from(0)

for i in range(a.shape[0]):
    print_ln("%s", sha3_256(a[i]).reveal())