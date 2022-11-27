# [Algorithm] 奇怪的加密

- 命题人：debugger
- Flag 1：250 分
- Flag 2：200 分

## 题目描述

<p>小 Z 学习了简易替换密码、维吉尼亚密码等多种古典密码，然后自己设计了一种古典密码。</p>
<p>小 Z 认为，这种密码没人能破解。</p>
<p>是这样的吗？</p>
<p>Flag 2 提示：</p>
<ol>
<li>此部分和 Flag 1 没有关联，也即不需要先解出 Flag 1</li>
<li>搜索引擎会给你一些帮助，虽然不是必需的</li>
<li>如果你还原的原文正确，把原文的内容放到搜索引擎里面搜索，会告诉你下一步做什么</li>
</ol>
<p><strong>本题 Flag 格式符合此正则表达式：<code>flag\{[a-z0-9_]+\}</code></strong></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>根据上下文你或许能知道某些字母对应的明文。如果第i个和第j个字母的明文和密文都相同，这说明了什么？</li>
<li>另外，英文字母的分布是有规律的，而加密的置换可以分解成若干个不相交的轮换，因此……</li>
<li>Flag 2：明文符合此正则表达式：<code>[0-9a-f\n]+</code>。另外，数字不会被加密，在密文还是保持原样。</li>
</ul>
</div>

**[【附件：下载题目附件（prob17.zip）】](attachment/prob17.zip)**

## 预期解法

### Flag 1

此题思路比较开放，有多种分析方法，此处只描述其中三种方法。此题需要大量手工工作，所以这里不提供完整代码。

可以把密文的所有字母提取出来，设`x='cinqwmzewt...takggieunz'`，共11109个字符，下标从0开始计数，如`x[0]='c'`，`x[1]='i'`，……

#### 方法1

首先，可以发现密文里面有多个单字母单词，例如“uziti n amhbueyp”和“n kcorcd”里面的“n”，而因为英语里有意义的小写单词只有a，因此可以假设这两个n会被解码为a，而这两个n的下标分别为1609和2599。设key里面a对应的轮换长度为k，n和a的位置差为t，有1609 mod k=t、2599 mod k=t，从而k是990的约数。

再考虑“gz a imqpgoqd”里面的“a”，下标为2662，所以k是2662的约数，同时是两数最大公约数22的约数。如果循环长度为22的话，有t=3。

密文中单字母单词还有f、e、s、n、g、p、t、z、k、h、b、i等等，同样可以算出对应的t，因为轮换已经涉及了超过11个字母，显然k>11，只有可能是k=22。

另外，有选手想出了类似的思路：寻找不同位置的较长的相同字母片段（例如密文中有两个Twhpyxq），可以假设对应的明文也相同，从而两个子串的位置的差是这些字母所在轮换的周期的最小公倍数的倍数。这点在整个加密的置换周期（这里是22）较小时有用，较大就不太管用了。

#### 方法2

假如已经知道了a对应的轮换长度为22，使用`[len([i for i in range(len(x)) if i%22==j and x[i]=='a']) for j in range(22)]`就能统计出原文不同位置字母加密为a的数量。这里是`[48, 26, 0, 5, 13, 19, 18, 10, 10, 66, 22, 1, 34, 3, 15, 38, 31, 12, 56, 31, 11, 10]`，例如第一个数为48，说明有48个下标为22的倍数，且该下标对应的字母加密后为a，从而原字母也是a；第三个数为0，说明有0个下标mod 22为2，且该下标对应的字母加密后为a，从而原字母是轮换中a前面第二个字母（这里是q）。

同样的，原文不同位置字母加密为n的数量为`[33, 10, 13, 44, 33, 2, 8, 17, 12, 20, 12, 5, 68, 30, 0, 31, 3, 7, 36, 32, 12, 52]`，两个数组的低谷分别在第3、12、14和6、15、17个数，可知轮换中a前面第二个字母和n前面第五个字母是相同的，也即a和n在轮换中位置相差3个字母。

如果不知道轮换长度，可以猜一个。例如j和d对应的数组分别是`[0, 11, 0, 11, 0, 12, 0, 12, 1, 17, 1, 14, 1, 9, 0, 7, 0, 15, 1, 9, 0, 17]`和`[15, 13, 17, 15, 15, 18, 18, 17, 18, 12, 19, 18, 20, 18, 17, 13, 10, 13, 16, 18, 12, 16]`，和原始数组的低谷分布不相似，所以j和d不在轮换里面。同时，也可以发现j和d并不在一个轮换，且j所在的轮换长度为2（因为只有26个字母，不可能是大于2的偶数）。

#### 方法3

有些字母不在a的轮换里面，例如j。一种处理方法是先处理完其他字母，然后尝试还原明文。这样在知道明文的一部分之后通过一些单词片段就能知道j被加密成什么字母。

#### 非预期解

有选手直接猜出了明文的部分内容并搜到了明文。

### Flag 2

使用上面的方法2（取轮换长度26）可以解出明文。接着[Google里面的内容](https://www.google.com.hk/search?q=b9ece18c950afbfa6b0fdbfa4ff731d3)可以发现是一些MD5值。因此可以枚举短字符串的MD5值进行恢复：

```python
from hashlib import md5
import string
md5set={}
for i in string.printable:
    md5set[md5(i.encode()).hexdigest()]=i

for i in string.printable:
    for j in string.printable:
        md5set[md5((i+j).encode()).hexdigest()]=i+j

for i in string.printable:
    for j in string.printable:
        for k in string.printable:
            md5set[md5((i+j+k).encode()).hexdigest()]=i+j+k

x=open("plain2.txt").readlines()
x=[i.strip() for i in x]
x=[md5set.get(i,i) for i in x]
print("".join(x))
```

即使你没有还原出明文，通过[搜索密文的数字](https://www.google.com.hk/search?q=415290769594460)也可以知道这是MD5值，又因为数字是不加密的，所以仍然可以解密：

```python
from hashlib import md5
import string
md5set={}
for i in string.printable:
    m=md5(i.encode()).hexdigest()
    m=''.join([i for i in m if '0'<i<'9'])
    md5set[m]=i

for i in string.printable:
    for j in string.printable:
        m=md5((i+j).encode()).hexdigest()
        m=''.join([i for i in m if '0'<i<'9'])
        md5set[m]=i+j

for i in string.printable:
    for j in string.printable:
        for k in string.printable:
            m=md5((i+j+k).encode()).hexdigest()
            m=''.join([i for i in m if '0'<i<'9'])
            md5set[m]=i+j+k

x=open("crypt2.txt").readlines()
x=[''.join([i for i in m if '0'<i<'9']) for m in x]
x=[md5set.get(i,i) for i in x]
print("".join(x))
```

### 附注

本题原来有3个flag，src目录里面crypt2_old.txt还有一段密文（原文不是英文，同时把空格去掉了从而上面的方法1也不能使用），但是因为此题需要较大工作量，为了减轻负担所以删去了此flag。

另外Flag 2的命题思路来自2022年[腾讯网络安全T-Star高校挑战赛](https://cloud.tencent.com/developer/competition/introduction/10042)。
