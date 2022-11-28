d = []
with open("cryp2.txt", "r") as f:
    for line in f.readlines():
        l = line.strip().split()
        d.append(l[0])

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
temp = [set() for _ in range(26)]

pos = 0
for x in d:
    for y in x:
        if y in letters or y in letters.upper():
            temp[pos].add(y)
            pos = (pos + 1) % 26

print(temp)
ans = {}
for x in letters.lower():
    ret = set(letters)
    for i in range(26):
        if x in temp[i]:
            ret = ret & temp[(i + 1) % 26]
    ans[x] = list(ret)[0]

print(ans)
print("".join(list(map(lambda x: ans[x].upper(), list(letters)))))
