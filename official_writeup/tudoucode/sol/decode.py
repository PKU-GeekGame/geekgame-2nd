from Crypto.Cipher import AES
chars='滅苦婆娑耶陀跋多漫都殿悉夜爍帝吉利阿無南那怛喝羯勝摩伽謹波者穆僧室藝尼瑟地彌菩提蘇醯盧呼舍佛參沙伊隸麼遮闍度蒙孕薩夷迦他姪豆特逝朋輸楞栗寫數曳諦羅曰咒即密若般故不實真訶切一除能等是上明大神知三藐耨得依諸世槃涅竟究想夢倒顛離遠怖恐有礙心所以亦智道。集盡死老至冥奢梵呐俱哆怯諳罰侄缽皤佛曰：'
import sys
sys.setrecursionlimit(15000)
x=open(sys.argv[1],"r",encoding="utf-8").read()
x=x.encode("shift_jis")
sections=[]
cur_section=[]
for i in x:
    if i>=192 or len(cur_section)>=3:
        if len(cur_section)>0:
            sections.append(tuple(cur_section))
            cur_section=[]
    cur_section.append(i)

sections.append(tuple(cur_section))
#print(sections)
charmap={}
for i in chars:
    chrutf=i.encode("utf-8")
    charmap[tuple(chrutf)]=i
    charmap[tuple(chrutf[:2])]=''.join(list(set(charmap.get(tuple(chrutf[:2]),'')+i)))
    charmap[tuple(chrutf[1:])]=''.join(list(set(charmap.get(tuple(chrutf[1:]),'')+i)))
    charmap[(chrutf[0],)+(chrutf[2],)]=''.join(list(set(charmap.get((chrutf[0],)+(chrutf[2],),'')+i)))
    charmap[(chrutf[0],)]=''.join(list(set(charmap.get((chrutf[0],),'')+i)))

sections=[charmap[i] for i in sections]
print(sections)
KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
IV = b'Potato@Key@_@=_='

def dectext(enctext):
    dec = AES.new(KEY, AES.MODE_CBC, IV).decrypt(bytes(enctext))
    flag = dec[-1]
    if flag < 16 and dec[-flag] == flag:
        dec = dec[:-flag]
    try:
        t=dec.decode('utf-16le')
        for i in t:
            if ord(i)>127:
                return None
            #if 0xA000<=ord(i)<=0xD7FF:
            #    return None
            #if 0xE000<=ord(i)<=0xFE50:
            #    return None
            #if 0x3400<=ord(i)<=0x4DBF:
            #    return None
        #print(t)
        return t
    except Exception as e:
        return None

def decpart(sections, curenctext, pre=False):
    if len(curenctext)%16==0 and not pre:
        z=dectext(bytes(curenctext))
        if z==None:
            return None
        else:
            #print(z)
            return sections, curenctext
    sect=sections[:]
    bm='冥奢梵呐俱哆怯諳罰侄缽皤'
    if len(set(sect[0])&set(bm))>0 and len(sect)>=2:
        for i in set(sect[1])-set(bm):
            u=decpart(sect[2:], curenctext+[chars.index(i)+128])
            if u!=None:
                return u
    for i in set(sect[0])-set(bm):
            u=decpart(sect[1:], curenctext+[chars.index(i)])
            if u!=None:
                return u

t, curenctext=sections[3:],[]
while len(t)>0:
    t, curenctext=decpart(t, curenctext, True)
    print(len(t))
print(dectext(bytes(curenctext)))
    #print(i)
