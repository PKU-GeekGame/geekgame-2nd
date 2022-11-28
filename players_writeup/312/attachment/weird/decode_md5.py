import hashlib

md5 = hashlib.md5()

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = "0123456789"

with open("plain2.txt", "r") as f:
    cnt = 0
    for x in f.readlines():
        cnt += 1
        flag = False
        for i in range(0, 127):
            md5 = hashlib.md5()
            md5.update(chr(i).encode("utf-8"))
            res = md5.hexdigest()
            if res == x.strip():
                flag = True
                print(chr(i), end = "")
                break
        if not flag:
            for i in range(0, 127):
                for j in range(0, 127):
                    md5 = hashlib.md5()
                    md5.update((chr(i)+chr(j)).encode("utf-8"))
                    res = md5.hexdigest()
                    if res == x.strip():
                        flag = True
                        print(chr(i) + chr(j), end = "")

print("")
