from pwn import *
import sympy
import random
import time

#context.log_level = 'debug'

# BEGIN BV https://www.zhihu.com/question/381784377/answer/1099438784

bv_table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
bv_tr={}
for i in range(58):
    bv_tr[bv_table[i]]=i
bv_s=[11,10,3,8,4,6]
bv_xor=177451812
bv_add=8728348608

def bv_decode(x: str) -> int:
    assert x.startswith('BV')
    r=0
    for i in range(6):
        r+=bv_tr[x[bv_s[i]]]*58**i
    return (r-bv_add)^bv_xor

# END BV

TOKEN = 'vivo50'

def find_prime(lo, hi):
    li = [x for x in range(lo, hi+1) if sympy.isprime(x)]
    print('!! prime', len(li))
    return random.choice(li)

def main():
    r = remote('127.0.0.1', 10001)
    r.recvuntil(b'token: ')
    r.sendline(TOKEN.encode())

    r.recvuntil(b'> ')
    r.sendline('急急急'.encode('utf-8'))

    for _ in range(7):
        q = r.recvuntil(b'> ').decode('utf-8')
        if '向该主机发送的' in q:
            a = 'ctf.xn--4gqwbu44czhc7w9a66k.com'
        elif '最早描述该软件的论文' in q:
            a = '10.14778/2002974.2002976'
        elif '《电子游戏概论》中，通过第' in q:
            level = q.partition('《电子游戏概论》中，通过第')[2].partition('级关卡')[0].strip()
            a = str((lambda level: 300+int(level**1.5)*100)(int(level)))
        elif '图片格式的最早' in q:
            a = '65'
        elif '软件都有唯一的包名' in q:
            a = 'cn.edu.pku.pkurunner'
        elif '我有一个朋友在美国' in q:
            a = '80304'
        elif '下划线内应填什么数字' in q:
            bvid = q.partition('bilibili.com/video/')[2].partition('也可以通过')[0].strip()
            assert bvid.startswith('BV')
            a = str(bv_decode(bvid))
        elif '我刚刚在脑海中想了一个介于' in q:
            prange = q.partition('我刚刚在脑海中想了一个介于')[2]
            plower = prange.partition('到')[0].strip()
            pupper = prange.partition('到')[2].partition('之间')[0].strip()
            a = str(find_prime(int(plower), int(pupper)))
        else:
            print('!!', q)
            return False
            
        r.sendline(a.encode())
        
    d = r.stream().decode('utf-8')
    r.close()
    return '你共获得了 100 分' in d
    
while not main():
    time.sleep(10)
