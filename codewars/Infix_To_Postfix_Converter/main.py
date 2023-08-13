def to_postfix (infix):
    operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    output = []

    for character in infix:
        if character.isnumeric():
            output.append(character)
        elif character not in operators and character not in ["(", ")"]:
            output.append(character)
        elif character == "(":
            stack.append(character)
        elif character == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and (operators.get(character, 0) <= operators.get(stack[-1], 0) if character != "^" else False):
                output.append(stack.pop())
            stack.append(character)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


print("TEST1:\nmn*pq-+r+", " : ", to_postfix("m*n+(p-q)+r"))
print("TEST2:\n33*71+/", " : ", to_postfix("3*3/(7+1)"))
print("TEST3:\n123^^", " : ", to_postfix("1^2^3"))