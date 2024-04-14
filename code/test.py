# a = sint(1)
# b = sint(2)

# dbit = (a != b).if_else(1,0)
# @if_(dbit)
# def _():
#     print_ln("Not equal")

dummy_data = [20, 99, 20, 20, 10, 11, 12, 12, 23, 24, 10, 11]
arr_test = sint.Array(len(dummy_data))
arr_test.assign(dummy_data)
arr_test.sort()


space = sint.Array(20)
unique_values = sint.Array(None, address=space.address)
counts = sint.Array(None, address=space.address)


@for_range(10)
def _(i):
    unique_values[i] = 1
    counts[i] = 1
# s = MultiArray([arr_test.length, 2], sint)
# s.assign_all(0)
print_ln("%s", unique_values.reveal_list())