# [Binary] 次世代立方计算机

- 命题人：MaxXing
- 题目分值：400 分

## 题目描述

<p>“这是什么？一个 JAR 包？你确定没搞错吗？”</p>
<p>“你不能质疑我<ruby>超级嗨客<rt>スーパーハカー</rt></ruby>的实力，他们的服务器上确实只有这一个可疑的文件。”</p>
<p>“那这就是传说中的‘次世代立方计算机’咯？”</p>
<p>“确切地说，根据服务器里的其他文档，这是这个计算机的 RTL 描述。”</p>
<p>“真不敢想象，这么个文件，居然能描述一个……可以用来构建元宇宙的计算机。”</p>
<p>“我超！元……宇宙？！这也太酷了！很符合我对……”</p>
<p>“行了行了，说正经的，这玩意要怎么用呢？”</p>
<p>“我不道哇。是不是得想办法把它运行起来，然后里面会输出什么东西之类的吧？”</p>
<p>“不可能这么简单，我觉得里面肯定用了什么<strong>加密手段</strong>和<strong>编码手段</strong>。”</p>
<p>“确实，毕竟是 THERN。”</p>
<p>“是啊，全球顶尖的组织，世界最高的机密，你觉得我们的胜算有几成？”</p>
<p><strong>“无所谓，我会出手。”</strong></p>
<p>补充说明：</p>
<ul>
<li>Cube64 计算机某些内部状态的初始值可能会影响其输出。</li>
<li>Cube64 输出的内容使用 base64 解码后即可得到 Flag。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>如果无法理解 Scala 里各种抽象的语法，你可以尝试运行 JAR 包，检查生成的 FIR（FIRRTL）文件，其语法相对更好理解。</li>
<li>你不仅需要分析 Cube64 的 RTL 描述，还需要分析 ROM 中的程序，最好能用其他编程语言写一个等价的程序。</li>
<li>程序从内存读取输入，且只会在输入正确的情况下，输出一个合法的 flag（base64 解码后以 <code>flag{</code> 开头），所以你可能需要枚举所有输入。</li>
</ul>
</div>

**[【附件：下载题目程序（prob20-Cube64.jar）】](attachment/prob20-Cube64.jar)**

**[【附件：下载题目源码（prob20-src.zip）】](attachment/prob20-src.zip)**

## 预期解法

由于题目提供了源码, 我们可以直接看源码: 很明显, 这个项目是用 Scala 写的 (因为源代码后缀为 `.scala`).

同时, 题目中提到这是 “次世代立方计算机” 的 RTL 描述. 在网络上搜索 “Scala RTL”, 我们不难找到一个名为 “Chisel” 的硬件设计语言——确切地说是基于 Scala 构建的 DSL. 在项目的构建配置中, 我们也可以找到相关的依赖:

```scala
libraryDependencies ++= Seq(
  "edu.berkeley.cs" %% "chisel3" % chiselVersion,
  "edu.berkeley.cs" %% "chiseltest" % "0.5.1" % "test"
),
```

所以, 要想理解这个项目是如何工作的, 你必须首先理解如何用 Chisel 描述电路. 当然, 你可能还需要对数字电路的相关概念有一定的了解. 此处略过枯燥的教学环节 (可参考 [Scala 的文档](https://docs.scala-lang.org), [Chisel 的文档](https://www.chisel-lang.org/chisel3/docs/introduction.html), CSAPP 第四章, 数字电路教材等), 直接开始分析实现.

首先看项目的顶层模块, 即 `src/main/scala/cube64/Cube64.scala`, 其中定义了 Cube64, 也就是所谓 “次世代立方计算机”, 的顶层描述. 这部分实例化了几个模块:

* `Rom`: 看名称, 这是 Cube64 的 ROM, 即保存程序的地方, 看代码也确实如此. 程序的二进制内容位于 `src/main/resources/rom.bin`.
* `Ram`: Cube64 的 RAM.
* `Core`: 看起来是 Cube64 的核心部分.

ROM 和 RAM 只是两个普通的存储器, 所以我们接下来看看 `Core` 模块的组成:

* `Core.scala:22-27`: 状态机 (FSM) 的控制逻辑, 在 “取指” (fetch), “译码” (decode), “执行” (execute) 三个状态之间来回切换.
* `Core.scala:29-30`: 实例化堆栈 (`Stack`).
* `Core.scala:32-35`: 实例化取指 (`Fetch`) 模块, 连接必要的 IO 信号.
* `Core.scala:37-42`: 实例化译码 (`Decode`) 模块, 连接必要的 IO 信号.
* `Core.scala:44-59`: 实例化执行 (`Execute`) 模块, 连接必要的 IO 信号.
* `Core.scala:61-70`: 处理其他的 IO 信号.

看样子 Cube64 的核心部分是一个经典的多周期处理器, 一条指令经由 `Fetch`, `Decode` 和 `Execute` 模块的处理, 最终完成执行. 同时它是一个栈机而非寄存器机, 因为核心部分里用来保存相关状态的只有一个堆栈.

接下来分析 `Fetch` 模块. 注意到其中计算 ROM 地址的逻辑:

```scala
// position
val (x, nextX) = pos(-1.S(posWidth.W).asUInt, Direction.XP, Direction.XN)
val (y, nextY) = pos(0.U(posWidth.W), Direction.YP, Direction.YN)
val (z, nextZ) = pos(0.U(posWidth.W), Direction.ZP, Direction.ZN)
def pos(init: UInt, dirPos: UInt, dirNeg: UInt) = {
  val p = RegInit(init)
  val next =
    Mux(nextDir === dirPos, p + 1.U,
    Mux(nextDir === dirNeg, p - 1.U, p))
  when (io.en) { p := next }
  (p, next)
}

// fetch the current instruction from the ROM
val pc = Cat(nextZ, nextY, nextX)
io.rom.addr := pc
```

模块中 `dir` 寄存器保存了 `Direction`, 即 “方向”. 之后的地址计算逻辑会根据当前方向, 增加或者减少 `x`, `y`, `z` 三个地址分量的值. 最后, ROM 的地址由 `z`, `y`, `x` 三个分量按顺序拼接而成.

这是什么意思呢? 如果我们把 `x`, `y`, `z` 理解成三维坐标系里的 $(x, y, z)$, 一切就说得通了:

* Cube64 的 ROM 是 $16 \times 16 \times 16$ 的一个三维空间.
* 初始化之后, `Fetch` 从坐标 $(0, 0, 0)$ 处开始取指.
* 下一次取指时, 坐标会按照当前的方向变化, 方向分为 x/y/z 轴正方向/负方向 六种. 初始化之后, 坐标会按照 “x 轴正方向” 的方向发生变化, 即每次 x 坐标加 1.
* 所有控制转移指令, 包括分支和跳转, 都只会改变当前的执行方向. 比如把 “x 轴正方向” 改为 “y 轴负方向”, 这样更新坐标时, x 分量将不变, 同时 y 分量减一.
* ROM 实际上只是一个线性地址空间的存储器, 所以 `Fetch` 向 ROM 发送的地址实际上是 $16^2z + 16y + x$.

这也是为什么这道题叫做 “次世代立方计算机”.

接下来看 `Decode` 模块. 这个模块借助 `Instructions` object 中定义的译码表完成了指令译码:

```scala
// control signals
val (stackOp :: opr1 :: opr2 :: aluOp :: ctOp :: lsuOp ::
  (hasResult: Bool) :: (out: Bool) :: (halt: Bool) :: Nil) =
  ListLookup(io.inst, Instructions.DEFAULT, Instructions.TABLE)
```

之后按照译码结果从堆栈读取操作数, 更新堆栈状态, 以及计算控制转移指令指定的方向.

作为一个栈机, Cube64 指令的所有操作数都来自堆栈, 同时结果也会写回堆栈. 接触过 JVM, WASM 等栈机的同学们对此一定不陌生.

最后, `Execute` 模块完整了实际的运算操作, 例如计算加减法, 计算位运算, 访存等等, 之后将结果写回堆栈, 其中的细节不再赘述.

看一眼刚刚在 `Decode` 模块中出现的译码表, 其中列举了每条指令的编码, 甚至贴心地把指令名字都给出来了:

```scala
// patterns
val NOP = BitPat("b0000000")
val DUP = BitPat("b0000001")
val SWAP = BitPat("b0000010")
val LD = BitPat("b0000011")
val ST = BitPat("b0000100")
...
```

按照这些逻辑, 我们可以写出一个反汇编器, 见 [`src/disassembler.py`](src/disassembler.py). 简单处理一下 `rom.bin` 中的指令, 我们可以发现, Cube64 执行了 64 次以下的操作:

```
dup     # 栈顶的数字最开始是 0
li 3
and
dup
ld
li 61   # 这个数字在各次操作中会发生变化
xor
out
dup
ld
dup
li 63
st
swap
li 62
st
li 3
and
dup
ld
li 62
ld
st
li 63
ld
swap
st
inc     # 栈顶的数字此时加一
```

翻译成 Python 代码如下:

```py
magic_numbers = [
    61, 31, 20, 15, 61, 18, 3, 10,
    40, 47, 27, 16, 63, 35, 43, 13,
    40, 12, 19, 17, 62, 35, 59, 38,
    53, 45, 47, 23, 57, 35, 15, 38,
    57, 15, 11, 17, 62, 32, 19, 56,
    51, 13, 35, 16, 60, 3, 58, 15,
    41, 60, 19, 6, 63, 34, 59, 10,
    41, 15, 59, 23, 44, 55, 43, 4,
]

def get_output(mem):
  out = []
  for i in range(64):
    k = i & 3
    out.append(mem[k] ^ magic_numbers[i])
    # 这里其实还用到了 mem[62] 和 mem[63] 两块内存,
    # 但程序并未直接读取这两块内存的值,
    # 只是借助内存完成了数据交换.
    temp = mem[k]
    mem[k] = mem[temp & 3]
    mem[temp & 3] = temp
  return out
```

这部分似乎对应了题目中提到的 “加密手段”: 一些 magic number, 和内存中 0-3 四个地址处读取到的数字, 经过一通异或, 得出了一串新的数字.

但是这串数字有什么用呢? 题目中还提到了 “编码手段”, 结合 `Cube64` 模块的代码: 模块输出的整数长度只有 6 位, 我们可以联想到 base64 这种编码方式, 也就是说, 把输出的证书序列翻译成 base64 编码后的字符串, 然后对其进行解码, 即可得到 flag. *当然此步骤有点过于脑洞, 可能导致出题人被远程殴打, 于是后期我们给题目增加了部分补充说明.*

然而还有一个问题: `mem[k]` 的值是多少? 根据常识, 程序在读取内存之前必须对其初始化, 否则读出的可能是垃圾数据. 但是 ROM 所示的程序中, 在读取 `mem[0]` 到 `mem[3]` 之前, 程序并未对内存进行任何初始化操作, 虽然 Chisel Tester 会在仿真时将内存的值视为 0.

假设整块内存的值为 0, 尝试运行程序并解码输出, 我们会得到一串乱码, 看起来不太对. 尝试更改内存地址 0-3 处的值, 我们发现程序的输出会发生变化. 因此, 不妨尝试把所有可能的值都穷举一遍:

```py
def b64_int_to_ascii(c):
  # 把数字转换成 base64 字符, 实现略
  return ...

for m0 in range(64):
  for m1 in range(64):
    for m2 in range(64):
      for m3 in range(64):
        out = get_output([m0, m1, m2, m3])
        s = bytes(map(b64_int_to_ascii, out)).decode()
        if s.startswith('ZmxhZ3'):
          print(b64decode(s).decode())
```

最终可得 flag.

## 相关实现

参考 [`src` 目录](src), 附:

* 题目核心算法原型 (一个劣化版 RC4).
* Scala 源代码.
* 汇编器.
* 反汇编器.
* 解释器.
* Verilator 仿真验证程序.

## 花絮

1. ~~该题是对 DEF CON CTF 2020 [fountain-ooo-reliving](https://archive.ooo/c/fountain-ooo-reliving/332/) 的拙劣模仿.~~
2. Flag 里提到 “Simulate the Earth with A Cube64 cluster”, neta “PS3 模拟地球”.

我承认这个题出得比较孬, 主要在于有些步骤太脑洞了. 在被某位选手远程殴打之后, 我不得不在 “被所有做这道题的选手远程殴打” 和 “只被寥寥几位幸 (bu) 运 (xing) 选手远程殴打” 这两个选项中做出艰难抉择, 最后还是决定放出一些补充说明以避免大家走过多弯路 (逃

以及, 这个题最开始的时候是不提供源代码下载的, 只有一个 JAR 包, 本意是想让大家看 Chisel 电路生成的 FIRRTL. 后来由于种种原因, [@xmcp](https://github.com/xmcp) 把这个题挪到了 Misc 分类下, 此时考虑到:

1. 作为一道 Misc, 此题不应该给大家过多的逆向压力.
2. Scala 生成的 JAR 包逆出来的东西实在是太恶心了.

于是我们提供了源代码下载.

当然再后来这道题又被放回了 Binary 分类下, 避免了出题人遭受更进一步的远程殴打.
