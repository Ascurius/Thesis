a = sint.Matrix(4, 5)
a.input_from(0)
vec = a.get_column(5)
# vec.elements()[0]
print_ln("%s", len(vec.elements()))

# for i in range(a.shape[0]):
#     print_ln("%s", a[i].reveal())