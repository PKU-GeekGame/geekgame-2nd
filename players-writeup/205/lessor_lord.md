# 私有笔记

## 解题过程


### Share in my knowledge
题目已经明示了，搜 CVE 打就是了。然后去搜 MediaWiki 的 CVE。然后找个这个很有用的链接：[Security Release QA](https://www.mediawiki.org/wiki/2021-12_security_release/FAQ)

其中提到了三个问题，并给了三种可能的利用方式：

1. `action=mcrundo` or `action=mcrrestore`: can be used to edit without permission.

2. `action=edit&undo=###&undoafter=###`: can be used view the contents of arbitrary revisions.

3. `action=rollback&from=...` and `from={{:private page}}`: can be used to view the contents of arbitrary pages.

乱点的时候，在查看历史的时候，发现一个 query param `oldid=1` 推测页面数应该不会很多，开始枚举第二种利用方式。从 `undo=0&undoafter=0` 开始枚举到 `undo=1&undoafter=2` 就过了，，，我没理解，但他过了。



### Make yourself at home
登录之后发现可以编辑了。上述 3 个 CVE 并未提到能产生 RCE，得找其他办法，于是再去看那个 Software version，发现有个奇怪的扩展 Score。查了一下是用来嵌入LilyPond 乐谱的。去搜相关 CVE，发现有一个可以 RCE 的漏洞，和 `-dsafe` 有关。

先按照 Score 的文档试了一下 `<score>\relative c' { f d f a d f e d cis a cis e a g f e }</score>`，发现确实能使用 Lilypond 的功能。

然后在 Lilypond 的[文档](https://lilypond.org/doc/v2.22/Documentation/usage/command_002dline-usage)处查询 `-dsafe`，找到两个给出的例子：

~~~
% too dangerous to write correctly
#(s ystem "rm -rf /")
% malicious but not destructive
{ c4^$(ly:gulp-file "/etc/passwd") }
~~~

先尝试执行了下面的例子，发现在乐谱图片的上方出现了文件内容。即可以实现文件读取。

用参考下面的例子，试了 `<score>\relative c' #(system "ls /")</score>`，点显示预览，发现 `wrong type for argument 2.  Expecting music, found 0`，说明执行成功了。

利用 `tmp/tmp` 作为中间文件，就相当于获得了一个 shell。比较奇怪的是，发现 flag2 在 `/` 下，但 `<score>\relative c' { c4^$(ly:gulp-file "/flag1") }</score>` 并不能得到 flag。之后先把 flag2 输出到 `/tmp/tmp` 再读取发现是 OK 的，推测是两个用户？
