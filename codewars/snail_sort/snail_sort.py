def snail(snail_map):
    expected = []
    while snail_map:

        expected.extend(snail_map.pop(0))
        
        if snail_map:
            for row in snail_map:
                expected.append(row.pop())

        if snail_map:
            expected.extend(reversed(snail_map.pop(-1)))

        if snail_map:
            for row in reversed(snail_map):
                expected.append(row.pop(0))


    return expected



array = [[1,2,3],
         [4,5,6],
         [7,8,9]]

expected = [1,2,3,6,9,8,7,4,5]

res = snail(array)

print(f'Ex: {expected}')
print(f'Rs: {res}')
