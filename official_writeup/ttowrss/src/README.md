# TTOWRSS 相关实现

> By MaxXing.

某天刷知乎的时候看到了[这个回答](https://www.zhihu.com/question/46773069/answer/463741166):

> 具体的各种争夺手法差不多可以写本书了，这里就举一个有趣的加密手法：
>
> 利用int3让内存里的程序倒序执行。或者说倒序才是正确的打开方式。
>
> 本来第n条指令执行完毕之后应该执行第n+1条指令，加密程序利用int3在执行完第n条指令之后，把命令指针改成n-1，从而实现倒序执行。
>
> 静态分析，内存里的代码简直狗屁不通。
>
> 动态跟踪你就得去截int3。可你一篡改int3，程序就没法倒序执行了，结果就更是狗屁不通了，从而达成防止破解的目的。

觉得很有意思, 刚好当时在筹备下一届 GeekGame, 于是决定把这个思路出成一道逆向, 虽然我自己完全不会逆向 (遗憾).

但让一个合法的 x86-64 程序倒序执行, 并不是一个简单的事情, 我们需要考虑很多问题, 包括:

* 如何让 `rip` 在跑完一条指令之后指向上一条指令, 而不是下一条?
* 如何处理分支, 跳转, 以及函数调用?
* 手写汇编也许可以实现这样的事情, 但如何把整个过程自动化?

好在思考了一段时间, 外加一通 STFW 之后, 我还是找到了一种可行的实现方法.

## 实现思路

### 倒序执行

如何倒序执行程序呢?

首先, 负责执行程序的是 CPU. 而据我所知, 世界上的绝大多数 CPU, 都只会按照 PC 递增方向执行代码 (控制转移指令除外), 同时也不提供更改代码执行方向的配置选项.

不过并不是说这个事是解决不了的, 或者说, 既然 CPU 本身没办法解决这个事, 我们也许可以换种思路:

1. 让 CPU 单步执行代码.
2. 使用软件接管单步执行的流程.
3. 在一次单步执行结束后, 修改 PC, 使其指向上一条指令而非下一条.
4. 继续单步执行.

好, 之前的问题解决了, 但我们又多出三个问题:

1. 如何让 CPU 单步执行代码?
2. 如何使用软件接管单步执行的流程?
3. 如何修改 PC 使其指向上一条指令?

我们的目标是写出一个倒着跑的 x86-64 程序, 而在 x86 上, CPU 恰好为我们提供了一种单步执行的机制: [trap flag](https://en.wikipedia.org/wiki/Trap_flag), 确切的说是 [`flags`/`eflags`/`rflags` 寄存器](https://en.wikipedia.org/wiki/FLAGS_register)的第 8 位.

在设置 trap flag 之后, CPU 会进入单步模式, 每执行一条指令触发一次异常, 之后进入异常处理程序. 而运行于 CPU 之上的操作系统, 会根据异常原因识别出这一行为, 并且通知当前执行的进程发生了 trap.

在 Linux (或者说 POSIX) 中, 这种通知机制由 [signal](https://en.wikipedia.org/wiki/Signal_(IPC)) 机制实现. 发生 trap 时, 程序会收到 [`SIGTRAP` 信号](https://en.wikipedia.org/wiki/Signal_(IPC)#Default_action). 如需自行处理该信号, 程序可注册对应的 signal handler.

不过, 一般情况下, `SIGTRAP` 会由调试器触发, 比如你正在单步调试. 此时程序内是没有任何 handler 处理这个信号的, 调试器会使用 [`ptrace`](https://en.wikipedia.org/wiki/Ptrace) 来处理被调试进程的 `SIGTRAP`.

所以, 为了实现 (至少是部分代码的) 倒序执行, 我们可以在程序启动后设置 `SIGTRAP` 的 handler, 然后设置 trap flag, 之后在 handler 中处理更新 PC 的逻辑.

那么, 如何在 handler 中, 将 PC 指向上一条指令呢?

仔细阅读 Linux 手册中和 signal 相关的部分, 例如 [`sigaction`](https://man7.org/linux/man-pages/man2/sigaction.2.html), 其中提到 signal handler 具备三个参数, 其中第三个参数, `ucontext` 的描述如下:

> `ucontext`
>
> This is a pointer to a `ucontext_t` structure, cast to `void *`.
>
> The structure pointed to by this field contains signal context information that was saved on the user-space stack by the kernel; for details, see [sigreturn(2)](https://man7.org/linux/man-pages/man2/sigreturn.2.html). Further information about the `ucontext_t` structure can be found in [getcontext(3)](https://man7.org/linux/man-pages/man3/getcontext.3.html) and [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html).
>
> Commonly, the handler function doesn't make any use of the third argument.

也就是说, 我们可以借助 `ucontext`, 修改由内核保存的, 和该进程相关的上下文 (context), 其中自然包括了所有寄存器的值. 在 x86-64 中, 我们只需要修改 `rip` (instruction pointer) 寄存器, 即可控制程序的 PC, 很简单吧!

然而, 上帝这个 byd 在为你打开一扇窗之后, 就必然会关闭一扇门. 在 x86-64 下, 我们还需要考虑另一个问题: 作为古老的 [CISC](https://en.wikipedia.org/wiki/Complex_instruction_set_computer) 架构, x86-64 的指令是变长的, 我们没办法简单地通过 “将 `rip` 的值减去固定数值” 的方式, 让程序倒序执行. 更蛋疼的是, x86-64 的指令编码是一种[前缀码](https://en.wikipedia.org/wiki/Prefix_code), 你只能通过从前往后扫描来确定指令的边界, 从后往前扫是不行的.

也许这个问题有很多种解决方式, 比如往程序里嗯塞一个 x86-64 decoder (如 [iced](https://github.com/icedland/iced)), 或者利用 CPU 来帮我们完成一部分译码的任务 (其实我没想好这样要怎么搞). 但在权衡实现的复杂性之后, 我还是决定用一种非常简单的方式来解决这个问题: **打表**.

当然, 为了进一步简化实现, 缩小程序的体积, 我们可以把这个表压缩成位图 (bitmap): 也就是说, 指定一串数据, 其中的每一位对应程序代码段的每一个字节. 如果某个字节是某条指令的开头, 就将位图里对应位设为 1, 否则设为 0. 这个位图可以提前用其他方式生成, 然后嵌入到程序中.

在需要更新 `rip` 的时候, 我们可以根据 `rip` 目前的值, 找到位图中的对应位. 需要注意的是, 在设置 trap flag 的情况下, CPU 执行完一条指令之后, 会将 `rip` 指向下一条指令, 然后再触发异常, 进入 handler. 所以我们需要在位图中找到 `rip` 对应指令之前第二条指令的开头, 并将 `rip` 设为对应的地址.

### 处理控制流

经过一通折腾, 我们终于找到了一种可行的方法, 将整个顺序执行的指令流变成倒序执行. 不过, 现实世界的程序中, 几乎不可能只有顺序执行这一种情况, 还会出现分支, 跳转, 函数调用/返回等各类控制流转移的情况. 怎么处理这类情况呢?

其实我们刚刚提出的处理方式已经可以完全兼容控制流了, 只需要做出一些小小的改动. 考虑以下情况:

```
  inst1
  inst2
  jump label1
  inst3
  inst4
label1:
  inst5
  inst6
```

如果我们把它简单地连 label 一起倒过来:

```
  inst6
  inst5
label1:
  inst4
  inst3
  jump label1
  inst2
  inst1
```

然后按照我们刚刚的思路, 从 `inst1` 开始倒序执行, 你会发现: 执行完 `jump` 之后, `rip` 会指向 `inst4`. 接着进入 handler, handler 会将 `rip` 前移两条指令, 也就是指向 `inst6`, 然后开始执行.

但程序原本的执行流程应该是, 遇到 `jump` 之后, 接着从 `inst5` 开始执行. 为了实现这样的效果, 我们只需要把 label 往后挪一个指令:

```
  inst6
  inst5
  inst4
label1:
  inst3
  jump label1
  inst2
  inst1
```

这样, 倒序执行时的执行流就和顺序时完全一致了. 这种处理方式对于分支, 函数调用等等其他控制流指令也同理. 不过需要注意以下的情况:

```
func:
  inst1
  inst2
  inst3
  call func
```

倒过来之后, 我们需要往开头 (或者说结尾) 加两条别的指令, 然后才能把 `func` label 挪下去:

```
  call func
  inst3
  inst2
  inst1
  nop
func:
  nop
```

当然如果没出错, 这两条指令永远都不会被执行到, 所以其实把它们换成任何指令都是可以的.

### 自动化

首先, 很显然, 人肉写汇编的话, 按照上面我们讨论的思路手搓一个倒序执行的程序, 是完全可行的.

然而, 作为一个能写脚本就决不躬亲的极致懒狗, 让我手搓还不如把我扬了——而且这样一点也不酷. 跑个自动化脚本, 啪的一下, 很快啊, 你写的源代码直接就变成一个倒着执行的二进制了, 这才符合我对计算机的想象, 科技并带着趣味.

所以我是怎么实现自动化的呢? 首先我决定用 C 来编写这样的程序——其实用什么语言无所谓了, 不过 C 会省心很多. 我将前文提到的若干内容封装成了头文件, 包括:

* 设置 trap flag 和 signal handler 的代码.
* signal handler 本体, 包含 bitmap 的扫描和 `rip` 的更新操作.
* 预留出来的用来存放 bitmap 的空位, 稍后会用其他方式替换掉二进制里的 bitmap.
* 其他必要的判断逻辑. 例如我们只能倒序执行程序里的代码, 而不能倒序执行 shared library. 为了判断目前是否需要开启倒序执行, handler 会判断 `rip` 的值是否落在了代码段内, 这就要求程序必须获知代码段的起始和结束地址. 我们可以通过修改链接器脚本 (linker script) 来实现这一操作.

任何需要倒序执行的程序, 只需 include 上述头文件即可, 非常省事.

接下来是负责把程序生成的机器指令倒过来的部分, 这部分我选择用以下方法实现:

1. 首先 `gcc -S` 输出 C 程序对应的汇编.
2. 然后写个脚本, 按照前文提到的逻辑把汇编倒过来, 同时修改所有 label 的位置.
3. 指定使用修改过的链接器脚本链接这个汇编程序, 以便 C 里判断代码段范围的逻辑生效.

最后, 我们需要生成 bitmap, 然后将其嵌入程序. 这里我偷个懒, 用 `objdump` 扫一遍刚刚得到的二进制, 然后用脚本简单解析一下输出, 生成一个 bitmap. 最后用 `readelf` 定位二进制内 bitmap 符号的偏移量, 把 bitmap 写到二进制文件即可.

## 相关工具及用法

**好消息: 我开源了刚刚提到的自动化脚本.**

如果你也像我一样闲, 希望搞一个能倒着跑的 x86-64 Linux 程序的话, 可以直接参考[这套实现](https://gist.github.com/MaxXSoft/f043eff08634d9ea4bb7296d35a3e73e). 具体来说, 你需要:

1. 下载 [`rev.h`](https://gist.github.com/MaxXSoft/f043eff08634d9ea4bb7296d35a3e73e#file-rev-h).
2. 写一个普通的 C 语言程序. 注意这个实现暂不支持多文件 (当然你感兴趣的话可以改改), 所以你必须把代码写在一个文件里.
3. 在程序的开头 include `rev.h`.
4. 下载 [`compile_rev.py`](https://gist.github.com/MaxXSoft/f043eff08634d9ea4bb7296d35a3e73e#file-compile_rev-py), 执行 `./compile_rev.py 你写的C文件` 编译程序.
5. 程序会保存在当前目录, 运行一下看看吧!

说实话这个脚本写的有点 tricky, 里面依赖了很多 `gcc`, `ld`, `objdump` 和 `readelf` 的特性. 而且, 我只测试了给 GeekGame 出题用的那个程序 (以及其他简单的例子), 对此这个脚本是可以正常工作的, 但我不保证对于其他的 C 程序, 这个脚本还能生成一个能跑的 ELF.

为了避免这个脚本在你的环境上崩溃, 我还提供了一个 [`Dockerfile`](https://gist.github.com/MaxXSoft/f043eff08634d9ea4bb7296d35a3e73e#file-dockerfile). 你可以执行 (请确保你的 CPU 是 x86-64 架构):

```
docker build -f Dockerfile路径 -t rev
```

然后在生成的镜像里跑这个脚本, 或者测试脚本生成的程序.

## 你可以用它做什么?

玩.
