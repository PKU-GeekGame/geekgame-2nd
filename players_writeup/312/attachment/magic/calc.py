def calc(x):
    ret = []
    while x > 0:
        ret = [x%256] + ret
        x //= 256
    return ret

l = calc(2511413510804014444327808527271906959503584409677526946111)
ans = [0x66, 0x6c, 0x61, 0x67, ord('{')]
print(l)
l = l[4:]
l[0] = l[0] ^ ord('{')
x = l[0]
l = l[1:]
j = 2

def dfs(x, i, j):
    if i == len(l):
        return True
    x = (x << 8) + l[i]
    for res in range(0, 127):
        y = x ^ res
        if (y >> 4) % j == 0 and y % (j+1) == 0:
            ans.append(res)
            if (dfs(x ^ res, i+1, j+2)):
                return True
            ans.pop()
    return False

print(dfs(x, 0, j))

print("".join(list(map(chr,ans))))
