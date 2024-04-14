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

def odd_even_merge(half_array):
    if half_array.length > 2:
        odd_even_merge(half_array[:-1])
        odd_even_merge(half_array)
        @for_range_opt(1, half_array.length - 2)
        def _(i):
            b = (half_array[i] < half_array[i+1]).less_than(half_array[i], half_array[i+1])
            @if_(b.reveal())
            def _():
                half_array[i], half_array[i+1] = half_array[i+1], half_array[1]
    else:
        b = (half_array[0] < half_array[1]).less_than(half_array[0], half_array[1])
        @if_(b.reveal())
        def _():
            half_array[0], half_array[1] = half_array[1], half_array[0]

def odd_even_merge_sort(array):
    if array.length > 1:
        odd_even_merge_sort(array[:int(array.length / 2)])
        odd_even_merge_sort(array[int(array.length / 2):])
        odd_even_merge(array)

def print_matrix(matrix):
    for i in range(matrix.shape[0]):
        print_ln("%s", matrix[i].reveal())

def get_shape(arr):
    if isinstance(arr, list):
        return [len(arr)] + get_shape(arr[0])
    else:
        return []