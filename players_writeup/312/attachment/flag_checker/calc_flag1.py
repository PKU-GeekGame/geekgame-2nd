s = "MzkuM8gmZJ6jZJHgnaMuqy4lMKM4"
A = "abcdefghijklm"
B = "nopqrstuvwxyz"
C = A.upper()
D = B.upper()
E = "01234"
F = "56789"

for x in s:
    if x in A or x in C:
        print(chr(ord(x) + 13), end = "")
    elif x in B or x in D:
        print(chr(ord(x) - 13), end = "")
    elif x in E:
        print(chr(ord(x) + 5), end = "")
    else:
        print(chr(ord(x) - 5), end = "")

print("")
