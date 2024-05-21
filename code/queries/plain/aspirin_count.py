
def preprocess(filename):
    with open(filename, 'r') as file:
        list_of_lists = []
        for line in file:
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

def select_distinct(matrix: list, column: int) -> list:
    result = []
    prev_value = None
    for i in range(len(matrix)):
        if (matrix[i][column] != prev_value) & (matrix[i][-1] == matrix[i][-2] == matrix[i][-3] == matrix[i][13] == 1):
            result.append(matrix[i] + [1])
            prev_value = matrix[i][column]
        else:
            result.append(matrix[i] + [0])
    return result

def nested_loop_join(left, right, left_key, right_key):
    result = []
    for l_row in left:
        for r_row in right:
            if r_row[right_key] == l_row[left_key]:
                result.append(l_row + r_row + [1])
            else:
                result.append(l_row + r_row + [0])
    return result

def where(matrix, key, value):
    for i in range(len(matrix)):
        if matrix[i][key] == value:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix

def where_less_then(matrix, col1, col2):
    for i in range(len(matrix)):
        if matrix[i][col1] <= matrix[i][col2]:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
    return matrix

a = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P0-0")
b = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P1-0")

aw = where(a, 8, 414)
bw = where(b, 4, 0)

j = nested_loop_join(aw, bw, 1, 1)

m = where_less_then(j, 2, len(aw[0])+2)



# print(s)
# m = []
# for row in lt:
#     if row[-1] == row[-2] == row[-3] == row[13] == 1:
#         m.append(row)
        
s = select_distinct(m, 0)
c = 0
for row in s:
    if row[-1] == 1:
        print(row[0])
        c += 1
print("Total count: {}".format(c))