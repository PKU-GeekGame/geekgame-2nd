# [Web] 这也能卷

- 命题人：thezzisu
- Flag · 摆：100 分
- Flag · 大：200 分
- Flag · 烂：350 分

## 题目描述

<blockquote>
<p>某大学的很多课都有作业，特别是程序设计课程，往往会要求同学们写些简单程序当作业。
可惜，现在大家都很卷，考试总能取得极高的分数，甚至大作业也会卷出新花样来。
倘若某人在作业上开摆，那么等待他的往往只能是一个寄字，这也是某大学“摆寄”花名之由来。</p>
</blockquote>
<p>你有一位室友，他的口头禅是“我是摆大最摆的人”和“我从不内卷”。</p>
<p>这一次，他选修了一门叫《JavaScript程序设计》的课程。自从选修这门课程后，你发现他
天天熬到半夜，对着VSCode傻笑，实为异常。</p>
<p>一天，你在偶然间听到了他的喃喃自语：“只要我把小作业当期末作业做，大作业当毕业设计做，势必能卷过其他卷王！”
听到这，感觉收到了欺骗的你勃然大怒，打开了他的第一个“小”作业——一个“简单”的计算器。</p>
<p>另外，通过一顿家园，你获得了他的后端源码，<del>这让这道题的难度大大降低。</del></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<p>对于Flag1:</p>
<ul>
<li>成为会员会有不错的收获。</li>
<li>不要试图逆向<code>premium.js</code>，会变得不幸。</li>
</ul>
<p>对于Flag2:</p>
<ul>
<li>flag在<code>/* What's this? */</code>这处被删除的源代码里。</li>
</ul>
<p>对于Flag3:</p>
<ul>
<li>文档是个好东西。<a target="_blank" rel="noopener noreferrer" href="https://nodejs.org/api/process.html#process">看看文档吧</a>。</li>
<li>出题人当初是不打算给chrome沙箱的，但想了想还是给以降低难度。</li>
<li>Node.JS是怎么调试的？</li>
</ul>
</div>

**【网页链接：访问题目网页】**

**[【附件：下载题目源码（prob09-src.tar.gz）】](attachment/prob09-src.tar.gz)**

## 预期解法

### Flag1

检查前端代码，判断是否为`premium`用户的方法是检查`localStorage`中的`i_am_premium_user`字段，手动设置即可。

> 很多 SPA/PWA 网站前端通过`localStorage`来存储用户信息，手动修改就可以改变前端部分逻辑执行效果。

### Flag2

后端有一个简单的 WAF，过滤方式为正则匹配`^([a-z0-9+\\-*/%(), ]|([0-9]+[.])+[0-9]+)+$`。

预期解法为使用`unescape`函数配合 JS 中的隐式类型转换以绕过，参见`sol/poc.mjs`中的下列函数：

```js
function generatePayload(code) {
  return `eval(unescape(/%2f%0a${[...code]
    .map((_) => "%" + _.charCodeAt(0).toString(16).padStart(2, "0"))
    .join("")}%2f/))`;
}
```

这样，就能在 Chrome 沙箱和 Node.JS 沙箱中做到 RCE。可以发现在 Chrome 沙箱的全局上下文中有一个`flag`变量，但里面并没有`flag`。直接通过 DOM 操作拿到对应代码段源码就能找到 flag 了。

> JavaScript 是解释型语言，可以通过源码层面的奇技淫巧来实现一些有趣的事。

### Flag3

这个 flag 需要执行二进制。 Node.JS 沙箱运行在 esm 模式下，并通过 policy 禁用了`import`外部包。但我们仍然能访问`process`对象。

当一个`Node.JS`进程收到`SIGUSR1`信号时会进入调试模式，并在`127.0.0.1:9229`处暴露一个`DevTools API`。我们先使用`process.kill`向沙箱的父进程，也即后端主进程发送信号，在 Node.JS 沙箱里使用 fetch 去获取具体的 ws Endpoint，然后通过 Chrome 沙箱去连接这个 Endpoint，就能在后端主进程的上下文里运行代码——这一次将可以使用`require`来加载外部包，从而实现 RCE。

继而，我们可以使用`find`命令等手段寻找具有 suid 权限的二进制（本题中为`dd`），并使用其读取 flag 文件。

> 这个 flag 的灵感来源于 Node.JS 新的[Permissions API](https://nodejs.org/api/permissions.html)。但就算用了这个 API，Node.JS 沙箱依然非常危险。

### 解题脚本

flag2 和 flag3 的解题脚本在`sol/poc.mjs`中。

## 命题花絮

- JS 是门好语言，欢迎大家来学。
- flag2 本来是打算用`Proxy`来实现的，但是预期的方法也需要解析源码，所以换成了这个方式。选手们可能需要一些脑洞才能做出来。
