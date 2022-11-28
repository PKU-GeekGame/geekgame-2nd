# 编译原理习题课

## 解题过程

### 玩挺大
太久不写 C/C++ 了一开始真没啥思路，所以直接去搜了。Google "Compiler bomb" 可以搜到一个 [Challenge](https://codegolf.stackexchange.com/questions/69189/build-a-compiler-bomb)。

其中一个答案是 `main[-1u]={1};`，理解了一会反应过来是直接开了个大数组。

~~~c
#define S 0xffffff
long t[S] = {1};

int main() {}
~~~

### 玩挺长
这个也可以搜。Google "g++ error message bomb" 可以找到这个链接：[Generate the longest error message in C++](https://codegolf.stackexchange.com/questions/1956/generate-the-longest-error-message-in-c)。

如下的解答确实输出了大量报错信息。虽然还不够，但也给出了思路：递归报错。
~~~c
#include __FILE__
p;
~~~

一次不够可以来两次，报错信息将变成指数级增长：
~~~c
#include __FILE__
#include __FILE__
A;
~~~
### 玩挺花
这个不得不搜。搜 Compiler bugs lead to segmentation fault，跟着各种链接可以找到 [GCC Bugzilla](https://gcc.gnu.org/bugzilla) 的链接。

没有找到特别好的搜索方法，在 c++ 相关的 bug 里试了不少，最后发现这段代码可以让目标 gcc crash：
~~~
template <auto... Methods>
struct Foo;
template <
    typename Class,
    typename... ReturnType, 
    ReturnType (Class::*...Methods)()>
struct Foo<Methods...> {
    constexpr void operator ()() { }
};
struct Bar {int baz() { return 42; }};
void tryOut() {Foo<&Bar::baz>{}();}
~~~


