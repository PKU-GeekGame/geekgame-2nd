// for flag1
// RUST issue: https://github.com/rust-lang/rust/issues/66658

#![forbid(unsafe_code)]
#![allow(unconditional_recursion)]
use std::ops::Deref;
#[derive(Debug)]
struct Outer<T: Deref<Target = Outer<T>>> {
    inner: T,
    foo: Vec<i32>,
}

impl<T: Deref<Target = Outer<T>>> Deref for Outer<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}
#[derive(Debug)]
struct Inner {
    bar: i32
}

impl Deref for Inner {
    type Target = Outer<Inner>;

    fn deref(&self) -> &Self::Target {
        //Look at which struct we're implementing Deref for,
        //and then read the next line very carefully.
        &self.inner
    }
}
pub fn run() {
    let i: Inner = Inner { bar: 0 };
    println!("{:?}", *i);
}
//EOF