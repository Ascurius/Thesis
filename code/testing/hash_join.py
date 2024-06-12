from collections import defaultdict
from typing import List
from hashlib import sha3_256


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

def hash_join(left, right, left_key, right_key):
    hash_map = defaultdict(list)

    # Hash phase
    for l_row in left:
        secure_hash = sha3_256(str(l_row[left_key]).encode()).hexdigest()
        hash_map[secure_hash].append(l_row)

    # Join phase
    result = []
    for r_row in right:
        secure_hash = sha3_256(str(r_row[right_key]).encode()).hexdigest()
        for l_row in hash_map[secure_hash]:
            result.append(l_row + r_row)
    
    return result

join = hash_join(a, b, 1, 1)
join.sort(key=lambda row: row[0])

for i in join:
    print(i[0])