def lcs(x,y):
    res = []
    i = 0
    for item in y:
        if item in x[i:]:
            print('ITEM ', item)
            res.append(item)
            i = x.index(item) + 1
    return ''.join(res)         

RESULT2 = lcs("abaac", "ac")
print(RESULT2)
