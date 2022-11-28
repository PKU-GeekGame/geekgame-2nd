import numpy as np
import math
from decimal import *

magic_l = 28

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

p = list(map(math.sqrt, primes[:magic_l]))

result = ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024', '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']

l = ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024', '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']

l = list(map(float, l))
l = l + [ord('f'), ord('l'), ord('a'), ord('g'), ord('{'), ord('}'), ord('_'), ord('_'), ord('a'), ord('e')]

def enc(flag):
    res=[]
    p=primes[:len(flag)]
    for i in range(len(flag)):
        res.append(str(sum([Decimal(p[i]).sqrt()*flag[i] for i in range(len(flag))])))
        p=[p[-1]]+p[:-1]
    return res

B = np.matrix(l).T

A = np.zeros((28, 28), np.float64)
for i in range(18):
    for j in range(28):
        A[i][j] = p[j]
    p = [p[-1]] + p[:-1]
A[18][0] = 1
A[19][1] = 1
A[20][2] = 1
A[21][3] = 1
A[22][4] = 1
A[23][-1] = 1

letters = "abcdefghijklmnopqrstuvwxyz"

for i in range(5, 27):
    A[24][i] = 1
    for j in range(i+2, 27):
        A[25][j] = 1
        for k in range(5, 27):
            if k != i and k != j:
                A[26][k] = 1
                for x in range(5, 27):
                    if x != k and x != i and x != j:
                        A[27][x] = 1
                        #assert(np.linalg.det(A) != 0)
                        ans = np.linalg.inv(A).dot(B)
                        ans = np.round(ans).reshape(-1).tolist()[0]
                        ans = list(map(int, ans))
                        flag = True
                        for t in ans:
                            if t < 0 or t >= 127:
                                flag = False
                                break
                        if not flag:
                            A[27][x] = 0
                            continue
                        print("".join(list(map(chr,ans))))
                        # if enc(ans)[:-10] == result:
                        #     print(ans)
                        #     exit(0)
                A[26][k] = 0
        A[25][j] = 0
    A[24][i] = 0

# l = np.round(x).reshape(-1)[0].tolist()[0]
# print(l)

# with open("flag2.txt", "wb") as f:
#     for x in l:
#         f.write(int(x).to_bytes(1, "little"))
