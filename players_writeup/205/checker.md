# Flag Checker

## 解题过程
程序没有加壳，可以直接用在线工具进行反编译。


~~~java
if (actionEvent.getSource() == this.button1) {
    if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(rot13(Base64.getEncoder().encodeToString(this.textField1.getText().getBytes("UTF-8"))))) {
        JOptionPane.showMessageDialog(null, "Correct");
    }
    else {
        JOptionPane.showMessageDialog(null, rot13(Base64.getEncoder().encodeToString(this.textField1.getText().getBytes("UTF-8"))));
    }
}
~~~

Flag1 满足 Base64 编码后进行 Rot13 加密，密文为 `MzkuM8gmZJ6jZJHgnaMuqy4lMKM4`。逆运算即可获得 flag1。

Flag2 求解的过程涉及一段字符串 `"\u0089\u009a\u0081\u008c\u009b\u0086\u0080...`，在 `build` 之后进行了输出，发现是一段简单混淆过的 javascript 代码：

~~~javascript
function checkflag2(_0xa83ex2) { var _0x724b = ['charCodeAt', 'map', '', 'split', 'stringify', 'Correct', 'Wrong', 'j-']; return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function (_0xa83ex3) { return _0xa83ex3[_0x724b[0]](0) })) == JSON[_0x724b[4]]([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232][_0x724b[1]](function (_0xa83ex3) { return (checkflag2 + _0x724b[2])[_0x724b[0]](_0xa83ex3) })) ? _0x724b[5] : _0x724b[6]) }
~~~

简单处理可得：
~~~javascript
function checkflag2(flag) {
    return (JSON.stringify(flag.split('').map(
        function (s) {
            return s.charCodeAt(0)
        })
    ) == JSON.stringify([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(
        function (s) {
            return (checkflag2 + '').charCodeAt(s)
        })) ? 'Correct' : 'Wrong')
}
~~~

获取等式右边的值即可得到 flag2。注意由于计算过程中用到了 checkflag2 作为字符串，故需保证在求解 flag 的时候该函数与之前有混淆时一致。

~~~javascript
function get_flag() {
    JSON.stringify([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(
        function (s) {
            return (checkflag2 + '').charCodeAt(s)
        }))
}
~~~