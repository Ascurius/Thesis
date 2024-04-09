from Compiler.types import sint
from Compiler.library import for_range_opt, if_

def inner_join(left, right, key=0):
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