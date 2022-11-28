import os
import math
import random
os.environ['PWNLIB_NOTERM'] = 'True'

from pwn import *


def encode(s):
    return bytes(s, encoding = "utf8")

def check(num):
    x = int(math.sqrt(num) + 3)
    for i in range(2, x+1):
        if (num % i == 0):
            return False
    return True

def run():

    conn = remote("prob01.geekgame.pku.edu.cn", 10001)

    l = conn.recvuntil(encode(": "))

    conn.sendline(encode("312:XXX"))

    conn.recvuntil(encode("> "))
    conn.sendline(encode("急急急"))

    flag = 0

    for i in range(7):
        mesg = conn.recvuntil("> ").decode(encoding = "utf8")
        if ("我有一个朋友" in mesg):
            flag = 1
            conn.sendline(encode(""))
        elif ("访问网址" in mesg):
            conn.sendline(encode("ctf.xn--4gqwbu44czhc7w9a66k.com"))
        elif ("划线内应填什么" in mesg):
            conn.sendline(encode("418645518"))
        elif ("京大学某实验室" in mesg):
            conn.sendline(encode("10.14778/2002974.2002976"))
        elif ("片格式的最早" in mesg):
            conn.sendline(encode("65"))
        elif ("都有唯一的包名" in mesg):
            conn.sendline(encode("cn.edu.pku.pkurunner"))
        elif ("电子游戏概论" in mesg):
            l = mesg.index("通过第 ")
            x = 0
            if (mesg[l+5] == " "):
                x = int(mesg[l+4])
            else:
                x = int(mesg[l+4:l+6])
            x = 300 + int(x ** 1.5) * 100
            conn.sendline(encode(str(x)))
        elif ("我刚刚在脑海中" in mesg):
            l = mesg.index("于")
            x = int(mesg[l+2:l+12])
            l = mesg.index("到")
            y = int(mesg[l+2:l+12])
            sushu = []
            for i in range(x, y+1):
                if (check(i)):
                    sushu.append(i)
            conn.sendline(encode(str(sushu[random.randint(0, len(sushu)-1)])))

    x = conn.recvall().decode(encoding = "utf8")
    conn.close()
    print(x)

run()
