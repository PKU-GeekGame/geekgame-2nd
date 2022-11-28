import hashlib
dic={}
for i in range(0,0xff):
	byte=i.to_bytes(1,'big')
	md=hashlib.md5(byte)
	mdstr=md.hexdigest()
	dic[mdstr]=byte
for i in range(0,0xffff):
	byte=i.to_bytes(2,'big')
	md=hashlib.md5(byte)
	mdstr=md.hexdigest()
	dic[mdstr]=byte
with open('org2.txt') as f:
    lines=f.readlines()
result=""
for line in lines:
	line=line.strip()
	if line in dic:
		result+=dic[line].decode()

print(result)	