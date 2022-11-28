# a.to_bytes(24,'big') =
#    f  l  a  g  x .......
# 0x66 6c 61 67 78 28 25 33 cf 02 92 eb 65 8b 66 e2 59 c5 16 4b 6b c7 d4 b2

#    f  l  a  g  {                                                   }
# 0x66 6c 61 67 7b ..................................................... 7d

# Printable ASCII: [20,7f)
# xor result:    3 ..................................................... cf

num=0x8282533cf0292eb658b66e259c5164b6bc7d4b2

def getPos(curx,level):
    x=curx<<8
    n=num>>(8*(19-level))
    div1=2*level
    div2=div1+1
    
    pos1=[]
    for i in range(0x20,0x7f):
        testx=x+i
        xorx=testx^n
        if xorx % div2 ==0 and (xorx>>4) % div1 ==0:
            pos1.append(testx)
    if level<19:
        for i in pos1:
            result=getPos(i,level+1)
            if result:
                return result
        return None
    else:
        for i in pos1:
            if (i&0xff)==0x7d:
                return i
        return None

result = getPos(0xb,1)
result += 0x7<<(4*39)
print('flag'+result.to_bytes(20,'big').decode('utf-8'))