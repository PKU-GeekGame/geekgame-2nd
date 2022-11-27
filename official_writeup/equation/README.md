# [Algorithm] 方程组

- 命题人：debugger
- Flag 1：100 分
- Flag 2：200 分
- Flag 3：300 分

## 题目描述

<p>小 Z 编了一道数学练习题，解一个线性方程组。根据《高等代数》课上老师说的，如果方程数量小于变量数量，那么方程有无穷多个解。但是……</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>第二问的方程组有多少个自由变量？P.S：Flag 2格式符合此正则表达式：<code>flag\{[a-z0-9_]+\}</code>。</li>
<li>阅读一下<a target="_blank" rel="noopener noreferrer" href="https://reference.wolfram.com/language/ref/LatticeReduce.html">https://reference.wolfram.com/language/ref/LatticeReduce.html</a>，包括里面给的范例。当然，做这道题并不是必须要用Mathematica。</li>
</ul>
</div>

**[【附件：下载题目附件（prob11.zip）】](attachment/prob11.zip)**

## 预期解法

### Flag 1

第一问的方程数和变量数相等，所以解一个线性方程组就能拿到Flag 1。

```python
import numpy as np
import math
y=['16404', '16416', '16512', '16515', '16557', '16791', '16844', '16394', '15927', '15942', '15896', '15433', '15469', '15553', '15547', '15507', '15615', '15548', '15557', '15677', '15802', '15770', '15914', '15957', '16049', '16163']
x=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271][:len(y)]
x=[math.sqrt(i) for i in x]
y=[int(i) for i in y]
x=[x[-i:]+x[:-i] for i in range(len(x))]
flag=np.linalg.solve(x,y)
print(bytes([int(i+0.5) for i in flag]))
```

### Flag 2

第二问有28个变量、18个方程。因为flag以flag{开头，以}结尾，所以实际上不知道的变量只有22个，从而有4个自由变量。可以用消元法把其他变量表示成4个自由变量的线性函数，然后因为flag里面是ASCII字符，只要枚举95^4种自由变量组合，检查其他变量的值是否接近某个32和126之间的整数即可。给出提示之后枚举范围缩小到37^4。这还可以进一步改进，例如如果搜索到某个自由变量的某个值之后无论后面的自由变量取最大还是最小值都会导致某一其他变量的值超出范围，那么就不用进一步搜索。这里没有给出该算法的实现，请参见其他选手的wp。

也可以用第三问的方法做第二问，见sol目录里面的flag2.nb。此外，有些选手使用了整数线性规划的方法计算（见nxp和nynauy的wp），还有用[PyTorch的Adam优化器解的](https://blog.fyz666.xyz/blog/8100/)。

### Flag 3

第三问只有一个方程，直接枚举要枚举95^57种情况，显然是不可能的。这是一个[整数关系问题](https://en.wikipedia.org/wiki/Integer_relation_algorithm)，最早的实现此问题的算法是[LLL（Lenstra–Lenstra–Lovász）算法](https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm)，SageMath和Mathematica里面都有该算法的直接实现。见sol目录里面flag3.nb。

关于LLL的详细介绍，可以见[这里](https://ctf-wiki.org/crypto/asymmetric/lattice/lattice-reduction/)，这里不再多做介绍。

此外有选手使用了PSLQ算法（Mathematica提供了[FindIntegerNullVector函数](https://reference.wolfram.com/language/ref/FindIntegerNullVector.html)）。

<!--TODO：进一步介绍-->

