target = 39


def dfs(now, i):
    for cur in range(16):
        nxt = (now << 4) + cur
        if nxt % i == 0:
            if i == target:
                if nxt > 0:
                    return nxt
            else:
                possible = dfs(nxt, i+1)
                if possible != -1:
                    return possible

    return -1


ans = dfs(0, 1)
print(ans)

ans ^= 2511413510823273577350468206724207602459660000906919269554
print(ans)

bytes = ans.to_bytes((ans.bit_length() + 7) // 8, 'big')
print(bytes)
