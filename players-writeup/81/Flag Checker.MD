# Flag Checker

题面很清晰，出题代码也很易懂，属于容易一档的题目。

不过我在解jar包的过程中卡了一会，由于没做过java开发，不知道IDEA可以直接解jar包。网上找的好多工具解出来之后跟flag2有关的那处字符串就成了乱码。

此处感谢JetBrain家的一系列IDE，当我遇到不熟悉的语言配不好环境的时候，IDE总是能帮我一键处理。

### flag1

对题目代码的`rot13`函数求逆运算，先找到了几个rot13编解码的工具。
解码之后的结果似乎是一个`flag`开头，但不包含`{}`的字符串，
因此怀疑出题人对`rot13()`函数动了手脚，不是标准的rot13编码过程，只得根据encode代码写了decoder。文末附上代码。

### flag2

这个flag就是将代码中那串乱码解码成js，在`nashorn`引擎中运行，要注意的有两点：

1. 要保证jar包反编译的源码是正确的
2. `nashorn`引擎与`V8`引擎的运算结果不一致（大坑），因此需要在`nashorn`中运行以获得flag2

### 附件

decoder代码如下

```java
static String rot13_decode(String paramString) {
        StringBuilder stringBuilder = new StringBuilder();
        for (byte b = 0; b < paramString.length(); b++) {
            char c = paramString.charAt(b);

            if (c - 5 >= '0' && c - 5 <= '4') {
                c = (char) (c - 5);
            } else if (c + 5 >= '5' && c + 5 <= '9') {
                c = (char) (c + 5);
            } else if (c + 13 >= 'N' && c + 13 <= 'Z') {
                c = (char) (c + 13);
            } else if (c + 13 >= 'n' && c + 13 <= 'z') {
                c = (char) (c + 13);
            } else if (c - 13 >= 'A' && c - 13 <= 'M') {
                c = (char) (c - 13);
            } else if (c - 13 >= 'a' && c - 13 <= 'm') {
                c = (char) (c - 13);
            }
            stringBuilder.append(c);
        }
        return stringBuilder.toString();
    }
```
