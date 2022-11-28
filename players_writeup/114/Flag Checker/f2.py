with open("GeekGame.class","rb") as f:
    x=f.read()
    y=[]
    for i in range(100,len(x)-100):
        y.append(x[i]^0xEF)
    y=bytes(y)
    