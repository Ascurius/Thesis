from typing import Callable, List


def nested_loop_join(
        left: List[List[int]],
        right: List[List[int]], 
        left_key: int, 
        right_key: int,
        condition: Callable[[List[int], List[int]], bool] = lambda left, right: True
    ) -> List[List[int]]:
    result = []
    for l_row in left:
        for r_row in right:
            if (r_row[right_key] == l_row[left_key]) and condition(l_row, r_row):
                result.append(l_row + r_row + [1])
            else:
                result.append(l_row + r_row + [0])
    return result

def preprocess(filename: str, num_rows: int = 50) -> List[List[int]]:
    list_of_lists = []
    with open(filename, 'r') as file:
        for _ in range(num_rows):  
            line = file.readline()  
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

a = preprocess("./MP-SPDZ/Player-Data/Input-P0-0", 10)
b = preprocess("./MP-SPDZ/Player-Data/Input-P1-0", 10)

result = nested_loop_join(a, b, 1, 1)
result.sort(key=lambda row: row[0])

c = 0
for row in result:
    if row[-1] == 1:
        print(row[0])