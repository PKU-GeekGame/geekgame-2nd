# TTOWRSS

## 解题过程
首先尝试和程序交互，弹出 "PASSWORD: "，随便输入后得到 "Invalid password!"。大概能确定是个编码的逆向题，于是就逆呗。但扔进 IDA 之后除了一个 signal handler 基本看不出任何函数，也找不到输出字符串的地方在哪。推测可能是有混淆，于是打算先用 gdb 试试。

但调试之后发现不对，每次 `c` 就只走一个指令。发现是程序收到了 SIGTRAP。然后逆了下程序还能看的部分：

1. 注册了 SIGTRAP 的处理函数，根据内存中的数据和当前的 RIP，计算新的 RIP。

2. 注册完之后，修改了 FLAGS Registers，将 TF 标志位置为 1。

这使得程序每执行完一个命令后，由 signal handler 根据 RIP 值，决定实际要执行的指令的 RIP 值。于是写了个脚本，计算 signal handler 进行的映射。之后尝试在 gdb 中，根据当前 RIP 和映射关系，强行跳转到对应的执行，尝试恢复控制流，但脚本好像有点问题，也可能是原理不对，程序会陷入死循环，，，其中导出映射关系的脚本如下，gdb 脚本没跑通就删掉了。

~~~python
import json

from pwn import *

start_addr = 0x1098
end_addr = 0x1445

def bittest(a, b):
    return a & (1 << b)

def jmp(addr, bytes_array):
    v5 = addr - 1
    v6 = 0
    v7 = addr + ~start_addr
    while v6 != 2:
        v8 = v7
        v9 = v7
        v7 = v7 - 1
        if ((bytes_array[v8 >> 3]) >> (v9 & 7)) & 1:
            v6 = v6 + 1
        addr = v5
        v5 = v5 - 1
    return addr


if __name__ == '__main__':
    with open('prob22-crackme', 'rb') as f:
        binary = f.read()
    bytes_array = binary[0x30e0:][:118]

    jumps = dict()
    first = True
    for i in range(start_addr, end_addr):
        diff = i - start_addr
        lookup = bytes_array[diff >> 3]
        if bittest(lookup, diff & 7):
            jumps[i] = jmp(i, bytes_array)
    l = list(jumps.keys())
    with open('jumps.json', 'w') as f:
        json.dump(jumps, f)
~~~

根据计算出的映射关系，可以确定程序是从高地址向地址执行的。以下是一小段映射关系：

~~~json
{
    "13c1": "13b9",
    "13c4": "13bb",
    "13c5": "13c1"
}
~~~

RIP 为 13c5 时，执行 13c1，然后 RIP 变为 13c4，执行 13bb，然后 RIP 变成 13c1...


之后去 Google 了 "How to debug program captures SIGTRAP."，找到如下信息：

> If you simply continue from GDB, the signal will be "swallowed", which is not what you want.
> 
> You can ask GDB to continue the program and send it a signal with signal SIGTRAP.

写了下面的脚本记录函数执行路径。

~~~python
trace = []
while True:
    line = []
    try:
        at_trap = gdb.execute('x /i $rip', to_string=True)
        at_trap = at_trap[3:at_trap.find(':')]
        gdb.execute('signal SIGTRAP')
        after_trap = gdb.execute('x /i $rip', to_string=True)
        trace.append(f'{at_trap} -> {after_trap}')
    except:
        with open('trace.txt', 'w') as f:
            for line in trace:
                f.write(line + '\n')
        break
~~~

去掉 0x7fff 开头的行，最后也就几百行。而且能够确定代码范围不大，就手工逆了，需要注意的是记录到的 `after_trap` 是指令执行完的后一条指令。手工逆向后得到如下结果：

~~~
0x555555555080 <__isoc99_scanf@plt> -> 0x7ffff7a5de70 <__isoc99_scanf>
0x55555555518e -> 0x555555555189 // 186   mov     rdi, rbp
0x555555555189 -> 0x5555555553c5 // 181   call    sub_13C5
0x5555555553c5 -> 0x5555555553c4 // 3c1   movsx   eax, byte ptr [rdi]
0x5555555553c4 -> 0x5555555553c1 // 3bb   mov     edx, cs:dword_4020 // 13h
0x5555555553c1 -> 0x5555555553bb // 3b9   test    al, al
0x5555555553bb -> 0x5555555553b9 // 3b6   setz    cl
0x5555555553b9 -> 0x5555555553b6 // 3b3   shr     edx, 1Fh
0x5555555553b6 -> 0x5555555553b3 // 3b1   cmp     cl, dl
0x5555555553b3 -> 0x5555555553b1 // 3af   jnz     short loc_1354
0x5555555553b1 -> 0x5555555553af // 3ad   xor     ecx, ecx
0x5555555553af -> 0x5555555553ad // 3a6   lea     r8, dword_4020
0x5555555553ad -> 0x5555555553a6 // 39f   lea     r10, unk_2040
0x5555555553a6 -> 0x55555555539f // 398   lea     r9, unk_20A0 
0x55555555539f -> 0x55555555535f // 396   jmp     short loc_135F
0x55555555535f -> 0x55555555535d // 35b   test    al, al
0x55555555535d -> 0x555555555398 // 359   jnz     short loc_1398
0x555555555398 -> 0x555555555396 // 392   movsxd  rsi, dword ptr [r8+rcx*4]
0x555555555396 -> 0x555555555392 // 38e   mov     r11d, [r8+rcx*4]
0x555555555392 -> 0x55555555538e // 389   movsx   edx, byte ptr [r9+rsi]
0x55555555538e -> 0x555555555389 // 386   xor     edx, r11d
0x555555555389 -> 0x555555555386 // 383   movsxd  rdx, edx
0x555555555386 -> 0x555555555383 // 37e   movzx   edx, word ptr [r10+rdx*2]
0x555555555383 -> 0x55555555537e // 37b   and     edx, 7Fh
0x55555555537e -> 0x55555555537b // 379   cmp     eax, edx
0x55555555537b -> 0x555555555379 // 377   jnz     short loc_1354
0x555555555379 -> 0x555555555377 // 373   add     rcx, 1
0x555555555377 -> 0x555555555373 // 36f   movsx   eax, byte ptr [rdi+rcx]
0x555555555373 -> 0x55555555536f // 36b   mov     edx, [r8+rcx*4]
0x55555555536f -> 0x55555555536b // 369   test    al, al
0x55555555536b -> 0x555555555369 // 365   setz    sil
0x555555555369 -> 0x555555555365 // 362   shr     edx, 1Fh
0x555555555365 -> 0x555555555362 // 35f   cmp     sil, dl
0x555555555362 -> 0x55555555535f // 35d   jnz     short loc_1354
0x55555555535f -> 0x55555555535d // 35b   test    al, al
~~~

发现输入的 password 没有做任何处理，只是进行比对。都不用求反解算法了，脚本改一下每次把目标值读出来再写进去就可以了。

~~~python
flag = b''

while True:
    line = []
    try:
        at_trap = gdb.execute('x /i $rip', to_string=True)
        at_trap = at_trap[3:at_trap.find(':')]
        if at_trap == '0x55555555537e':
            rdx = gdb.execute('info registers rdx', to_string=True)
            rdx = rdx[rdx.find('0x') + 2:][:2]
            flag += bytes.fromhex(rdx)
            gdb.execute('set $rax = $rdx')
        gdb.execute('signal SIGTRAP')
    except:
        with open('flag', 'wb') as f:
            f.write(flag)
        break
~~~

此外在调试时还有个问题没搞懂，尝试在信号处理函数处加断点，程序就没法捕获 SIGTRAP 了。对 gdb 的理解还是不太够，，，

