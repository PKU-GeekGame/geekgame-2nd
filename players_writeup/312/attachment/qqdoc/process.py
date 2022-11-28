import json

ans = dict()
with open("data.in", "r") as f:
    s = "{" + f.readline().strip() + "}"
    ans = json.loads(s)

l = list(ans.keys())

pos = 22
res = 0
for x in l:
    while (pos < int(x)):
        pos += 1
        print(" ", end = "")
        res += 1
        if (res == 11):
            print("")
            res = 0
    print("@", end = "")
    pos += 1
    res += 1
    if (res == 11):
        print("")
        res = 0
# flag{WeAreNotSponsoredByTencent}
