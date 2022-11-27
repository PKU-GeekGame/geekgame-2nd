from gorand import *
import requests, datetime, time, sys
server=sys.argv[1]
def getboard():
    for i in range(16):
        u=requests.post(server+"/click",data={"x":0,"y":i}).json()
        if "boom" in u:
            return u["boom"]

def getlv2rand():
    u=getboard()
    x=sum(u[:4],[])
    y=sum(u[4:8],[])
    z=sum(u[8:12],[])
    w=sum(u[12:16],[])
    return [sum([2**i*(x[i]==-1) for i in range(64)]),sum([2**i*(y[i]==-1) for i in range(64)]),sum([2**i*(z[i]==-1) for i in range(64)]),sum([2**i*(w[i]==-1) for i in range(64)])]

requests.post(server+"/reset")
requests.post(server+"/init",data={"level":2})

x=[]
for i in range(200):
    x.extend(getlv2rand())

for t in range(4):
    x.append((x[-607]+x[-273])%(1<<64))
    v=x[-1]
    for i in [i for i in range(64) if (v>>i)&1==0]:
        k=requests.post(server+"/click",data={"y":i%16,"x":i//16+4*t}).json()
        if "flag" in k:
            print(k["flag"])
