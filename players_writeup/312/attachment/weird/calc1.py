d = []

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
with open("cryp1.txt", "r") as f:
    for line in f.readlines():
        l = line.strip().split()
        d.append(l)

cycle = 22
pos = 0
sigma = {}

for x in d:
    for y in x:
        if len(y) == 1 and y in letters.lower():
            sigma[pos % cycle] = ord(y)-ord("a")
        for z in y:
            if z in letters or z in letters.lower():
                pos += 1

ans = ["0" for _ in range(26)]
print(len(sigma))
sigma = dict(sorted(list(sigma.items())))
print(len(sigma))
sigma[6] = ord('r') - ord('a')
sigma[15] = ord('m') - ord('a')
for x, y in sigma.items():
    print(x, chr(y + ord('a')))
print(sorted(sigma.values()))
for i in range(cycle-1):
    if i in sigma and i+1 in sigma:
        if (sigma[i] == 8):
            print(sigma[i+1])
            print(chr(sigma[i+1] + ord("a")).upper())
        ans[sigma[i]] = chr(sigma[i+1] + ord("a")).upper()
    else:
        print(i, i+1)

if 0 in sigma and cycle-1 in sigma:
    ans[sigma[cycle-1]] = chr(sigma[0] + ord("a")).upper()
else:
    print(0, cycle - 1)

print("".join(ans))

print(ans)
for i in range(len(ans)):
    print("{} -> {}".format(chr(i + ord("A")), ans[i]))

# ans = "YNKIFJDAWLQPVTZCHMEGRUXOBS"
# print(ans)
# for i in range(len(ans)):
#     print("{} -> {}".format(chr(i + ord("A")), ans[i]))
# x = ans[0]
# pos = 1
# while x != "A":
#     if pos in sigma:
#         print(pos, x)
#         assert(sigma[pos] == ord(x) - ord("A"))
#     pos += 1
#     x = ans[ord(x) - ord("A")]
"""
YNKDFMRAWUQPLTZCHIEGJVXOBS
flag{fre9uency_4naly5is_1s_useful}
"""
