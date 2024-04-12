dummy_data = [20, 99, 20, 20, 10, 11, 12, 12, 23, 24, 10, 11]
arr_test = sint.Array(len(dummy_data))
arr_test.assign(dummy_data)

def group_by(arr):
    result = []
    count = 1
    for i in range(len(arr)):
        if arr[i] == arr[i+1]:
            count += 1
        else:
            result.append([arr[i-1], count])