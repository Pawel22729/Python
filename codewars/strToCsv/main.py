

def repsent(mat: list) -> str:
    return '\n'.join([ ','.join(map(str, i)) for i in mat ])

if __name__ == "__main__":
    
    mat = [[0, 1, 2, 3, 4],
          [10, 11, 12, 13, 14],
          [20, 21, 22, 23, 24],
          [30, 31, 32, 33, 34]]
    
    res = repsent(mat)

    print(res)