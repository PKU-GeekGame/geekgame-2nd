# [Misc] Flag Checker

- 命题人：debugger
- Flag 1：150 分
- Flag 2：150 分

## 题目描述

<p>我们发现，有很多选手在比赛中提交了错误的 Flag。</p>
<p>为了防止这种情况发生，给选手良好的参赛体验，这里有一个简单的 Java 程序。</p>
<p>你可以在程序里面输入要提交 Flag ，程序会帮你检查 Flag 是否正确。</p>
<p>是不是非常的贴心呢？</p>
<p><strong>提醒：JRE 版本高于 15 时可能无法运行此程序。建议使用 JRE 8 运行。</strong></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>有众多工具可以反编译Java程序（包括一些IDE也有反编译功能）。不像C或C++，反编译产生的Java通常都非常接近原始Java代码。</li>
<li>JavaScript可以直接复制到浏览器开发者工具进行调试。</li>
</ul>
</div>

**[【附件：下载题目附件（prob15.jar）】](attachment/prob15.jar)**

## 预期解法

如果你的机器装了IntelliJ IDEA，可以直接打开.class文件，里面内置了一个FernFlower decompiler。如果你没装任何Java IDE，你也可以用[Java decompiler online](http://www.javadecompilers.com/)反编译Java程序。下文的代码都是FernFlower decompiler产生的。

可以发现Check Flag 1和Check Flag 2这两个按钮对应的对象分别是button1和button2。首先看Flag 1的检测逻辑：
```java
            if (var1.getSource() == this.button1) {
                byte[] var2 = this.textField1.getText().getBytes("UTF-8");
                String var7 = rot13(Base64.getEncoder().encodeToString(var2));
                if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(var7)) {
                    JOptionPane.showMessageDialog((Component)null, "Correct");
                } else {
                    JOptionPane.showMessageDialog((Component)null, "Wrong");
                }
            }
```

可以发现rot13函数是可逆的，因此用以下代码即可恢复flag：
```java
import java.util.Base64;
public class Main {
    public static void main(String args[]) {
      System.out.println(new String(Base64.getDecoder().decode(rot13("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4"))));
    }

    static String rot13(String var0) {
        StringBuilder var1 = new StringBuilder();

        for(int var2 = 0; var2 < var0.length(); ++var2) {
            char var3 = var0.charAt(var2);
            if (var3 >= 'a' && var3 <= 'm') {
                var3 = (char)(var3 + 13);
            } else if (var3 >= 'A' && var3 <= 'M') {
                var3 = (char)(var3 + 13);
            } else if (var3 >= 'n' && var3 <= 'z') {
                var3 = (char)(var3 - 13);
            } else if (var3 >= 'N' && var3 <= 'Z') {
                var3 = (char)(var3 - 13);
            } else if (var3 >= '5' && var3 <= '9') {
                var3 = (char)(var3 - 5);
            } else if (var3 >= '0' && var3 <= '4') {
                var3 = (char)(var3 + 5);
            }

            var1.append(var3);
        }

        return var1.toString();
    }
}
```

再看Flag 2。函数首先处理了一段字符串，然后以处理的结果调用eval函数。先看看处理的结果是什么：
```java
public class Main {
    public static void main(String args[]) {
        String var4 = "\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ï\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088ÝÇ°ß\u0097\u008e×Ü\u008a\u0097ÝÆ\u0094\u0099\u008e\u009dÏ°ß\u0097ØÝÛ\u008dÒ´È\u008c\u0087\u008e\u009d¬\u0080\u008b\u008a®\u009bÈÃÈ\u0082\u008e\u009fÈÃÈÈÃÈ\u009c\u009f\u0083\u0086\u009bÈÃÈ\u009c\u009b\u009d\u0086\u0081\u0088\u0086\u0089\u0096ÈÃÈ¬\u0080\u009d\u009d\u008a\u008c\u009bÈÃÈ¸\u009d\u0080\u0081\u0088ÈÃÈ\u0085ÂÈ²Ô\u009d\u008a\u009b\u009a\u009d\u0081ÏÇ¥¼ ¡´°ß\u0097ØÝÛ\u008d´Û²²Ç°ß\u0097\u008e×Ü\u008a\u0097Ý´°ß\u0097ØÝÛ\u008d´Ü²²Ç°ß\u0097ØÝÛ\u008d´Ý²Æ´°ß\u0097ØÝÛ\u008d´Þ²²Ç\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0094\u009d\u008a\u009b\u009a\u009d\u0081Ï°ß\u0097\u008e×Ü\u008a\u0097Ü´°ß\u0097ØÝÛ\u008d´ß²²ÇßÆ\u0092ÆÆÒÒÏ¥¼ ¡´°ß\u0097ØÝÛ\u008d´Û²²Ç´ßÃÞÚÃÞÙÃÞØÃÜßÃÞßÚÃÞÙÃÜÞÃÞÙÃÙØÃÜÃÜÜÃÚÃÙßÃÛÃÞßÙÃÙÃÛÞÃßÃÞÃÙØÃÜÃÞÙÃÛÃÙÃÜÜÃÝÜÝ²´°ß\u0097ØÝÛ\u008d´Þ²²Ç\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0094\u009d\u008a\u009b\u009a\u009d\u0081ÏÇ\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088ÝÄÏ°ß\u0097ØÝÛ\u008d´Ý²Æ´°ß\u0097ØÝÛ\u008d´ß²²Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0092ÆÆÐ°ß\u0097ØÝÛ\u008d´Ú²Õ°ß\u0097ØÝÛ\u008d´Ù²Æ\u0092";
        StringBuilder var8 = new StringBuilder();

        for(int var9 = 0; var9 < var4.length(); ++var9) {
            var8.append((char)(var4.charAt(var9) ^ 239));
        }

        System.out.println(var8.toString());
    }
}
```

运行结果是：
```javascript
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}
```

这是一段被混淆的JavaScript代码。对于常见的混淆代码，可以用<https://deobfuscate.io/>这个工具去混淆。结果是：
```javascript
function checkflag2(leycester) {
  var green = ["charCodeAt", "map", "", "split", "stringify", "Correct", "Wrong", "j-"];
  return JSON.stringify(leycester.split("").map(function (jolin) {
    return jolin.charCodeAt(0);
  })) == JSON.stringify([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function (makeeba) {
    return (checkflag2 + "").charCodeAt(makeeba);
  })) ? "Correct" : "Wrong";
}
```

这个函数会读取输入flag的每个字符，转成ASCII码，再和一个数组进行比较。需要注意的是，如果你用了去混淆后的代码计算目标数组，会得到错误的结果。这是因为checkflag2 + ""返回的是checkflag2的代码，这里需要使用原始的代码而不是去混淆后的代码。把以下代码复制到浏览器控制台或者Node的REPL，就能得到Flag 2。

```javascript
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])} 
String.fromCharCode(...[0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function (makeeba) {
    return (checkflag2 + "").charCodeAt(makeeba);
}))
```

### 附注

Java 15不再内置Nashorn引擎，所以此程序只能在较低版本的Java运行。

Flag 2的命题思路来自[Google CTF 2022的Js Safe 4.0一题](https://kitctf.de/writeups/jssafe)，该题目有个更复杂的把自身代码作为数据的例子。

本题的早期版本（见old/GeekGame.jar）有3个flag，其中本来Flag 1和Flag 2只是铺垫，真正的挑战是Flag 3（Flag 3是Crypto+Reverse，显著难于前两个Flag）；题目分类曾经在binary、algorithm（有Flag 3时）和misc之间多次移动，后来把因为题目类型不再是algorithm所以把Flag 3删除了。代码里面还没删除干净，有选手的wp里面说发现了没有定义的checkflag3函数。
