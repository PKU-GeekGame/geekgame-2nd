# Flag Checker

## Flag 1

使用 [`CFR`](https://www.benf.org/other/cfr/) 反编译得到

```java
/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Button;
import java.awt.Frame;
import java.awt.Label;
import java.awt.TextField;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Base64;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.swing.BoxLayout;
import javax.swing.JOptionPane;

public class GeekGame
extends Frame
implements ActionListener {
    TextField textField1;
    Button button1;
    Button button2;
    Invocable invocable;

    GeekGame() {
        this.setSize(300, 300);
        this.setVisible(true);
        this.setLayout(new BoxLayout(this, 1));
        Label label = new Label("Flag: ");
        this.textField1 = new TextField("flag{...}");
        this.button1 = new Button("Check Flag 1");
        this.button1.addActionListener(this);
        this.button2 = new Button("Check Flag 2");
        this.button2.addActionListener(this);
        this.add(label);
        this.add(this.textField1);
        this.add(this.button1);
        this.add(this.button2);
        ScriptEngineManager scriptEngineManager = new ScriptEngineManager();
        ScriptEngine scriptEngine = scriptEngineManager.getEngineByName("nashorn");
        try {
            String string = "\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00cf\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088\u00dd\u00c7\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dd\u00c6\u0094\u0099\u008e\u009d\u00cf\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00d2\u00b4\u00c8\u008c\u0087\u008e\u009d\u00ac\u0080\u008b\u008a\u00ae\u009b\u00c8\u00c3\u00c8\u0082\u008e\u009f\u00c8\u00c3\u00c8\u00c8\u00c3\u00c8\u009c\u009f\u0083\u0086\u009b\u00c8\u00c3\u00c8\u009c\u009b\u009d\u0086\u0081\u0088\u0086\u0089\u0096\u00c8\u00c3\u00c8\u00ac\u0080\u009d\u009d\u008a\u008c\u009b\u00c8\u00c3\u00c8\u00b8\u009d\u0080\u0081\u0088\u00c8\u00c3\u00c8\u0085\u00c2\u00c8\u00b2\u00d4\u009d\u008a\u009b\u009a\u009d\u0081\u00cf\u00c7\u00a5\u00bc\u00a0\u00a1\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00db\u00b2\u00b2\u00c7\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dd\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00dc\u00b2\u00b2\u00c7\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00dd\u00b2\u00c6\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00de\u00b2\u00b2\u00c7\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00c7\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0094\u009d\u008a\u009b\u009a\u009d\u0081\u00cf\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00df\u00b2\u00b2\u00c7\u00df\u00c6\u0092\u00c6\u00c6\u00d2\u00d2\u00cf\u00a5\u00bc\u00a0\u00a1\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00db\u00b2\u00b2\u00c7\u00b4\u00df\u00c3\u00de\u00da\u00c3\u00de\u00d9\u00c3\u00de\u00d8\u00c3\u00dc\u00df\u00c3\u00de\u00df\u00da\u00c3\u00de\u00d9\u00c3\u00dc\u00de\u00c3\u00de\u00d9\u00c3\u00d9\u00d8\u00c3\u00dc\u00c3\u00dc\u00dc\u00c3\u00da\u00c3\u00d9\u00df\u00c3\u00db\u00c3\u00de\u00df\u00d9\u00c3\u00d9\u00c3\u00db\u00de\u00c3\u00df\u00c3\u00de\u00c3\u00d9\u00d8\u00c3\u00dc\u00c3\u00de\u00d9\u00c3\u00db\u00c3\u00d9\u00c3\u00dc\u00dc\u00c3\u00dd\u00dc\u00dd\u00b2\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00de\u00b2\u00b2\u00c7\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00c7\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0094\u009d\u008a\u009b\u009a\u009d\u0081\u00cf\u00c7\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088\u00dd\u00c4\u00cf\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00dd\u00b2\u00c6\u00b4\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00df\u00b2\u00b2\u00c7\u00b0\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0092\u00c6\u00c6\u00d0\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00da\u00b2\u00d5\u00b0\u00df\u0097\u00d8\u00dd\u00db\u008d\u00b4\u00d9\u00b2\u00c6\u0092";
            StringBuilder stringBuilder = new StringBuilder();
            for (int i = 0; i < string.length(); ++i) {
                stringBuilder.append((char)(string.charAt(i) ^ 0xEF));
            }
            scriptEngine.eval(stringBuilder.toString());
        }
        catch (Exception exception) {
            StringWriter stringWriter = new StringWriter();
            PrintWriter printWriter = new PrintWriter(stringWriter);
            exception.printStackTrace(printWriter);
            JOptionPane.showMessageDialog(null, stringWriter.toString());
        }
        this.invocable = (Invocable)((Object)scriptEngine);
        this.addWindowListener(new WindowAdapter(){

            @Override
            public void windowClosing(WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
        try {
            if (actionEvent.getSource() == this.button1) {
                byte[] byArray = this.textField1.getText().getBytes("UTF-8");
                String string = GeekGame.rot13(Base64.getEncoder().encodeToString(byArray));
                if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(string)) {
                    JOptionPane.showMessageDialog(null, "Correct");
                } else {
                    JOptionPane.showMessageDialog(null, "Wrong");
                }
            } else {
                Object object = this.invocable.invokeFunction(actionEvent.getSource() == this.button2 ? "checkflag2" : "checkflag3", this.textField1.getText());
                JOptionPane.showMessageDialog(null, (String)object);
            }
        }
        catch (Exception exception) {
            StringWriter stringWriter = new StringWriter();
            PrintWriter printWriter = new PrintWriter(stringWriter);
            exception.printStackTrace(printWriter);
            JOptionPane.showMessageDialog(null, stringWriter.toString());
        }
    }

    static String rot13(String string) {
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < string.length(); ++i) {
            char c = string.charAt(i);
            if (c >= 'a' && c <= 'm') {
                c = (char)(c + 13);
            } else if (c >= 'A' && c <= 'M') {
                c = (char)(c + 13);
            } else if (c >= 'n' && c <= 'z') {
                c = (char)(c - 13);
            } else if (c >= 'N' && c <= 'Z') {
                c = (char)(c - 13);
            } else if (c >= '5' && c <= '9') {
                c = (char)(c - 5);
            } else if (c >= '0' && c <= '4') {
                c = (char)(c + 5);
            }
            stringBuilder.append(c);
        }
        return stringBuilder.toString();
    }

    public static void main(String[] stringArray) {
        GeekGame geekGame = new GeekGame();
    }
}
```

阅读源码发现 Flag 1 经过 `Base64` 编码后再 `rot13` 的结果为 `MzkuM8gmZJ6jZJHgnaMuqy4lMKM4`，逆操作即可得到 Flag 1。

## Flag 2

把 Java 代码里那一长串字符串打印出来，发现是一段混淆过的 JavaScript 代码：

```javascript
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}
```

手工做一些变量替换，就可以把代码还原成：

```javascript
function checkflag2(input) {
    var codes = ['charCodeAt', 'map', '', 'split', 'stringify', 'Correct', 'Wrong', 'j-'];
    return JSON.stringify(
        input.split('').map(function (x) { return x.charCodeAt(0) })) == JSON.stringify([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function (x) { return str.charCodeAt(x) })) ? 'Correct' : 'Wrong'
}
```

其中 `str` 就是原本那段混淆了的代码。这样就可以很简单地还原出 Flag 2：

```javascript
console.log(String.fromCharCode(...[0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function (x) { return str.charCodeAt(x) })))
```
