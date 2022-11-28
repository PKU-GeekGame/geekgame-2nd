import numpy as np

from decimal import *

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

res = list(map(float, ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024', '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']))
print(len(res))
l = len(res) + 10

def main() -> None:
    getcontext().prec=15
    p = primes[:l]
    pp = [float(Decimal(x).sqrt()) for x in p]
    # print(np.zeros((2, 3)))
    # exit()
    # TODO: Use the knowledge that flag is of format flag{...}
    a = np.zeros((l - 10, l - 10))
    for i in range(l - 10):
        for j in range(l):
            if j < 9:
                res[i] -= ord('flag{y0u_'[j]) * pp[(j - i + l) % l]
            elif j < l - 1:
                a[i, j - 9] = pp[(j - i + l) % l]
            else:
                res[i] -= ord('}'[j - (l - 1)]) * pp[(j - i + l) % l]

    x, residuals, rank, s = np.linalg.lstsq(a, res)
    print(len(x))
    print(x, residuals, rank, s)
    print(''.join(chr(round(i) - 1) for i in x))
    print(''.join(chr(round(i)) for i in x))
    print(''.join(chr(round(i) + 1) for i in x))
    # ek`f{w.t]_qd]_^eoTW[bimry|
    # The last two are 128.61170046 133.99011013
    #      x0u^ard^`_goho]bjaoxst
    # w/t]`qc]_^fngn\ai`nwrs
    # x0u^ard^`_goho]bjaoxst
    # y1v_bse_a`hpip^ckbpytu
    # y0u
    # flag{y0u_are_a_good_guesser}


if __name__ == "__main__":
    main()
