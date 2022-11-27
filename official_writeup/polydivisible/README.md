# [Algorithm] 381654729

- 命题人：debugger
- 题目分值：200 分

## 题目描述

<p>381654729，被称为“神奇而又独一无二的数”。</p>
<p>小 Z 找到了一个类似的数，并把 Flag 编码到这个数里面，你能找到它吗？</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<p>如果不考虑Flag里面只有可见字符，符合条件的数共8407789个。试着把它们都找出来。</p>
</div>

**[【附件：下载题目附件（prob16.py）】](attachment/prob16.py)**

## 预期解法

此题是求16进制的累进可除数（题面中的381654729是一个10进制的累进可除数。同时，381654729里面1-9这9个数字恰好各出现一次。16进制下不存在恰好1-f各出现一次的累进可除数。）

本题目使用的是动态附件，所以附件有多个版本（参见src目录里的gen.py）。下文叙述的是存档中“下载题目附件”链接给的附件。

首先运行`(2511413510787461238669866766355566039743902103765988701586).to_bytes(100,"big")`，可以发现flag有24字节。

可以参考[维基百科](https://en.wikipedia.org/wiki/Polydivisible_number#Programming_example)的Python代码（src目录里也有一份）直接修改，计算出所有累进可除数。然后反推出flag，检查是否只有可见字符即可。

```python
previous = [i for i in range(1, 16)]
new = []
digits = 2
while not previous == []:
    for n in previous:
        for j in range(0, 16):
            number = n * 16 + j
            if number % digits == 0:
                new.append(number)
                flag=(2511413510787461238669866766355566039743902103765988701586^number).to_bytes(24,"big")
                if len(set(flag)-set(range(127)))==0:
                    print(flag)
    previous = new
    print(digits,len(new))
    new = []
    digits = digits + 1
```
