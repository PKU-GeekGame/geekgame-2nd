import re
from pwn import *
from math import sqrt
import time
 
def isPrime(n):
	if n % 2 == 0: 
		return False
	for i in range(3, int(sqrt(n)) + 1, 2): 
		if n % i == 0: 
			return False
	return True

while 1:
	r = remote('prob01.geekgame.pku.edu.cn', 10001)
	title = r.recv()
	print(title.decode("utf-8"))
	r.sendline('114:XXX')
	title = r.recv()
	print(title.decode("utf-8"))
	r.sendline('急急急')

	while 1:
		time.sleep(0.1)
		recv = r.recv()
		if recv:
			recv=recv.decode("utf-8")
			print(recv)
			if re.search("gStore", recv):
				r.sendline('10.14778/2002974.2002976')
			elif re.search("电子游戏概论", recv):
				a=re.findall("\d+",recv)
				level=int(a[1])
				money=300+int(level**1.5)*100
				r.sendline(str(money))
			elif re.search("video/BV1EV411s7vu", recv):
				r.sendline('418645518')
			elif re.search("PKU Runner", recv):
				r.sendline('cn.edu.pku.pkurunner')
			elif re.search("http://ctf.世界一流大学.com", recv):
				r.sendline('ctf.xn--4gqwbu44czhc7w9a66k.com')
			elif re.search("Firefox", recv):
				r.sendline('65')
			elif re.search("gStore", recv):
				r.sendline('10.14778/2002974.2002976')
			elif re.search("质数", recv):
				a=re.findall("\d+",recv)
				minn=int(a[1])
				maxn=int(a[2])
				flag=0
				for i in range(int(minn*0.7+maxn*0.3),maxn): 
					if isPrime(i): 
						print(i)
						r.sendline(str(i))
						flag=1
						break
				if flag==0:
					for i in range(minn+1,int(minn*0.7+maxn*0.3)): 
						if isPrime(i): 
							print(i)
							r.sendline(str(i))
							break			
			elif re.search("d2:94:35:21:42:43", recv):
				r.sendline('11111')
			elif re.search("flag", recv):
				break
			elif re.search("答案格式", recv):
				r.interactive()
	r.close()
	print('\n\n\n')
	time.sleep(5)