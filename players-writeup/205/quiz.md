# 小北问答 · 极速版

## 解题过程
在 web termial 打开了几次，发现每次题目不一样，随后多次运行脚本获取第一道题，发现可以获得 8 道题。


1. 支持 WebP 图片格式的最早 Firefox 版本是多少？

    百度搜索题干即可获得：“Firefox浏览器亦在65.0版本支持WebP图像。”

2. 在第一届 PKU GeekGame 比赛的题目《电子游戏概论》中，通过第 5 级关卡需要多少金钱？

    第一届的题目代码可以在 [github](https://github.com/PKU-GeekGame/geekgame-1st/blob/master/src/pygame/game/server/libtreasure.py#L19) 中找到，公式为 `300+int(level**1.5)*100`

3. 视频 bilibili.com/video/BV1EV411s7vu 也可以通过 bilibili.com/video/av_____ 访问。下划线内应填什么数字？

    搜到的[在线转换工具](http://www.atoolbox.net/Tool.php?Id=910)

4. 访问网址 “http://ctf.世界一流大学.com” 时，向该主机发送的 HTTP 请求中 Host 请求头的值是什么？

    Chrome 开发者模式，在 network panel 里访问链接，第一个网络包中可看到：`Request URL: https://ctf.xn--4gqwbu44czhc7w9a66k.com/`

5. 每个 Android 软件都有唯一的包名。北京大学课外锻炼使用的最新版 PKU Runner 软件的包名是什么？

    首先查了查包名是啥：

    > The APK Package Name must not contain spaces and special characters (such as “.” “_” except special characters,). The APK Package Name must contain at least one period (eg“ xx.xxx ”). The generally accepted form of APK Package Name creation is the reverse domain name (some sort of reverse address of web address).

    并且了解到 `.apk` 其实也就是个压缩包。没有 android 的开发环境，找到脚本虽然没跑通，但大概给了思路，包名应该在 `classes.dex` 这个文件里。于是 `strings` + `grep runner` 就找到了。

6. 北京大学某实验室曾开发了一个叫 gStore 的数据库软件。最早描述该软件的论文的 DOI 编号是多少？

    Google Scholar 搜索 gSotre，[第一篇](https://dl.acm.org/doi/abs/10.14778/2002974.2002976)就是。发现 URL 里就有 DOI。

7. 我刚刚在脑海中想了一个介于 X 到 Y 之间的质数。猜猜它是多少？

    首先可以用 `sympy.nextprime` 来获取满足条件的质数。多次尝试发现两个数字会变，但差距不大，解虽不唯一，但也不多。

8. 我有一个朋友在美国，他无线路由器的 MAC 地址是 d2:94:35:21:42:43。请问他所在地的邮编是多少？

    之前了解的是 MAC 地址是由 IEEE 分配给厂家的，所以应该比较好查。但在各个查询网站都查不到。进一步了解，MAC 地址的前三 bytes 构成 OUI，标识厂家。但第一 byte 的后两位有特殊含义：

    ![avatar](https://www.pathsolutions.com/hs-fs/hubfs/blog/fig-2-macncheese2-1.jpg?width=676&name=fig-2-macncheese2-1.jpg)

    所以这个 MAC 和厂家没关系？

    ？？？？？

然后猜测每次会出的题应该是随机的，故即便第八题查不到，第七题有概率过，也是能通关的。故写了如下脚本，运行半小时之内即得到 flag。

~~~python
import time
import re
import random

from pwn import *
from sympy import nextprime

while True:
    records = []
    p = remote('prob01.geekgame.pku.edu.cn', 10001)
    p.recvuntil('Please input your token: ')
    p.sendline('$TOKEN$')
    p.recvuntil('> ')
    p.sendline('急急急')
    for i in range(7):
        question = p.recvuntil('> ').decode()
        records.append(question)
        if 'Runner' in question:
            p.sendline('cn.edu.pku.pkurunner')
        elif 'gStore' in question:
            p.sendline('10.14778/2002974.2002976')
        elif 'WebP' in question:
            p.sendline('65')
        elif '一流' in question:
            p.sendline('ctf.xn--4gqwbu44czhc7w9a66k.com')
        elif '电子' in question:
            level = int(re.findall(r'通过第 ([\d]+) 级关卡', question)[0])
            p.sendline(str(300 + int(level**1.5)*100))
        elif 'bilibili' in question:
            p.sendline('418645518')
        elif '美国' in question:
            continue
        elif '质数' in question:
            start, end = re.findall(r'介于 ([\d]+) 到 ([\d]+) 之间的质数', question)[0]
            possible_list = []
            t = nextprime(int(start))
            while t < int(end):
                possible_list.append(t)
                t = nextprime(t)
            p.sendline(str(possible_list[random.randint(0, len(possible_list) - 1)]))
        else:
            raise ValueError(question)
    flag = p.recvall().decode()
    print(flag)
    if '你共获得了 100 分' in flag:
        break
    time.sleep(10)
~~~


