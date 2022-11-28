import numpy as np

from decimal import *

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

res = list(map(int, ['16404', '16416', '16512', '16515', '16557', '16791', '16844', '16394', '15927', '15942', '15896', '15433', '15469', '15553', '15547', '15507', '15615', '15548', '15557', '15677', '15802', '15770', '15914', '15957', '16049', '16163']))
# print(res)
l = len(res)

def main() -> None:
    getcontext().prec=5
    p = primes[:len(res)]
    pp = [float(Decimal(x).sqrt()) for x in p]
    a = np.zeros((l, l))
    for i in range(l):
        for j in range(l):
            a[i, j] = pp[(j - i + l) % l]
    x, residuals, rank, s = np.linalg.lstsq(a, res)
    print(x, residuals, rank, s)
    print(''.join(chr(round(i)) for i in x))
    # flag{g00d_1inear_equation}


if __name__ == "__main__":
    main()
