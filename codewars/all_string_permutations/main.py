def permutations(s):

    res = []

    for let in range(len(s)):
        new_s = [ s[i] for i in range(len(s)) if i != let ]
        res.append(s[let] + ''.join(new_s))

    print(res)

s = 'aabb'

print(['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa'])
permutations(s)


# Your function should return ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']