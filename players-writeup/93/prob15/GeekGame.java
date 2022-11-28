import java.util.Base64;
import java.awt.event.ActionEvent;
import javax.script.ScriptEngine;
import java.awt.event.WindowListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowAdapter;
import javax.swing.JOptionPane;
import java.io.Writer;
import java.io.PrintWriter;
import java.io.StringWriter;
import javax.script.ScriptEngineManager;
import java.awt.Component;
import java.awt.Label;
import java.awt.LayoutManager;
import java.awt.Container;
import javax.swing.BoxLayout;
import javax.script.Invocable;
import java.awt.Button;
import java.awt.TextField;
import java.awt.event.ActionListener;
import java.awt.Frame;

// 
// Decompiled by Procyon v0.5.36
// 

public class GeekGame extends Frame implements ActionListener
{
    TextField textField1;
    Button button1;
    Button button2;
    Invocable invocable;
    
    GeekGame() {
        this.setSize(300, 300);
        this.setVisible(true);
        this.setLayout(new BoxLayout(this, 1));
        final Label comp = new Label("Flag: ");
        this.textField1 = new TextField("flag{...}");
        (this.button1 = new Button("Check Flag 1")).addActionListener(this);
        (this.button2 = new Button("Check Flag 2")).addActionListener(this);
        this.add(comp);
        this.add(this.textField1);
        this.add(this.button1);
        this.add(this.button2);
        final ScriptEngine engineByName = new ScriptEngineManager().getEngineByName("nashorn");
        try {
            final String s = "\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00cf\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088\u00dd\u00c7°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dd\u00c6\u0094\u0099\u008e\u009d\u00cf°\u00df\u0097\u00d8\u00dd\u00db\u008d\u00d2´\u00c8\u008c\u0087\u008e\u009d¬\u0080\u008b\u008a®\u009b\u00c8\u00c3\u00c8\u0082\u008e\u009f\u00c8\u00c3\u00c8\u00c8\u00c3\u00c8\u009c\u009f\u0083\u0086\u009b\u00c8\u00c3\u00c8\u009c\u009b\u009d\u0086\u0081\u0088\u0086\u0089\u0096\u00c8\u00c3\u00c8¬\u0080\u009d\u009d\u008a\u008c\u009b\u00c8\u00c3\u00c8¸\u009d\u0080\u0081\u0088\u00c8\u00c3\u00c8\u0085\u00c2\u00c8²\u00d4\u009d\u008a\u009b\u009a\u009d\u0081\u00cf\u00c7¥¼ ¡´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00db²²\u00c7°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dd´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00dc²²\u00c7°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00dd²\u00c6´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00de²²\u00c7\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00c7°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0094\u009d\u008a\u009b\u009a\u009d\u0081\u00cf°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00df²²\u00c7\u00df\u00c6\u0092\u00c6\u00c6\u00d2\u00d2\u00cf¥¼ ¡´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00db²²\u00c7´\u00df\u00c3\u00de\u00da\u00c3\u00de\u00d9\u00c3\u00de\u00d8\u00c3\u00dc\u00df\u00c3\u00de\u00df\u00da\u00c3\u00de\u00d9\u00c3\u00dc\u00de\u00c3\u00de\u00d9\u00c3\u00d9\u00d8\u00c3\u00dc\u00c3\u00dc\u00dc\u00c3\u00da\u00c3\u00d9\u00df\u00c3\u00db\u00c3\u00de\u00df\u00d9\u00c3\u00d9\u00c3\u00db\u00de\u00c3\u00df\u00c3\u00de\u00c3\u00d9\u00d8\u00c3\u00dc\u00c3\u00de\u00d9\u00c3\u00db\u00c3\u00d9\u00c3\u00dc\u00dc\u00c3\u00dd\u00dc\u00dd²´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00de²²\u00c7\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081\u00c7°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0094\u009d\u008a\u009b\u009a\u009d\u0081\u00cf\u00c7\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088\u00dd\u00c4\u00cf°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00dd²\u00c6´°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00df²²\u00c7°\u00df\u0097\u008e\u00d7\u00dc\u008a\u0097\u00dc\u00c6\u0092\u00c6\u00c6\u00d0°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00da²\u00d5°\u00df\u0097\u00d8\u00dd\u00db\u008d´\u00d9²\u00c6\u0092";
            final StringBuilder sb = new StringBuilder();
            for (int i = 0; i < s.length(); ++i) {
                sb.append((char)(s.charAt(i) ^ '\u00ef'));
            }
            System.out.printf(sb.toString());
            engineByName.eval(sb.toString());
        }
        catch (Exception ex) {
            final StringWriter out = new StringWriter();
            ex.printStackTrace(new PrintWriter(out));
            JOptionPane.showMessageDialog(null, out.toString());
        }
        this.invocable = (Invocable)engineByName;
        this.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(final WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }
    
    @Override
    public void actionPerformed(final ActionEvent actionEvent) {
        try {
            if (actionEvent.getSource() == this.button1) {
                if ("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4".equals(rot13(Base64.getEncoder().encodeToString(this.textField1.getText().getBytes("UTF-8"))))) {
                    JOptionPane.showMessageDialog(null, "Correct");
                }
                else {
                    JOptionPane.showMessageDialog(null, "Wrong");
                }
            }
            else {
                JOptionPane.showMessageDialog(null, this.invocable.invokeFunction((actionEvent.getSource() == this.button2) ? "checkflag2" : "checkflag3", this.textField1.getText()));
            }
        }
        catch (Exception ex) {
            final StringWriter out = new StringWriter();
            ex.printStackTrace(new PrintWriter(out));
            JOptionPane.showMessageDialog(null, out.toString());
        }
    }
    
    static String rot13(final String s) {
        final StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); ++i) {
            char char1 = s.charAt(i);
            if (char1 >= 'a' && char1 <= 'm') {
                char1 += '\r';
            }
            else if (char1 >= 'A' && char1 <= 'M') {
                char1 += '\r';
            }
            else if (char1 >= 'n' && char1 <= 'z') {
                char1 -= '\r';
            }
            else if (char1 >= 'N' && char1 <= 'Z') {
                char1 -= '\r';
            }
            else if (char1 >= '5' && char1 <= '9') {
                char1 -= '\u0005';
            }
            else if (char1 >= '0' && char1 <= '4') {
                char1 += '\u0005';
            }
            sb.append(char1);
        }
        return sb.toString();
    }
    
    public static void main(final String[] array) {
        final GeekGame geekGame = new GeekGame();
    }
}
