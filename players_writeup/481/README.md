# GeekGame 2.0 WriteUp

​	——wwj

## 前言

​		GeekGame 2.0 是本人参加的第一场 CTF 比赛。虽然限于知识储备，能做的题不多，但在比赛~~（坐牢）~~过程中还是挺欢乐的。

​		不过对于我这样的新生来说，确实有点自闭。~~《让 没 有 相 关 经 验 的 新 生 享 受 比 赛》~~

​		~~享受夺旗，享受生活。心中有光，闪耀四方！ CTF 不为所动 做更专业的自己~~

![ﾋﾄﾘﾀﾞｹﾅﾝﾃｴﾗﾍﾞﾅｲﾖｰ](img/you-sticker.png)

​		<font color=white>这风格，拉拉人+音游人狂喜！</font>

## Prob19 †签到†（Tutorial）

​		下载附件，将乱码（实则 Wingdings 字体）复制到文本编辑器中，得到：

​		tips: 用 vscode 可以完整复制内容。

```
fa{hns4PaigGeGm!
lgTak__lyn_ekae}
```

​		竖着看（即栅栏密码）即得到 flag。

​		~~怎么和去年一样啊。~~

​		<font color=white>不会有人不看背景的 Setsuna 吧（</font>

## Prob01 小北问答 · 极速版（Tutorial）

​		共有 8 种可能的题型。

​		最终还需要在 3 秒内输出答案。需要用程序自动提交。

#### PKU Runner 包名

​		打开手机 /sdcard/Android/data/ 目录可找到 PkuRunner 对应包名。

#### gStore DOI 编号

​		知网搜索 gStore，找到最早的一篇即得。

#### 《电子游戏概论》

​		翻看 pygame 的源代码，可以发现有一行：

```python
GOAL_OF_LEVEL = lambda level: 300+int(level**1.5)*100
```

#### 支持 WebP 的 Firefox

​		搜索引擎检索关键词即得。

#### 范围内质数

​		可以编写程序计算，随机给出一个（需要碰运气）。

#### ~~无线路由器 Mac 地址~~

​		这个问题我不太清楚怎么搞，听说 Google Geolocation 的 API 可以实现这个功能，但是申请 API 和调用的时候总出问题，于是就没整出来。

#### Host 请求头

​		用 chrome 抓包可以找到：ctf.xn--4gqwbu44czhc7w9a66k.com

#### BV av 号码

​		相应的转换工具可以在搜索引擎搜索到。

有了答案，使用 socket 工具实现与服务器通信即可：

```python
from math import sqrt
import random
import socket
from time import sleep

token = "616:fake{He2e_1s-my_t0ken}"

s = socket.socket()

def prime(n):
    for i in range(2, int(sqrt(n))):
        if n % i == 0: return False
    return True
def answer(p):
    print(p)
    s.sendall((p + "\n").encode("utf-8"))
    sleep(.1)
    r = s.recv(1024).decode("utf-8")
    print(r)
    return r

def run():
    global s, Nope, allRun
    try:
        have = False
        s = socket.socket()
        s.connect(("prob01.geekgame.pku.edu.cn", 10001))

        print(s.recv(1024))
        answer(token)
        question = answer("急急急")
        for k in range(7):
            if (question.find("美国") != -1):
                # qaq
                question = answer("42, The answer to life, the universe, and everything")
            if (question.find("WebP") != -1):
                question = answer("65")
            if (question.find("bilibili") != -1):
                question = answer("418645518")
            if (question.find("质数") != -1):
                pos1 = question.find("介于") + 2
                pos2 = question.find("到")
                pos3 = question.find("到") + 1
                pos4 = question.find("之间")
                L = int(question[pos1 : pos2])
                R = int(question[pos3 : pos4])
                plist = list(filter(prime, range(L, R + 1)))
                question = answer(str(random.choice(plist)))
            if (question.find("gStore") != -1):
                question = answer("10.14778/2002974.2002976")
            if (question.find("电子游戏概论") != -1):
                pos1 = question.find("通过第") + 3
                pos2 = question.find("级关卡")
                num = int(question[pos1 : pos2])
                question = answer(str(300 + int(num ** 1.5) * 100))
            if (question.find("PKU Runner") != -1):
                question = answer("cn.edu.pku.pkurunner")
            if (question.find("Host") != -1):
                question = answer("ctf.xn--4gqwbu44czhc7w9a66k.com")
        if (question.find("你共获得了 100 分。")):
            return True

        s.close()
    except ConnectionAbortedError as e:
        print(e)
    return False

while not run():
    sleep(6)
```

​		由于题目是八选七，因此空一题是有机会过的。

​		经过了很长时间的挂机，终于通过了。~~（我是真的不会，不是故意卡服 qwq）~~

## Prob04 编原译理习题课（Misc）

#### 玩挺大

​		常量字符串是存储在程序中的，从而只需要构造一个非常大的常量字符串即可。

​		要使短代码构造出非常长的数据，可以使用宏定义展开。

​		注意代码编译时间只有 3 秒，尽量避免include标准库。

```c++
#define a "abcdefghijk"
#define b a a a a a a a
#define c b b b b b b b
#define d c c c c c c c
#define e d d d d d d d
#define f e e e e e e e
#define g f f f f f f f
#define h g g g g g g g

const char str[] = h;
int main() {
    return 0;
}
//EOF
```

#### 玩挺长

​		与 flag1 同理，使用宏定义展开扩大输出。

​		为了防止编译错误从而提前退出，可以让 g++ 不断报警告而不编译错误。

```c++
#define a x >> 1
#define b a + a + a + a + a + a
#define c b + b + b + b + b + b
#define d c + c + c + c + c + c
#define e d + d + d + d + d + d
#define f e + e + e + e + e + e
#define g f + f + f + f + f + f
#define h g + g + g + g + g + g

#include <bits/stdc++.h>

int main() {
    int x;
    std::cout << (h);
    return 0;
}
//EOF
```

#### 玩挺花

​		用普通的手段很难使 g++ 崩溃，所以尝试去 GCC 的官方 bug 库搜索。

​		以 `crash` 为关键字在 https://gcc.gnu.org/bugzilla 上检索，按时间排序，将搜索结果多次尝试。最终找到了符合要求的解。

```c++
void operator""_x(const char *, unsigned long);
static_assert(false, "foo"_x);
//EOF

// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=105300
```

## Prob15 Flag Checker（Misc）

​		对 jar 文件用 JD-GUI 工具进行解包。

​		检查，可以发现有两段可疑代码：

```java
String str = "\u0089\u009A...\u00C6\u0092"; // 内容过长已省略
StringBuilder stringBuilder = new StringBuilder();
for (byte b = 0; b < str.length(); b++)
  stringBuilder.append((char)(str.charAt(b) ^ 0xEF)); 
scriptEngine.eval(stringBuilder.toString());
```

```java
byte[] arrayOfByte = this.textField1.getText().getBytes("UTF-8");
String str = rot13(Base64.getEncoder().encodeToString(arrayOfByte));
if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(str)) {
  JOptionPane.showMessageDialog(null, "Correct");
} else {
  JOptionPane.showMessageDialog(null, "Wrong");
}
```

#### Flag 1

​		对第二段代码，将数据串依次解密即可：先 rot13（注意数字也会转换），后 base64。

#### Flag 2

​		如第一段代码所示，将数据串每个字节异或 0xEF，可得一个函数：	

```java
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}
```

​	对其进行变量名替换，还原函数调用等反混淆方法，使程序可读性提高。

```java
function checkflag2(x){
	return JSON.stringify(x.split("").map(function(r){return r.charCodeAt(0);}))
        == JSON.stringify(
        [0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232].map(
            function(r){return(checkflag2+"").charCodeAt(r);}))?"Correct":"Wrong";
}
```

​		代码意思即为在 checkflag2 函数转为字符串的值中取出若干位得到 flag （注意是在简化前的的函数取字符）。

## Prob03 智慧检测器（Misc）

​		试玩几次可以了解游戏大致规则：有若干层的迷宫，在 + - 处可以上下楼，T 处可以传送。

​		再看眼程序：

```python
mapsizes = [[7, 1, 0],
            [11, 3, 0],
            [55, 80, 1],
            ]
```

​		只允许走 99 步，需要上到 80 层。说明必须要利用程序的 bug。

#### 破坏者

​		这个 Flag 算是运气比较好才拿到的（甚至抢了个一血）。在一次试玩中，我在 Level 1 时不小心输入了 SU，突然程序就崩溃了。

#### 调停者

​		这时思考为什么会崩溃，可以发现在一行输入多个指令时，第一个不合法的指令仍然会被执行。因此如果在只有 1 层的 Level 1 中选择了上楼，会产生数组越界。而且进一步观察，这个不合法但被执行的指令也不消耗步数。

​		因此在 Level 3 中，只需要每走一步时上一层就可以在最大步数之内上到顶层。在过程中也需要不断地向对面靠近，否则最终剩余步数还是不够。使用此方法多尝试几次即可过关。

## Prob21 企鹅文档（Web）

​		看了一下网址，居然是 doc.qq.com。居然让我们找 tx 官方的 bug？

​		在网页乱动了几下发现：点击下方按钮刷新工作表后，隐藏的数据在一瞬间会出现。

<img src=img/prob21_1.png width=50%><img src=./img/prob21_2.png width=50%>

​		同样的道理，在这一瞬间，筛选功能和搜索功能也可以使用。

​		由于筛选不能筛隐藏行中数据，因此考虑搜索功能。

​		枚举每个字母，搜索其在文档中的位置，就可以还原出数据。

<img src=img/prob21_3.png width=70%>

​		从而得到一个链接：https://geekgame.pku.edu.cn/service/template/prob_kAiQcWHobsBzRJEs_next/

​		下载附件，发现是网站数据包。然而这是用 json 格式保存的，并没有什么加密。直接根据提示搜索 `Below is your flag` 的位置。在该位置下面的一堆数据后又发现了 `Above is your flag`。将数据格式整理之后，得到若干数字，与提示的图片对应一下发现就是黑色方格的位置。

​		使用程序画一下就得到 flag 了。

```python
with open("text.txt", "r") as f:
    s = map(int,f.read().split())
    p = [0] * (230 * 11)
    for i in s:
        p[i] = 1
    for line in range(230):
        for i in range(11):
            if p[line * 11 + i]:
                print("█", end='')
            else:
                print(" ", end='')
        print('')
```

​		？提示是流量分析？什么流量分析，我一点都不懂（

​		这想必

## Prob07 私有笔记（Web）

#### 知识，与你分享

​		根据提示，在 CVE 网站和搜索引擎上搜索 MediaWiki 的漏洞。搜索到关于 MediaWiki [2021-12_security_release](https://www.mediawiki.org/wiki/2021-12_security_release/FAQ) 的内容。使用下面提到的 rollback bug，使用 ?action=rollback&from={{:Flag}} 即可看到 Flag 页面内容。



## Prob08 企业级理解（Web）

#### 赋能管理后台		

​		打开网站，是个登录页面。根据 java 代码，网站有 `/admin`，`/admin/query`，`/admin/source_bak` 几个接入点。

​		然而经过尝试发现，通过 `/admin/` 可以绕过登录直接访问后台，因此访问 `/admin/source_bak/` ，下载到了后台的源代码。

​		可以发现后台的逻辑为发送 POST 到本地 8079 端口，同时携带 type 参数（默认为 PKU )。发现 type 参数给了三个选项，经过尝试发现访问：`/admin/query/` 时，返回了 `{"type":"PKU","value":"Welcome to PKU GeekGame 2.0!"}` 。同时给了几个备选项，访问 `/admin/query/?type=PKU_GeekGame` 时得到了 Flag 1

#### 盘活业务增长

​		观察 java 代码，可以发现还有一个本地 8080 端口没用过。观察代码，发现访问 `/admin/localhost:8080` 可以忽略前面 baseUrl 的设定。尝试访问 8080 端口，返回了 `Endpoints:/bonus/source_bak`，提示有 `bonus/source_bak` 的接入点。

​		此时碰到了一个难点，我们难以在 `/admin/{index}` 的模式下输入左斜杠。然而代码中有使用 urlDecode 的逻辑，因此可以对访问的位置进行两次 urlEncode。访问 `/admin/localhost:8080%252Fbonus` 使用 bonus 服务，即可得到 Flag 2。

## Prob09 这也能卷（Web）

#### Flag · 摆

​		打开网页，是个计算器。尝试开启 Premium 功能。

​		在网页源代码中，发现了一个加密过的脚本 `premium.js`。在网上搜到了这是 ob 混淆。

​		使用网上的解混淆工具：[decode_obfuscator](http://tool.yuanrenxue.com/decode_obfuscator)，得到代码。

```javascript
const flag0 = "flag{fr0nt3nd_log1c_m4tters}";
const [code, activate, status] = ["code", "activate", "status"]["map"](x=>document["getElementById"](x));

if (localStorage["getItem"]("i_am_premium_user")) {
  status["innerText"] = "Premium Activated: flag{fr0nt3nd_log1c_m4tters}";
  code["disabled"] = true;
  code["placeholder"] = "Premium Activated";
  activate["disabled"] = true;
  activate["innerText"] = "You do not need to activate premium again";
} else {
  status["innerText"] = "Not Activated";
  activate["addEventListener"]("click", () => {
    if (code["value"] === flag0) {
      alert("Welcome to premium!");
      localStorage["setItem"]("i_am_premium_user", true);
      location["reload"]();
    } else {
      alert("Ooooops your code is wrong {{{(>_<)}}}");
    }
  });
}
```

​		取得 Flag 1，同时获得了 Premium 权限。

## Prob16 381654729（Algorithm）

​		抢了个一血，真不戳。

​		下载附件程序，代码逻辑即为：`(x >> 4 * (len - i)) mod i == 0`

​		即 16 进制下：前 i 位是 i 的倍数。

​		通过 dfs 找到了几个最长的数。

```python
table = "0123456789ABCDEF"
maxdep = 0
anslist = []
def dfs(dep, num, str):
    global anslist, maxdep, table
    if (dep > maxdep):
        anslist = [str]
        maxdep = dep
    elif dep == maxdep:
        anslist += [str]
    for i in range(16):
        if dep == 1 and i == 0:
            continue
        Nnum = num * 16 + i
        if Nnum % dep > 0:
            continue
        dfs(dep + 1, Nnum, str + table[i])

dfs(1, 0, "")
print(anslist)
```

经过还原可得 Flag：

```python
anslist = ['34E4A468166CD8604EC0F8106AB4326098286CF', 'AA44CE207C78FC30003C3CC0D8382E2078D07EF','FAE06678C2E884607EB8B4E0B0A0F0603420342']

for entry in anslist:
    num = int(entry, 16)
    w = 2511413510823276375832487608477453289997576663646622708914 ^ num
    print(w.to_bytes(128, 'big'))
```

## prob18 乱码还原（Algorithm）

#### Flag 1

​		整理代码逻辑：将原文经过 AES 加密后，将每个字节数据映射到一个或两个汉字上，将汉字的 utf-8 编码用 shift-jis 方式解码，再用 utf-8 编码输出到文件。

​		但是由于 shift-jis 码表里有些位置没有字符，解码过程可能会失败。因为参数里设置了 `errors=ignore` 

​		举个例子：

​			`佛曰：` 进行 utf-8 编码后是：`e4 bd 9b / e6 9b b0 / ef bc 9a`。

​			将编码尝试用 shift-jis 解码，得到 `菴帶峅ｼ`

​			实际上是：`e4 bd` → `菴`，`9b e6` → `帶` ，`9b b0` → `峅`，`ef` 失败，`bc` → `ｼ`，`9a` 失败。

​		因此需要对密文的 shift-jis 编码对应到原文的 utf-8 编码（在有些字符解码失败丢失时）。

​		尝试手动解码一段时间后，发现以下特点：

   1. 每个汉字 utf-8 都为 3 字节长，且第一位为 e。

   2. 除了开头的 ef 失败以外，正文里的 "e?"  字节均没有丢失的情况。

      因此将所有 "e?" 作为分隔符，每一段与某个汉字匹配。然而这样每一段的选择并不是唯一的，因此需要搜索找到合理的解。

#### *Flag 2

​		密文实在过长， 直接搜索肯定跑不出结果。

​		根据提示，去学习了一下 AES 加密的分块机制。AES 加密是将原文按 16 个字节分块，前一块的密文作为后一块的 IV。因此可以每 16 个字节做一次搜索。

```python
from Crypto.Cipher import AES
from random import choice
KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
IV = b'Potato@Key@_@=_='

TUDOU = [...]
BYTEMARK = [...]

def get_data(ciphertext):
    data = b''
    i = 0
    while i < len(ciphertext):
        if ciphertext[i] in BYTEMARK:
            i = i + 1
            data = data + bytes([TUDOU.index(ciphertext[i]) + 128])
        else:
            data = data + bytes([TUDOU.index(ciphertext[i])])
        i = i + 1
    return data

def Decrypt(ciphertext):
    data = get_data(ciphertext)
    # print(len(data))
    # 2. Use AES-256-CBC to Decrypt
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    result = cryptor.decrypt(data)
    # 3. Remove Paddings (PKCS7)
    flag = result[-1]
    if flag < 16 and result[-flag] == flag:
        result = result[:-flag]
    # 4. Decode Plaintext with UTF-16 Little Endian
    return result.decode('utf-16le')

found = False
newpos = 0
def dfs(dep, now, byte):
    global found, newpos, IV
    if (byte == 16):
        try:
            s = Decrypt(now)
            for c in s:
                if (ord(c) >= 127):
                    return
            found = True
            newpos = dep
            IV = get_data(now)
            print(s, end = '')
        except ValueError as e:
            # print("failed", e)
            pass
        return
    for c in choices[dep]:
        if (c in BYTEMARK and len(now) >= 1 and now[-1] in BYTEMARK):
            continue
        dfs(dep + 1, now + c, byte + (not c in BYTEMARK))
        if (found): return

codemap = []
for c in (BYTEMARK + TUDOU):
    d = str(c.encode("utf-8"))[2:-1].replace('\\x',' ').split()
    codemap += [(d[0], d[1], d[2], c)]

choices = []
now_pos = 0
w = []

with open("flag2.dec") as f:
    w = f.read().split()
    for i in range(len(w)):
        choice = []
        if (w[i][0] != 'e'):
            continue
        pos = len(w)
        for j in range(i + 1, len(w)):
            if (w[j][0] == 'e'):
                pos = j
                break
        if not (pos == i + 1 or pos == i + 2 or pos == i + 3):
            assert(False)
        if (pos == i + 3):
            for (a, b, c, d) in codemap:
                if [a, b, c] == w[i : pos]:
                    choice += [d]
        elif (pos == i + 2):
            for (a, b, c, d) in codemap:
                if a == w[i] and (b == w[i + 1] or c == w[i + 1]):
                    choice += [d]
        elif (pos == i + 1):
            for (a, b, c, d) in codemap:
                if a == w[i]:
                    choice += [d]
        choices += [choice]
while (now_pos < len(choices)):
    found = False
    dfs(now_pos, "", 0)
    if (not found):
        print("error!")
        exit(0)
    now_pos = newpos
```

## prob17 奇怪的加密（Algorithm）

​		观察算法，即给定字母的一个置换 $p$，将第 $i$ 个字母作用在 $p^{i-1}$ 上。

#### Flag 1

​		经过这样一个复杂的加密，密文应当乱七八糟，但是在其中仍能找到完全相同的单词。排除了那些特别短的可能是偶然的情况，比较长的单词应当是同一个词刚好经过了一个循环节得到的。

​		若一个比较长的词在 $i, j$ 两个位置出现，那么我们可以认为这其中的字母循环节都是 $(j-i)$ 的因数。因此对所有这样的限制条件取 gcd，可以得到很多字母的循环节。

```python
from math import gcd

pos = {}
period = [0] * 26

def letter(c):
    return c.islower() or c.isupper()

now_pos = 0

with open("crypt1.txt", "r") as f:
    w = f.read()
    s = list(w.split())
    for w in s:
        word = ""
        for c in w:
            if (letter(c)):
                word += c.lower()
        now_pos += len(word)
        if (len(word) <= 10):
            continue
        if word not in pos:
            pos[word] = [now_pos]
        else:
            pos[word] += [now_pos]
for (word, poses) in pos.items():
    if (len(poses) >= 2):
        print(word, poses)
    for j in range(1, len(poses)):
        u = poses[j] - poses[j - 1]
        for c in word:
            period[ord(c) - 97] = gcd(period[ord(c) - 97], u)

for i in range(26):
    print(chr(i + 97), ": ", period[i])
```

​		运行后发现很多数的循环节都是 22，还有一些是 22 的倍数（除了 DJUV 四个字母）。推测该置换有一个 22 的循环。

​		然而，没有一些原文内容，还是无法得到这个循环。

​		考虑到一篇英文文章出现单个小写字母很有可能是 `a`，因此我们分离出所有的单个小写字母，将其原文对应为 `a`。这样通过循环的性质，可以还原出这个大循环。剩余的四个字母可以通过还原原文来修正。

```python
key = {}

def letter(c):
    return c.islower() or c.isupper()

now_pos = 0

with open("crypt1.txt", "r") as f:
    w = f.read()
    s = list(w.split())
    for w in s:
        word = ""
        for c in w:
            if (letter(c)):
                word += c.lower()
        if (len(w) == 1 and w[0].islower()):
            key[now_pos % 22] = w[0]
        now_pos += len(word)
        
for (c, w) in sorted(key.items()):
    print(c, w)
```

​		在大段文章中搜索 flag，得到：

```
The flag is foxtrot lima alpha golf left bracket foxtrot romeo echo nine uniform echo november charlie yankee underscore four november alpha lima yankee five india sierra underscore one sierra underscore uniform sierra echo foxtrot uniform lima right bracket.
```

​		将 left/right bracket 转换成括号，one, four, five, nine 转换成数字，underscore 转换成下划线，其余单词取首字母即得 flag。

####  Flag 2

​		观察密文，每行是 32 列的字母数字组合。然而这种加密不改变数字的值，因此可以挑一段比较长的数字搜索。搜索文本 `73795649038408` 时，发现搜索项为 `4a8a08f09d37b73795649038408b5f332` 刚好和该行对应上了。翻了一下，发现这个就是字母 `c` 的 `md5` 算法结果。推测原文每行都是一个 `md5` 的哈希值。

​		对一行密文，枚举每个字母计算`md5`判断其中数字能不能对应。事实上只有一小部分的字母能对应上。

​		接下来可以通过已破解的密文推断密钥。对于一个已破解的位置，若原文和密文的第 $i$ 个字母相同，那么可以知道这个这个字母的循环节应当是 $i-1$ 的约数。与 Flag 1 一样取 gcd，可以得到每个字母循环节。发现很多字母的循环节都是 26，还有些是 26 的倍数。合理推断该置换是一个 26 的循环。

​		因此对第 $i$ 个字母若原文是 $c_1$，密文是 $c_2$，可得在循环中 $c_2$ 在 $c_1$ 后 $i-1$ 个位置。因此可以还原出原文。

```python
from hashlib import md5
from math import gcd

def mark(s):
    ans = ""
    for c in s:
        if c in "0123456789":
            ans += c
    return ans
def same(s, t):
    return mark(s) == mark(t)
def letter(s):
    ans = 0
    for c in s:
        if c.islower() or c.isupper():
            ans += 1
    return ans

pos = [0] + [-1] * 25
hints = []
with open("crypt2.txt", "r") as f:
    now_pos = 0
    w = f.read()
    for code in w.split():
        found = ''
        for p in range(32, 255):
            if (same(md5(chr(p).encode()).hexdigest(), code)):
                found = chr(p)
                print(found, end = '')
                break
        else:
            print('*', end = '')
        if (found != ''):
            s = md5(found.encode()).hexdigest()
            t = code
            for i in range(32):
                if (s[i].islower()):
                    hints += [(ord(s[i]) - 97, ord(t[i]) - 97, now_pos)]
                    now_pos += 1
        else:
            now_pos += letter(code)

for time in range(26):
    for (s, t, u) in hints:
        if (pos[s] != -1):
            pos[t] = (pos[s] + u) % 26
        if (pos[t] != -1):
            pos[s] = (pos[t] + 26 - u % 26) % 26

for i in range(26):
    print(chr(i + 97), pos[i])
```

​		最后将无法还原的`md5`进行搜索，发现都是两个字符拼接的`md5`（要是能猜到就不用这么费事了）。暴力枚举即可。

```python
from hashlib import md5

charset = [chr(i) for i in range(32, 127)]

def get(s):
    return md5(s.encode()).hexdigest()

with open("md5.txt", "r") as f:
    w = f.read()
    for code in w.split():
        found = False
        for p in charset:
            if get(p) == code:
                print(p, end='')
                found = True
        for p in charset:
            for q in charset:
                if (get(p + q) == code):
                    print(p + q, end='')
                found = True
        if (not found):
            print("*", end='')
```

## prob11 方程组（Algorithm）

​		题意大概是解一个线性方程组：
$$
AX=B\\
a_{i,j} =\sqrt{p_{(j-i)\mathrm{mod}n}}
$$
​		但是只给出 B 的前若干维。

#### Flag 1

​		观察代码发现，给出了 B 的所有数值，直接高斯消元即可：

```python
import os
from decimal import *

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

result = [16404, 16416, 16512, 16515, 16557, 16791, 16844, 16394, 15927, 15942, 15896, 15433, 15469, 15553, 15547, 15507, 15615, 15548, 15557, 15677, 15802, 15770, 15914, 15957, 16049, 16163]

# len(flag) = 26
n = 26
p = primes[:n]
matrix = []

getcontext().prec = 20

for i in range(n):
    line = [Decimal(p[j]).sqrt() for j in range(n)]
    line += [Decimal(result[i])]
    print(line)
    matrix += [line]
    p = [p[-1]] + p[:-1]

for i in range(n):
    l = i
    for j in range(i + 1, n):
        if (abs(matrix[j][i]) > abs(matrix[l][i])):
            l = j
    if l != i:
        for k in range(n + 1):
            matrix[i][k], matrix[l][k] = matrix[l][k], matrix[i][k]
    for j in range(i + 1, n + 1):
        matrix[i][j] /= matrix[i][i]
    matrix[i][i] = 1
    for j in range(n):
        if j != i:
            for k in range(i + 1, n + 1):
                matrix[j][k] -= matrix[j][i] * matrix[i][k]
            matrix[j][i] = 0

ans = [int(round(matrix[i][n])) for i in range(n)]

for c in ans:
    print(chr(c), end='')
```

#### Flag 2

​		题目把方程组的最后 10 个方程删掉了。

​		根据 flag 的格式 flag{} 可以确定六个变量，还有四个自由变量通过枚举可以求得。

​		最后要尽量取答案接近整数的那些。

```python
from decimal import *

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

result = [19106.6119577929, 19098.1846041713, 19124.6925013201, 19072.8591005901, 19063.3797914261, 19254.8741381550, 19410.9493230296, 18896.7331405884, 19021.3167024024, 18924.6509997019, 18853.3351082021, 18957.2296714145, 18926.7035797566, 18831.7182995672, 18768.8192204100, 18668.7452791590, 18645.9207293335, 18711.1447224940]

# len(flag) = 28
n = 28
p = primes[:n]
matrix = []

getcontext().prec = 30

for i in range(n - 10):
    line = [Decimal(p[j]).sqrt() for j in range(5, n - 1)]
    res = Decimal(result[i])
    for j in range(5):
        res -= Decimal(p[j]).sqrt() * ord("flag{"[j])
    res -= ord("}") * Decimal(p[-1]).sqrt()
    line += [res]
    matrix += [line]
    p = [p[-1]] + p[:-1]

eps = Decimal(10) ** -20

for i in range(n - 10):
    l = i
    for j in range(i, n - 10):
        if (abs(matrix[j][i]) > abs(matrix[l][i])):
            l = j
    if l != i:
        for k in range(n - 6 + 1):
            matrix[i][k], matrix[l][k] = matrix[l][k], matrix[i][k]
    if (abs(matrix[i][i]) < eps):
        continue
    for j in range(i + 1, n - 6 + 1):
        matrix[i][j] /= matrix[i][i]
    matrix[i][i] = Decimal(1)
    for j in range(n - 10):
        if j != i:
            for k in range(i + 1, n - 6 + 1):
                matrix[j][k] -= matrix[j][i] * matrix[i][k]
            matrix[j][i] = Decimal(0)

print(matrix)

charset = "0123456789qwertyuiopasdfghjklzxcvbnm_"

val = [Decimal(0)] * 22
ans = [0] * 22
m = Decimal(1)

def check(c):
    global m
    M = Decimal(0)
    for i in range(4):
        val[18 + i] = ord(c[i])
    for i in range(18):
        val[i] = matrix[i][22]
        for j in range(4):
            val[i] -= val[18 + j] * matrix[i][18 + j]
    for i in range(22):
        ans[i] = int(round(val[i]))
        if ans[i] < 32 or ans[i] > 127:
            return
        M = max(M, abs(val[i] - ans[i]))
    if M < m:
        m = M
        s = ""
        for i in ans:
            s += chr(i)
        print(s)


c = [0, 0, 0, 0]
for c[0] in charset:
    for c[1] in charset:
        for c[2] in charset:
            for c[3] in charset:
                check(c)
```

#### *Flag 3

​		根据提示，学习了 Mathematica 的 LatticeReduce 用法，直接调用即可：

```python
from decimal import *

primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]

result = '25800.3598436223754823177417650924231087407497040765066743916372206012564800767938337252665964911456534692346386812142791422663846274987022925198645625492302223476901845756519858676695489919379881'

# len(flag) = 58
n = 58
p = primes[:n]
matrix = []

base = 10 ** 190
getcontext().prec = 200

v = [round(Decimal(p).sqrt() * base) for p in primes]

print('{',end='')
for i in range(n + 1):
    print('{', end='')
    for j in range(n + 1):
        print(1 if i == j else 0, end=',')
    if (i == n):
        print(-round(Decimal(result) * base), end='}}',sep='')
    else:
        print(-v[i], end='},',sep='')
```

```mathematica
In[1] := a = {{...}}
Out[1] := {{...}}
In[2] := LatticeReduce[a]
Out[2] := {{...}, {{-102, -108, -97, -103, -123, -119, -104, -97, -116, -95, -97, -95, \
-49, -101, -110, -115, -116, -114, -97, -45, -49, -101, -110, -115,	\
-116, -114, -97, -45, -49, -111, -118, -97, -115, -122, -125, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, \
-187}}}
```

​		还原即得 flag。
