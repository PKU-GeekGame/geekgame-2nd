from pwn import *
import gmpy2

def bili():
    p.sendline(b"418645518")

def isprime(prime):
    pr = gmpy2.next_prime(prime)
    p.sendline(bytes(str(pr), encoding="utf-8"))

def android():
    p.sendline(b"cn.edu.pku.pkurunner")

def webp():
    p.sendline(b"65")

def android():
    p.sendline(b"cn.edu.pku.pkurunner")

def doi():
    p.sendline(b"10.14778/2002974.2002976")

def ctf():
    p.sendline(b"ctf.xn--4gqwbu44czhc7w9a66k.com")

def mac():
    p.sendline(b"80304")

def ele(level):
    p.sendline(bytes(str(300+int(level**1.5)*100), encoding="utf-8"))

def solve():
    r = p.recv()
    print(r.decode())
    if bytes("错误", encoding="utf-8") in r:
        return
    elif b'flag' in r:
        exit()
    elif b'av' in r:
        bili()
    elif b'Android' in r:
        android()
    elif b'WebP' in r:
        webp()
    elif bytes("质数", encoding="utf-8") in r:
        isprime(int(r.decode().split(' ')[3]))
    elif b'DOI' in r:
        doi()
    elif b'ctf' in r:
        ctf()
    elif b'MAC' in r:
        mac()
    elif bytes("电子游戏概论", encoding="utf-8") in r:
        ele(int(r.decode().split(' ')[6]))
    solve()

p = remote("prob01.geekgame.pku.edu.cn", 10001)
token = ""
p.recv()
p.sendline(bytes(token, encoding="utf-8"))
p.recv()
p.sendline(bytes("急急急", encoding="utf-8"))
solve()
p.interactive()