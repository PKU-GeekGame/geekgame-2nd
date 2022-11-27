# [Algorithm] 扫雷 II

- 命题人：debugger
- Flag 1：150 分
- Flag 2：200 分
- Flag 3：300 分

## 题目描述

<p>对于上一届 PKU GeekGame 的 “扫雷” 题目，有选手说：</p>
<p><br></p>
<table role="presentation" style="margin:auto; display:table; border-collapse: collapse; border: none; background-color: transparent; width: auto;"><tr>
<td style="width: 20px; vertical-align: top; border: none; color: #B2B7F2; font-size: 40px; font-family: &#39;Times New Roman&#39;, Times, serif; font-weight: bold; line-height: .6em; text-align: left; padding: 10px; text-orientation: upright">“
</td>
<td style="vertical-align: top; border: none; padding: 4px 10px;">建议主办方下次出扫雷这种题的时候可以真的搞一个扫雷的 UI<br />这样更好玩<br />虽然终端也能实现相同的逻辑，但是趣味性就差很多了</td>
<td style="width: 20px; vertical-align: bottom; border: none; color: #B2B7F2; font-size: 40px; font-family: &#39;Times New Roman&#39;, Times, serif; font-weight: bold; line-height: .6em; text-align: right; padding: 10px; text-orientation: upright">”
</td></tr>
<tr>
<td colspan="3" class="cquotecite" style="border: none; padding-right: 4%; font-size: smaller; text-align: right;"><cite>——zzh1996</cite>
</td></tr></table>
<p><br></p>
<p>因此我们今年就做了一个<strong>更好玩</strong>的扫雷游戏。</p>
<p>提示：理解去年的 “扫雷” 题目的解法对解出本题会有帮助。</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>如果从来没用过Go，或者不知道Go的随机数怎么生成，可以看看用Python写的等价的<a target="_blank" rel="noopener noreferrer" href="/service/attachment/prob14/prob14.zip">服务端实现</a>。</li>
<li>注意Go的time包使用的是monotonic clock，所以时间可能会快于实际的系统时间。</li>
<li>第三关真的是扫雷。经过一些处理后你甚至可以手玩。</li>
</ul>
</div>
<!--styling from https://zh.wikipedia.org/wiki/Template:Cquote, CC BY-SA 3.0-->

**【网页链接：访问题目网页】**

**[【附件：下载题目源码（prob14.go）】](attachment/prob14.go)**

**[【隐藏附件：prob14.zip】](attachment/prob14.zip)**

## 预期解法

此题的出题思路来自以下两道题目：
- [PlaidCTF 2022的PPPordle](https://ctftime.org/writeup/33231)，一道根据服务器时间猜随机数种子然后用服务器生成的数据验证的题目
- [Angstrom CTF 2022的Prophet](https://chovid99.github.io/posts/angstrom-ctf-2022/)，一道从已知随机数预测相邻的未知随机数的题目

Go的随机数的生成方法是Lagged Fibonacci generator，具体可以见sol目录下的gorand.py文件。

随机数重置时是用服务器时间做种子。因为提供了reset功能，所以可以把需要枚举的种子范围缩小到几秒钟（每秒对应1000个可能的种子）。同时，通过主动死亡也能拿到服务器生成的棋盘。

Flag 1只要枚举随机数种子之后模拟生成随机数，然后如果生成的棋盘和服务器端的相同，那么就可以确定是正确的种子，从而未来的状态也确定了。

Flag 3和Flag 1相似，但是256个格子里面有98个会被替换成无法预测的随机数。可以在枚举种子的时候不考虑这98个格子，然后枚举到种子后能确定新的棋盘中的其他158个格子的状态。接着可以用脚本点击其中没有雷的格子，然后回到游戏网页，把158个格子中没点开的标记成雷，接着手玩就能确定所有格子。当然你也可以真的写一个AI全自动处理。

Flag 2有多种解法：
- （比较简单的预期解）每一个棋盘对应4个64位随机数，而每个随机数状态等于之前第607个和第273个的和（mod 2^64），因此生成152个棋盘就能得到所有随机数状态，以及预测未来的随机数状态。
- （比较复杂的解）因为随机数状态之间的关系可以看成是矩阵和向量的乘法，因此利用矩阵乘法和快速幂可以从初始状态得到未来的任何一个状态。缺点是空间占用较大，生成第n个状态预计的时间复杂度是O(607^2\*log(n/607))，空间复杂度是O(607^3+607^2\*log(n/607))。
- （非预期解，by zzh）直接枚举种子，对每个种子生成20221119+256个随机数，然后和服务器端比较。

如果Flag 2的种子换成系统随机数，那么只有第一种解法还能使用。

sol目录有三关的exp，其中第三关的exp仅实现了把158个格子中没点开的标记成雷的功能，运行完后你还要手玩才能拿到flag。

### 非预期解

因为在reset函数没有清空curMarks数组，所以出现了这种非预期解（credit：zhn）：
1. 先用Flag 1的算法预测并挖开一些（不是全部）空格子。
2. 点reset，然后再切换到其他level
3. 此时挖开的格子仍然保持挖开的状态（包括有雷的格子），从而你可以根据上面的信息继续去挖其他空格子
4. 还可以不断重复reset，棋盘会变化，但是之前挖开的部分仍然会显示，因此可以如此重复直到完成游戏

### 附注

本题的最初版本有4个Flag，其中有一个Flag考矩阵乘法和快速幂，但是后来删掉了。另外最初版本并无reset功能（这样仍然可以通过启动实例的时间来推测随机数种子），后来降低难度，加上了这个功能。
