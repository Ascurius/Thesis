from Compiler.library import print_ln, print_ln_if

def string_to_array(string):
    """
    Wandelt einen String in ein Array von Zahlen um, wobei jede Zahl dem Unicode-Wert des entsprechenden Zeichens entspricht.
    """
    return [ord(char) for char in string]

def find_substring(string, substring):
    """
    Sucht nach einem Substring in einem Array von Zahlen, das aus dem gegebenen String erstellt wurde.
    """
    string_array = string_to_array(string)
    substring_array = string_to_array(substring)
    
    for i in range(len(string_array) - len(substring_array) + 1):
        if string_array[i:i+len(substring_array)] == substring_array:
            return i
    
    return -1  # Substring nicht gefunden

def get_matrix_dimensions(filename):
    num_rows = 0
    num_cols = None

    with open(filename, 'r') as file:
        for line in file:
            # Increment row count for each line
            num_rows += 1

            # Split the line into integers
            row_data = line.strip().split()

            # Check if the number of columns is consistent
            if num_cols is None:
                num_cols = len(row_data)
            elif num_cols != len(row_data):
                raise ValueError("Inconsistent number of columns in the matrix")

    return num_rows, num_cols

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def print_matches(matrix, match_key):
    for i in range(matrix.shape[0]):
        print_ln_if(matrix[i][match_key].reveal(), "%s", matrix[i].reveal())

def get_shape(arr):
    if isinstance(arr, list):
        return [len(arr)] + get_shape(arr[0])
    else:
        return []

def refill_matrix(target, source):
    assert target.shape[0] >= source.shape[0]
    for i in range(source.shape[0]):
        target[i].assign_vector(source[i])

def select_relevant(matrix: sint.Matrix, match_key: int) -> sint.Matrix:
    count = regint(0)
    vec = matrix.get_column(match_key)
    for i in range(len(vec.elements())):
        @if_(vec.elements()[i].reveal())
        def _():
            count.update(count+1)
    result = sint.Matrix(
        rows=count,
        columns=matrix.shape[1]
    )
    result_row = regint(0)
    for i in range(matrix.shape[0]):
        dbit = (matrix[i][match_key] == 1).if_else(1,0)
        @if_(dbit)
        def _():
            result[result_row] = matrix[i]
            result_row.update(result_row+1)
    return result
