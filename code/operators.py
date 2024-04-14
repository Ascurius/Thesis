from Compiler.types import sint
from Compiler.library import for_range_opt, if_


########################
#### Secure operators
########################

def inner_join_nested_loop(left, right, key=0):
    """
    The key=0 represents the zeroth column which usualy is the id.
    """
    result = sint.Matrix(
        rows=left.shape[0], 
        columns=left.shape[1] + right.shape[1] - 1
    )
    @for_range_opt(left.shape[0])
    def _(left_row):
        @for_range_opt(right.shape[0])
        def _(right_row):
            evaluate = left[left_row][key].equal(right[right_row][key])
            @if_(evaluate.reveal())
            def _():
                @for_range_opt(left.shape[1])
                def _(left_column):
                    result[left_row][left_column] = left[left_row][left_column]
                @for_range_opt(right.shape[1] - 1)
                def _(right_column):
                    result[left_row][left.shape[1] + right_column] = right[left_row][right_column + 1]
    return result

def order_by(table, key):
    table.sort((key,))

def groub_by(array):
    result = MultiArray([arr_test.length, 2], sint)
    count = sint(1)
    current_element = sint(0)
    @for_range_opt(array.length)
    def _(i):
        dbit = (array[i] != current_element).if_else(1,0).reveal()
        @if_e(dbit)
        def _():
            @if_((current_element != sint(0)).if_else(1,0).reveal())
            def _():
                result[i][0] = current_element
                result[i][1] = count
            current_element.update(array[i])
            count.update(sint(1))
        @else_
        def _():
            count.update(count + sint(1))
    @if_((current_element != sint(0)).if_else(1,0).reveal())
    def _():
        result[-1][0] = current_element
        result[-1][1] = count
    return result

########################
#### Plaintext operators
########################

def group_by(arr):
    result = []
    count = 1
    current_element = None
    for i in range(len(arr)):
        if arr[i] != current_element:
            if current_element is not None:
                result.append([current_element, count])
            current_element = arr[i]
            count = 1
        else:
            count += 1
    if current_element is not None:
        result.append([current_element, count])
    return result