# 编原译理习题课

## 玩挺大

开一个很大的静态数组即可。但要注意不能开太大，估计是服务器端资源限制，太大了会编译不出来。

```c
#include <stdio.h>
static const int huge[1 << 21] = {0};
int main() {
  puts("Hello, world!");
  return 0;
}
```

## 玩挺长

利用 `__FILE__` 递归引用，编译器就会生成一个很长的报错信息。

```c
#include __FILE__
#include __FILE__
#include __FILE__
```

## 玩挺花

搜索 `g++ crash` 找到这个[网页](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54080)。

下面的代码会让 `g++` 崩溃。

```cpp
template <class T> class vector {};

template <template <typename U> class Container, typename Func>
vector<int> foo(const Container<int> &input, const Func &func) {}

template <template <typename U> class OutType, typename Func1,
          typename FuncRest>
auto foo(const vector<int> &input, const Func1 &func1, const FuncRest funcrest)
    -> decltype(foo<vector>(foo(input, func1), funcrest)) {
  return;
}

int main() {
  vector<int> v1;
  foo<vector>(v1, 1, 1);
}
```
