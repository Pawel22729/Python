def solution(array_a, array_b):
    zip_list = [ abs(array_a[i] - array_b[i])**2 for i in range(len(array_a)) ]
    res = sum(zip_list) / len(zip_list)
    return int(res) if res % 1 == 0 else res
