# [Misc] 编原译理习题课

- 命题人：debugger、xmcp（题面：xmcp）
- 玩挺大：150 分
- 玩挺长：150 分
- 玩挺花：200 分

## 题目描述

<blockquote>
<p>一个测试工程师走进一家酒吧，要了一杯啤酒。</p>
<p>一个测试工程师走进一家酒吧，要了一杯咖啡。</p>
<p>一个测试工程师走进一家酒吧，要了 0.7 杯啤酒。</p>
<p>一个测试工程师走进一家酒吧，要了-1 杯啤酒。</p>
<p>一个测试工程师走进一家酒吧，要了一份雪王大圣代和冰鲜柠檬水。</p>
<p>一个测试工程师走进一家酒吧，对核验健康宝的店员出示了舞萌 DX 玩家二维码。</p>
<p>一个测试工程师走进一家酒吧，打开了 PKU GeekGame 比赛平台。</p>
<p>一个测试工程师走进一家酒吧，用 g++ 编译他的代码。</p>
<p>酒吧没炸，但 g++ 炸了。</p>
</blockquote>
<p>你知道多少种让 g++ 爆炸的姿势呢？快来大显身手吧。</p>
<ul>
<li>让 g++ <strong>编译出的程序超过 8MB</strong> 可以获得 Flag 1</li>
<li>让 g++ <strong>输出的报错信息超过 2MB</strong> 可以获得 Flag 2</li>
<li>让 g++ <strong>因为段错误而崩溃</strong> 可以获得 Flag 3</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>前两个问题是开发 OJ 系统需要考虑的。PoC 很容易在网上搜索到。</li>
<li>第三问考的是 GCC 的 bug（internal compiler error）。可以参考一下 GCC 的 bug tracker。</li>
</ul>
</div>

**【终端交互：连接到题目】**

**[【附件：下载题目源码（prob04.zip）】](attachment/prob04.zip)**

## 预期解法

本节作者：debugger

此题其实在某种意义上是一道信息检索题。

先说Flag 2。直接在Google里面[搜索“g++ longest compile error”](https://www.google.com.hk/search?q=g%2B%2B+longest+compile+error)就能搜到。

[这里](https://codegolf.stackexchange.com/questions/5802/write-the-shortest-program-that-generates-the-most-compiler-warnings-and-errors)给出了Flag 2的一个解：
```c++
#include __FILE__
#include __FILE__
```

你或许还能搜到[这个知乎回答](https://www.zhihu.com/question/61427323)，里面给出了一个例子：

```c++
struct x struct z<x(x(x(x(x(x(x(x(x(x(x(x(x(x(x(x(x(x(y,x(y><y*,x(y*w>v<y*,w,x{}
```

这个例子来自[这个仓库](https://github.com/vijos/malicious-code)，这个仓库收集了各种 OJ 系统遇到的恶意代码，这也是我为什么在提示里面会说“开发 OJ 系统需要考虑的”。

然后是Flag 1。

上面的仓库里面能找到bigexe.c这个文件。这个文件的magic数组非常大，可以改小一点，略大于8MB即可：
```c++
#include <stdio.h>

char magic[1024 * 1024 * 8] = { '\n' };

int main()
{
    printf("hello, world");
    printf(magic);
    return 0;
}
```

如果你看过Hackergame 2021的题解的话，[“Amnesia”一题](https://github.com/USTC-Hackergame/hackergame2021-writeups/blob/master/official/Amnesia/README.md)的[mcfx的非预期解](https://mcfx.us/posts/2021-10-30-hackergame-2021-writeup/)也生成了一个大的目标文件。

最后是Flag 3。如果[直接搜索“Please include the complete backtrace with any bug report”](https://www.google.com.hk/search?q=g%2B%2B+Please+include+the+complete+backtrace+with+any+bug+report)，未必能找到一个能独立编译的exp。但是你或许能找到[这个页面](https://wiki.gentoo.org/wiki/Gcc-ICE-reporting-guide)，里面有这种G++错误的报告指南。找不到这个页面也没关系，只要能知道这种类型错误叫做internal compiler error就行。

既然这是GCC的bug，我们需要在[GCC的bug tracker](https://gcc.gnu.org/bugzilla/)里面找。在里面[搜索internal compiler error](https://gcc.gnu.org/bugzilla/buglist.cgi?quicksearch=internal%20compiler%20error)，能搜到大量结果，但是其中大部分和g++无关。点击“Comp”一列，将结果按照该列排序，就能把[g++相关的issue](https://gcc.gnu.org/bugzilla/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&bug_status=SUSPENDED&bug_status=WAITING&bug_status=REOPENED&field0-0-0=product&field0-0-1=component&field0-0-2=alias&field0-0-3=short_desc&field0-0-4=status_whiteboard&field0-0-5=content&field1-0-0=product&field1-0-1=component&field1-0-2=alias&field1-0-3=short_desc&field1-0-4=status_whiteboard&field1-0-5=content&field2-0-0=product&field2-0-1=component&field2-0-2=alias&field2-0-3=short_desc&field2-0-4=status_whiteboard&field2-0-5=content&order=component%2Cbug_status%2Cpriority%2Cassigned_to%2Cbug_id&query_format=advanced&type0-0-0=substring&type0-0-1=substring&type0-0-2=substring&type0-0-3=substring&type0-0-4=substring&type0-0-5=matches&type1-0-0=substring&type1-0-1=substring&type1-0-2=substring&type1-0-3=substring&type1-0-4=substring&type1-0-5=matches&type2-0-0=substring&type2-0-1=substring&type2-0-2=substring&type2-0-3=substring&type2-0-4=substring&type2-0-5=matches&value0-0-0=internal&value0-0-1=internal&value0-0-2=internal&value0-0-3=internal&value0-0-4=internal&value0-0-5=%22internal%22&value1-0-0=compiler&value1-0-1=compiler&value1-0-2=compiler&value1-0-3=compiler&value1-0-4=compiler&value1-0-5=%22compiler%22&value2-0-0=error&value2-0-1=error&value2-0-2=error&value2-0-3=error&value2-0-4=error&value2-0-5=%22error%22)筛选出来。注意要看状态是“NEW”的issue。里面有多个issue提供了可以使编译器崩溃的代码。

例如<https://gcc.gnu.org/bugzilla/show_bug.cgi?id=90747>提供了以下代码：
```c++
struct a {};
template <typename> struct b { a operator*(); };
template <typename c, typename d> c e(d);
template <typename, typename d> auto e(b<d> f) -> decltype(e<int>(*f)) {}
```

<https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85097>提供了以下代码：
```c++
template <typename A, typename B>
struct X {};

template <typename, typename... TOuter>
struct S
{
    template <typename... TInner>
    void function(X<TOuter, TInner>...)
    { }
};

void test_case() {
    S<void, int> s;
    s.function(X<int, short>());
}
```

注意上面两个issue分别有ice-on-invalid-code和ice-on-valid-code这两个keyword。你可以在[有ice-on-valid-code的issue列表](https://gcc.gnu.org/bugzilla/buglist.cgi?keywords=ice-on-valid-code)和[有ice-on-invalid-code的issue列表](https://gcc.gnu.org/bugzilla/buglist.cgi?keywords=ice-on-invalid-code)找到更多使GCC崩溃的例子。
