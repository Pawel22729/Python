#!/usr/bin/env python3

def solution(N, S) -> int:
    row_full = ["A","B","C","D","E","F","G","H","J","K"]
    rows_all = []

    for i in range(1, N + 1):
        rows_all.append([
            str(i) + r for r in row_full
        ])

    reserved = S.split()

    for row in rows_all:
        for seat in row:
            if seat in reserved or ("A" or "K") in seat:
                row.pop(
                    row.index(seat)
                )
        for seat in row:
            row[row.index(seat)] = seat[-1]

    four_siters = 0
    full_slice = ''.join(row_full)
    for row in rows_all:
        if len(row) > 4:
            sit_pointer = 0
            while sit_pointer + 4 <= len(row):
                search_slice = ''.join(row[sit_pointer:sit_pointer+4])
                if search_slice in full_slice:
                    four_siters += 1
                    sit_pointer += 4
                else:    
                    sit_pointer += 1
    return four_siters

N = 22
S = "1A 3C 2B 20G 5A"

RESULT = solution(N, S)
print(RESULT)