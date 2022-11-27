from gorand import *
import requests, datetime, time, sys
server=sys.argv[1]
def getboard():
    for i in range(16):
        u=requests.post(server+"/click",data={"x":0,"y":i}).json()
        if "boom" in u:
            return u["boom"]

def getlv1rand():
    return [i==-1 for i in sum(getboard(),[])]

def getlv1seed():
    ts=int((datetime.datetime.strptime(requests.post(server+"/reset").headers["Date"],"%a, %d %b %Y %H:%M:%S GMT").timestamp()+8*3600)*1000)
    requests.post(server+"/init",data={"level":1})
    rnd=getlv1rand()
    for i in range(int((time.time()-1)*1000),int((time.time()+20)*1000)):
        setseed(i)
        ok=True
        for j in range(256):
            if intn(257)%2!=rnd[j]:
                ok=False
                break
        if ok:
            return i

setseed(getlv1seed())
[intn(257)%2 for i in range(256)]
for x in range(16):
    for y in range(16):
        if intn(257)%2==0:
            k=requests.post(server+"/click",data={"x":x,"y":y}).json()
            if "flag" in k:
                print(k["flag"])
