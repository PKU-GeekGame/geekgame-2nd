# 381654729

## 解题过程

要求的 number 不超过 48 位。开头的 1-4 位需要整除 1，开头 + 4 位需要整除 2...

由于每次补 4 位，不管前面是什么，一定能填上一个数满足条件。迭代求解即可。

但是 flag 的输入不是任意的，必须得是可打印的。所以写了个带回溯的版本试了试，跑出来了。


~~~python
# flag=input("Flag: ").encode()

options = [chr(c) for c in range(128) if chr(c).isprintable()]

def check(flag):
    num=int.from_bytes(flag,"big")^0x78082533ef0292cb658b46e259c5364b6bc7f4b2
    num_len=len(hex(num))-2
    for i in range(1,num_len+1):
        if (num>>((num_len-i)*4))%i>0:
            return i
    return i + 1

flag = ['{']
def recur(i):
    global flag
    if i == 20 and flag[-1] == '}':
        return True
    for c in options:
        flag.append(c)
        matched = check(''.join(flag).ljust(20, '0').encode())
        if matched > 2 * i:
            if recur(i + 1):
                return True
        flag.pop()
    return False


if(recur(1)):
    print('flag' + ''.join(flag))
~~~