from decimal import *

import numpy as np

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
          131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]


def enc(flag):
    res = []
    p = primes[:len(flag)]
    for i in range(len(flag)):
        res.append(str(sum([Decimal(p[i]).sqrt()*flag[i]
                   for i in range(len(flag))])))
        p = [p[-1]]+p[:-1]
    return res

# Solve the first problem


getcontext().prec = 5
enc1 = list(map(int, ['16404', '16416', '16512', '16515', '16557', '16791', '16844', '16394', '15927', '15942', '15896', '15433', '15469',
                      '15553', '15547', '15507', '15615', '15548', '15557', '15677', '15802', '15770', '15914', '15957', '16049', '16163']))

n = len(enc1)
a = np.zeros((n, n))
b = np.array(enc1)
p = primes[:n]
for i in range(n):
    for j in range(n):
        a[i][j] = Decimal(p[j]).sqrt()
    p = [p[-1]]+p[:-1]
x = np.linalg.solve(a, b)
x = list(map(round, x))
print('Flag 1:', bytes(x))

# Solve the second problem
getcontext().prec = 15
enc2 = list(map(float, ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024',
                        '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']))
n = len(enc2) + 10
a = np.zeros((n, n))
p = primes[:n]
for i in range(n - 10):
    for j in range(n):
        a[i][j] = Decimal(p[j]).sqrt()
    p = [p[-1]]+p[:-1]

a[n - 10][0] = 1
enc2.append(ord('f'))

a[n - 9][1] = 1
enc2.append(ord('l'))

a[n - 8][2] = 1
enc2.append(ord('a'))

a[n - 7][3] = 1
enc2.append(ord('g'))

a[n - 6][4] = 1
enc2.append(ord('{'))

a[n - 5][-1] = 1
enc2.append(ord('}'))

a[n - 4][5] = 1
enc2.append(ord('y'))

a[n - 3][6] = 1
enc2.append(ord('0'))

a[n - 2][7] = 1
enc2.append(ord('u'))

a[n - 1][8] = 1
enc2.append(ord('_'))

b = np.array(enc2)
x = np.linalg.solve(a, b)
x = list(map(round, x))
print('Flag 2:', bytes(x))

# Guess with the following code
#
# for guess in range(60, 127):
#     a[n - 4][5] = 1
#     b = np.array(enc2 + [guess])
#     x = np.linalg.pinv(a).dot(b)
#     x = list(map(round, x))
#     if all([i >= 0 and i < 256 for i in x]):
#         print('Flag 2:', bytes(x))

# Solve the third problem

# Results from Mathematica

x = [102, 108, 97, 103, 123, 119, 104, 97, 116, 95, 97, 95, 49, 101, 110, 115,
     116, 114, 97, 45, 49, 101, 110, 115, 116, 114, 97, 45, 49, 111, 118, 97, 115, 122, 125]

print('Flag 3:', bytes(x))
