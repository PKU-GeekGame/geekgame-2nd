import pwn
import random
import sympy
import re

r = pwn.remote('prob01.geekgame.pku.edu.cn', 10001)
r.recvuntil("Please input your token:".encode())
r.sendline("93:XXX".encode())
print(r.recvuntil('开始答题。\n>'.encode('utf-8')).decode('utf-8'))
r.sendline('急急急'.encode('utf-8'))
r.recvuntil('计时开始。\n'.encode('utf-8'))

for i in range(7):
    prob = r.recvuntil('>'.encode()).decode()
    print(prob)
    if 'WebP' in prob:
        r.sendline("65".encode())
    elif 'Host 请求头' in prob:
        r.sendline("ctf.xn--4gqwbu44czhc7w9a66k.com".encode())
    elif '软件的包名' in prob:
        r.sendline("cn.edu.pku.pkurunner".encode())
    elif '《电子游戏概论》' in prob:
        level = int(re.findall(r'通过第 (\d+) 级', prob)[0])
        r.sendline(str(300+int(level**1.5)*100).encode())
    elif 'gStore' in prob:
        r.sendline("10.14778/2002974.2002976".encode())
    elif 'bilibili' in prob:
        r.sendline("418645518".encode())
    elif '猜猜它是多少' in prob:
        p1, p2 = re.findall(r'\d+', prob[6:])
        p1 = int(p1)
        p2 = int(p2)
        p_mid = []
        while sympy.nextprime(p1) < p2:
            p1=sympy.nextprime(p1)
            p_mid.append(p1)
        print(random.sample(p_mid,1)[0])
        r.sendline(str(random.sample(p_mid,1)[0]).encode())
    elif 'MAC 地址' in prob:
        print("遇到MAC了")
        exit(0)
    else:
        print("未知情况")
        exit(0)
    respon = r.recvline().decode('utf-8')
    print(respon)
    if '不' in respon:
        exit(0)

while 1:
    try:
        print(r.recv().decode())
    except EOFError:
        break
