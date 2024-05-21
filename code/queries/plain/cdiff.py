
def preprocess(filename):
    with open(filename, 'r') as file:
        list_of_lists = []
        for line in file:
            elements = list(map(int, line.split()))
            list_of_lists.append(elements)
    return list_of_lists

