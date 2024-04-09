import random
from datetime import datetime

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

def random_date(min_year, max_year):
    # Generate a random year between min_year and max_year
    year = random.randint(min_year, max_year)
    
    # Generate a random month and day
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):  # Leap year
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    
    # Create a datetime object for the generated date
    date_object = datetime(year, month, day)
    
    # Convert the datetime object to a timestamp
    timestamp = date_object.timestamp()
    
    return timestamp

def generate_player_input(rows):
    with open("/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P0-0", "w") as file:
        for i in range(1, rows + 1):
            x = random.uniform(0, 1000)
            year = random.randint(1900, 2100),
            timestamp = random_date(year[0], 2100)
            data = [
                i,
                random.randint(1, 10),
                year[0],
                random.randint(1, 10),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                round(x, 2),
                random.randint(0, 1),
                timestamp,
                round(x, 2),
                int(x)
            ]
            file.write(" ".join(map(str, data)) + "\n")

generate_player_input(100)