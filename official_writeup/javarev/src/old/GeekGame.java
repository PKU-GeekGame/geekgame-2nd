import java.applet.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Base64;
import javax.script.*;
import java.io.*;
import java.util.zip.Inflater;

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
    button3 = new Button("Check Flag 3");
    button3.addActionListener(this);

    add(label1);
    add(textField1);
    add(button1);
    add(button2);
    add(button3);

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
      // Flag3：https://www.geocachingtoolbox.com/index.php?lang=en&page=burrowsWheelerTransform (Method=Encrypt, End of file character=empty)
      //engine.eval("var y=Math.imul;var z=Math.fround;var oSlot=0;var nullArray=[null];var nullObj={d:nullArray,o:0};function v(w,x){var s=0,h=0,j=null,l=null,r=0,q=null,g=0,d=0,b=0,c=null,a=0,e=0,i=0,k=0;if((w[x]&255)!==0){g=0;while(1){g=g+1|0;if((w[x+g|0]&255)!==0)continue;break;}}else{g=0;}s=(x);g=(x+g|0);h=g-s|0;d=h+1|0;j=new Uint8Array(d/1|0);if((d|0)!==0){b=0;while(1){j[b]=0;b=b+1|0;if(j!==j||(0+d|0)!==(0+b|0))continue;break;}}l=R([],0,(h<<2)/4|0,null);if((h|0)>0){b=0;while(1){c=new Uint8Array(d/1|0);if((d|0)!==0){a=0;while(1){c[a]=0;a=a+1|0;if(c!==c||(0+d|0)!==(0+a|0))continue;break;}}a=b;e=0;while(1){i=w[x+a|0]|0;c[e]=i;if((i&255)!==0){a=a+1|0;e=e+1|0;continue;}break;}if((b|0)!==0){;if((c[0]&255)!==0){a=0;while(1){a=a+1|0;if((c[a]&255)!==0)continue;break;}}else{a=0;}e=b;i=0;while(1){k=w[x+i|0]|0;r=a+1|0;c[a]=k;if((k&255)!==0){e=e-1|0;if((e|0)!==0){a=r;i=i+1|0;continue;}c[r]=0;}break;}}l[b]={d:c,o:0};b=b+1|0;if((b|0)!==(h|0))continue;if((h|0)>1){g=(s^ -1)+g|0;g=(g|0)>1?g|0:1|0;d=0;while(1){b=d+1|0;if((b|0)<(h|0)){a=b;while(1){c=l[d];q=l[a];e=c.d[c.o]|0;if((e&255)!==0){k=0;i=0;while(1){if((e&255)===(q.d[q.o+k|0]&255)){i=i+1|0;e=c.d[c.o+i|0]|0;if((e&255)!==0){k=k+1|0;continue;}}else if((e&255)>(q.d[q.o+k|0]&255)){l[d]=q;l[a]=c;}break;}}a=a+1|0;if((a|0)<(h|0))continue;break;}}if((b|0)!==(g|0)){d=b;continue;}break;}}g=h-1|0;d=0;while(1){c=l[d];j[d]=c.d[c.o+g|0]|0;d=d+1|0;if((d|0)!==(h|0))continue;break;}break;}}oSlot=0;return j;}function t(){var d=null,e=null,f=0,b=0,a=0,c=0;d=new Uint8Array(200);a=0;b=0;while(1){d[0+a|0]=p[b]|0;a=a+1|0;if(d!==d||(0+100|0)!==(0+a|0)){b=b+1|0;continue;}break;}a=0;b=0;while(1){d[100+a|0]=o[b]|0;a=a+1|0;if(d===d&&(100+100|0)===(100+a|0)){e=v(d,0);f=oSlot;b=e[f]|0;if((b&255)!==0){c=0;a=0;while(1){if((b&255)===(d[100+c|0]&255)){a=a+1|0;b=e[f+a|0]|0;c=c+1|0;if((b&255)!==0)continue;b=0;}break;}}else{b=0;c=0;}return (b&255)-(d[100+c|0]&255)|0;}b=b+1|0;continue;}}var p=new Uint8Array([102,108,97,103,123,120,120,120,45,121,121,121,45,122,122,122,125,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]);var o=new Uint8Array([114,115,45,45,108,114,123,104,101,108,125,115,97,87,102,101,114,97,102,114,101,84,111,114,117,119,110,98,111,103,109,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]);function R(r,s,e,v){for(var i=s;i<e;i++)r[i]=v;return r;}function checkflag3(flag){for(i=0;i<flag.length;i++)p[i]=flag.charCodeAt(i);p[flag.length]=0;return t()?'Wrong':'Correct';}");
      byte[] output=new byte[]{120, -100, -43, 86, 91, -113, -38, 56, 20, -2, 43, -12, 101, -58, 17, -127, 58, 116, -48, -62, 4, -73, -86, -6, -68, 90, -87, 85, -75, 15, 81, 86, 74, 108, -109, 24, -78, -55, 96, 2, 51, 93, -56, 127, -17, 57, 118, 18, 12, 65, -38, 125, 91, 85, 35, -113, 47, 57, -105, -17, 124, -25, 50, 115, 76, -12, -24, 7, -5, 61, -87, -13, -87, -6, -5, 80, -124, 71, -72, -1, 99, -17, 107, 93, 29, 74, 97, 94, -86, 111, 69, 85, 51, 106, -50, -27, -95, 40, 62, 107, -99, -4, 96, 17, 30, -29, -2, -15, -113, 116, -61, 78, -30, -71, -1, -18, 87, -49, -76, 9, -41, -121, -110, -41, -86, 42, 71, 71, -14, -22, -65, 121, 39, -108, -34, 51, -22, -25, -80, 54, 12, -123, -3, -62, 110, 26, 94, 118, -10, -104, -63, 81, -64, 74, 97, 113, -5, -108, -64, 81, -62, 82, -80, -74, 0, 69, -83, 9, 121, -115, -34, -30, -121, -39, 124, -18, -67, 99, -116, 122, 39, -48, 10, 95, 115, 85, 72, 18, -32, 37, 27, 7, -25, 94, 110, -100, -99, -87, 35, -53, -85, -78, 86, -27, 65, -122, -87, -106, -55, 54, 108, 26, 89, -20, -91, 49, -48, -20, 25, 121, -13, -62, 12, 126, -93, -114, 23, -26, 44, -101, -20, -63, -112, 96, -71, 49, 8, -96, -27, -21, -24, -69, 42, -21, -123, 9, -109, -120, -9, 1, -54, -95, 35, 1, 7, -117, 37, 117, -79, 108, -94, 52, -122, 123, -54, -46, 14, -46, 6, -92, 54, -25, 51, -95, -29, 86, 5, 78, 41, -100, -122, -64, 10, -10, -107, 68, -79, 79, 125, -110, -81, 86, 51, -17, -3, -45, -103, -6, 72, -120, 117, -104, -125, -50, -57, 91, 119, -4, 63, 33, 76, -82, 84, -94, 4, 17, 38, 44, -23, 16, 114, -112, -30, 55, 8, -109, -69, 8, 19, -106, -122, -46, 53, -90, 24, 18, 14, -62, 49, -104, -30, -111, -116, -103, 50, -66, -107, -109, -85, -50, -109, 100, -46, -20, -67, -43, -90, 53, -117, 10, 105, 15, -42, -24, -13, -56, 77, -31, 117, 0, 14, 114, -126, -63, -4, 91, -86, 81, -71, -111, -128, 92, -71, 86, -74, 6, -71, -78, -56, 117, 107, -46, 112, -77, 53, -106, -73, -114, 123, 64, 62, -23, 60, 74, -121, 85, 13, 38, -43, 77, 76, 60, -46, 72, 111, -45, 39, 21, 11, 2, 122, -123, -37, 30, 113, 10, -93, -117, -39, 100, -10, -126, -67, -49, -75, -87, 108, -78, -1, 107, 52, 9, 60, -84, 79, 44, -44, -52, 124, -8, 4, -37, 115, 96, 10, -43, -119, 40, 101, -30, -54, -12, -54, 26, 62, 97, -46, -100, -126, 41, 34, 17, -121, 59, -40, -110, 24, 82, -62, -89, 34, -30, -45, 42, -18, -94, 115, -94, 54, -83, 119, -107, -20, 94, -128, 1, -22, 29, 104, -18, -90, -43, 120, -37, 117, 27, 86, -125, 106, 51, -35, -102, -19, -8, 29, -102, -34, -34, -48, 102, 82, 53, -70, -56, 125, -68, 103, 31, -95, -77, 93, -120, -48, 25, -65, 80, -20, 22, 68, 114, 9, 124, 80, 13, 46, -25, -103, -95, 70, 0, 53, -125, 114, 108, 50, -106, 79, 6, -20, -74, -60, 109, 16, 66, 23, 93, 102, -93, 19, 14, -15, -30, 110, 78, 91, -53, -99, -125, 110, -58, 106, 89, 31, 116, 57, -38, -124, 77, 63, 58, 107, 98, -25, -90, -80, -93, 80, -38, 109, -35, 14, -56, -60, 12, 73, -12, 120, -45, -10, 51, 10, 77, -97, -104, -63, -29, 96, 22, -111, 105, -28, -104, -67, 64, 17, -98, -81, 122, 94, 0, 72, 97, 122, 62, -96, -12, -70, -21, 79, 93, -115, 14, -104, -71, -29, 0, -76, -83, -117, 106, -24, 2, -86, 68, 60, 60, 16, 20, -79, 78, -80, 108, 90, 5, 15, -69, -22, 72, -124, 15, -72, -41, -52, 16, 2, -90, 101, -76, -18, -54, 37, 117, -54, -123, -101, 121, 117, 83, -119, 105, 95, -119, 22, 5, -65, -44, 73, 7, -62, 24, -20, -89, 19, -29, -105, -10, -72, 55, 51, -36, -82, 53, -125, 3, 95, -48, 117, -45, -26, -87, 85, -101, -36, 58, 60, -93, -30, -128, -77, 6, -45, -8, 114, -101, 40, -48, -100, -7, 1, 93, -8, -53, -33, 96, -5, -32, 7, 51, 92, -76, 95, 79, 115, -40, -126, 126, -103, -21, -52, 89, 115, -8, -13, -16, 11, -4, -60, -98, -3, 103, 98, 24, 126, -16, -28, 7, -63, 28, 3, -61, -40, -128, 8, -13, -126, 44, 80, -40, 105, 96, -33, 32, 78, -108, 2, -110, 22, -56, -45, -52, 126, 1, -55, 101, 123, 13, -84, -16, 2, -83, -39, 47, 65, 0, -97, -126, 37, 44, -22, 47, 23, -10, 25, 9, -90, -53, -1, -101, -116, 43, 90, -6, 78, -1, 74, -76, -65, -9, -91, 127, -12, 78, -21, 74, 19, -92, 75, -79, 125, -88, 86, -16, 39, 96, 60, -10, 116, -92, 98, 118, -20, 70, -124, 118, 70, 4, -49, 37, -33, -82, -117, 36, -5, 64, -16, -73, 85, -57, 65, -83, 86, 120, -97, 22, -78, -52, -22, -36, 24, 121, 65, 35, -26, -111, -25, -119, -2, 82, 9, -7, -71, 38, -54, 11, 95, 34, 71, 50, -66, 76, 34, -104, 62, -97, 30, -1, -44, 85, -103, 61, 62, 63, 126, -87, -76, -106, -68, 126, 12, -101, -97, 12, -118, -6, 122};
     // Decompress the bytes
     Inflater decompresser = new Inflater();
     decompresser.setInput(output);
     byte[] result = new byte[7000];
     int resultLength = decompresser.inflate(result);
     decompresser.end();
     engine.eval(new String(result, 0, resultLength, "UTF-8"));
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
  Button button1, button2, button3;
  Invocable invocable;
  public static void main(String args[]) {
      GeekGame f=new GeekGame();
  }  
}