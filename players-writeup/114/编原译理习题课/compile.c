//huge binary
//定义大量需要初始化的变量，让data段巨大
#define a 1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1
#define b a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
#define c b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b
#define d c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
#define e d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d
int main(){long long x[]={e};return x[10];}
//EOF

//lots of errors
//C++模板的恶心报错，加上递归include自身
template<class T>struct W{T v;W(T v):v(v){}};
template<class T>int f(T x){f(W<T>(x));}
int main(){
    int a;
    std::vector<std::vector<int>> v;
    std::find(v.begin(), v.end(), a);
    f(0);
};
#include __FILE__
//EOF

//gcc bug: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=107148
int f(int);
class A {
public:
  A(int);
};
class C {
  constexpr C() : m(f(({ int x = 1; x; }))) {}
  A m;
};
//EOF