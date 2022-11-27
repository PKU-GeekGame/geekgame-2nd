import java.applet.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Base64;
import javax.script.*;
import java.io.*;

public class GeekGame extends Frame implements ActionListener {
  GeekGame(){
    setSize(300,300); 
    setVisible(true);  
    setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
    Label label1 = new Label("Flag: ");

    textField1 = new TextField("flag{...}");

    button1 = new Button("Check Flag 1");
    button1.addActionListener(this);
    button2 = new Button("Check Flag 2");
    button2.addActionListener(this);

    add(label1);
    add(textField1);
    add(button1);
    add(button2);

    ScriptEngineManager factory = new ScriptEngineManager();
    ScriptEngine engine = factory.getEngineByName("nashorn");
    try {
      // Flag2
      // function checkflag2(flag){return(JSON.stringify(flag.split('').map(function(x){return x.charCodeAt(0)}))==JSON.stringify([102,108,97,103,123,102,108,97,103,50,125].map(function(x){return (checkflag2+'').charCodeAt(x)}))?'Correct':'Wrong');}
      // https://www.javascriptobfuscator.com/Javascript-Obfuscator.aspx
      //engine.eval("function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}");
      String s="\211\232\201\214\233\206\200\201\317\214\207\212\214\204\211\203\216\210\335\307\260\337\227\216\327\334\212\227\335\306\224\231\216\235\317\260\337\227\330\335\333\215\322\264\310\214\207\216\235\254\200\213\212\256\233\310\303\310\202\216\237\310\303\310\310\303\310\234\237\203\206\233\310\303\310\234\233\235\206\201\210\206\211\226\310\303\310\254\200\235\235\212\214\233\310\303\310\270\235\200\201\210\310\303\310\205\302\310\262\324\235\212\233\232\235\201\317\307\245\274\240\241\264\260\337\227\330\335\333\215\264\333\262\262\307\260\337\227\216\327\334\212\227\335\264\260\337\227\330\335\333\215\264\334\262\262\307\260\337\227\330\335\333\215\264\335\262\306\264\260\337\227\330\335\333\215\264\336\262\262\307\211\232\201\214\233\206\200\201\307\260\337\227\216\327\334\212\227\334\306\224\235\212\233\232\235\201\317\260\337\227\216\327\334\212\227\334\264\260\337\227\330\335\333\215\264\337\262\262\307\337\306\222\306\306\322\322\317\245\274\240\241\264\260\337\227\330\335\333\215\264\333\262\262\307\264\337\303\336\332\303\336\331\303\336\330\303\334\337\303\336\337\332\303\336\331\303\334\336\303\336\331\303\331\330\303\334\303\334\334\303\332\303\331\337\303\333\303\336\337\331\303\331\303\333\336\303\337\303\336\303\331\330\303\334\303\336\331\303\333\303\331\303\334\334\303\335\334\335\262\264\260\337\227\330\335\333\215\264\336\262\262\307\211\232\201\214\233\206\200\201\307\260\337\227\216\327\334\212\227\334\306\224\235\212\233\232\235\201\317\307\214\207\212\214\204\211\203\216\210\335\304\317\260\337\227\330\335\333\215\264\335\262\306\264\260\337\227\330\335\333\215\264\337\262\262\307\260\337\227\216\327\334\212\227\334\306\222\306\306\320\260\337\227\330\335\333\215\264\332\262\325\260\337\227\330\335\333\215\264\331\262\306\222";
      StringBuilder sb = new StringBuilder();
      for(int i = 0; i < s.length(); i++)
       sb.append((char)(s.charAt(i) ^ 239));
      engine.eval(sb.toString());
    } catch (Exception ee) {
      StringWriter sw = new StringWriter();
      PrintWriter pw = new PrintWriter(sw);
      ee.printStackTrace(pw);
      JOptionPane.showMessageDialog(null, sw.toString());
      //JOptionPane.showMessageDialog(null, "Error");
    }
    invocable = (Invocable) engine;
    addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
          System.exit(0);
      }
    });
  }

  public void actionPerformed(ActionEvent e) {
    try {
      if (e.getSource() == button1) {
        byte[] bytes = textField1.getText().getBytes("UTF-8");
        String encoded = rot13(Base64.getEncoder().encodeToString(bytes));
        // Flag 1: flag -> base64 -> ROT13
        if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(encoded)) {
          JOptionPane.showMessageDialog(null, "Correct");
        } else {
          JOptionPane.showMessageDialog(null, "Wrong");
        }
      } else {
        Object funcResult = invocable.invokeFunction(e.getSource() == button2 ? "checkflag2" : "checkflag3", textField1.getText());
        JOptionPane.showMessageDialog(null, (String) funcResult);
      }
    } catch (Exception ee) {
      StringWriter sw = new StringWriter();
      PrintWriter pw = new PrintWriter(sw);
      ee.printStackTrace(pw);
      JOptionPane.showMessageDialog(null, sw.toString());
      //JOptionPane.showMessageDialog(null, "Error");
    }
  }

  static String rot13(String input) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < input.length(); i++) {
      char c = input.charAt(i);
      if (c >= 'a' && c <= 'm') c += 13;
      else if (c >= 'A' && c <= 'M') c += 13;
      else if (c >= 'n' && c <= 'z') c -= 13;
      else if (c >= 'N' && c <= 'Z') c -= 13;
      else if (c >= '5' && c <= '9') c -= 5;
      else if (c >= '0' && c <= '4') c += 5;
      sb.append(c);
    }
    return sb.toString();
  }
  TextField textField1;
  Button button1, button2;
  Invocable invocable;
  public static void main(String args[]) {
      GeekGame f=new GeekGame();
  }  
}