import os
from decimal import *
primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
def enc(flag):
    res=[]
    p=primes[:len(flag)]
    for i in range(len(flag)):
        res.append(str(sum([Decimal(p[i]).sqrt()*flag[i] for i in range(len(flag))])))
        p=[p[-1]]+p[:-1]
    return res

if __name__=='__main__':
    getcontext().prec=5
    print(enc(open("flag1.txt","rb").read().strip()))
    getcontext().prec=15
    print(enc(open("flag2.txt","rb").read().strip())[:-10])
    getcontext().prec=200
    print(enc(open("flag3.txt","rb").read().strip())[0])