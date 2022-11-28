import re
import time

from binascii import *
from random import randint
from pwn import *


def is_prime(x):
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def find_prime(l, r):
    return [i for i in range(l, r + 1) if is_prime(i)]


def recvuntil(r, until):
    b = r.recvuntil(until)
    line = str(b, 'utf-8')
    return line


def recvline(): return recvuntil(b'\n')


while True:
    r = remote('prob01.geekgame.pku.edu.cn', 10001)
    recvuntil(r, b'token: ')

    r.send(b'36:XXX\n')
    recvuntil(r, b'> ')

    r.send(u'急急急\n')

    for _ in range(7):
        question = recvuntil(r, '> ')
        if 'gStore' in question:
            r.send(b'10.14778/2002974.2002976\n')
        elif 'bilibili' in question:
            r.send(b'418645518\n')
        elif '电子游戏概论' in question:
            idx = question.index('通过第')
            print(question[idx+4:idx+6])
            level = int(question[idx+4:idx+6])
            target = 300+int(level**1.5)*100
            r.send(str(target).encode('utf-8')+b'\n')
        elif 'WebP' in question:
            r.send(b'65\n')
        elif 'PKU Runner' in question:
            r.send(b'cn.edu.pku.pkurunner\n')
        elif '脑海' in question:
            nums = re.findall('\d+', question)
            lo = int(nums[1])
            hi = int(nums[2])
            primes = find_prime(lo, hi)
            prime = primes[randint(0, len(primes)-1)]
            r.send(str(prime).encode('utf-8')+b'\n')
        elif '世界一流大学' in question:
            r.send(u'ctf.xn--4gqwbu44czhc7w9a66k.com\n')
        elif 'MAC' in question:
            r.send(b'12345\n')
        else:
            r.send(b'12345\n')

    ending = recvuntil(r, '欢迎再来！')
    if 'flag' in ending:
        print(ending)

    r.close()
    if '获得了 100 分' in ending:
        break

    time.sleep(10)
