# 方程组

## 解题过程
数学题直接摆烂。Flag1 直接 numpy 求解，处理一下误差。

~~~python
from decimal import *
import numpy as np

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
          131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
result = ['16404', '16416', '16512', '16515', '16557', '16791', '16844', '16394', '15927', '15942', '15896', '15433', '15469',
          '15553', '15547', '15507', '15615', '15548', '15557', '15677', '15802', '15770', '15914', '15957', '16049', '16163']

matrix = []
primes = primes[:len(result)]
for i in range(len(result)):
    matrix.append([p ** 0.5 for p in primes])
    primes = [primes[-1]]+primes[:-1]
t = np.array(matrix)
t.astype(np.float64)
t = np.linalg.solve(t, np.array([int(n) for n in result]))
for n in t:
    print(int(n + 0.5).to_bytes(length=1, byteorder='little').decode(), end='')
~~~