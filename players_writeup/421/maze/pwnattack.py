# level = 14
# print()

import math
from pwn import *

ops = {
	'N':'SUWE',
	'S':'NUWE',
	'E':'WUNS',
	'W':'EUNS'
}

conn = remote('prob03.geekgame.pku.edu.cn',10003,typ='tcp')
print(str(conn.recvuntil(b': ')))
conn.send(b'421:XXX')
level3 = False
cnt = 0
while True:
	cnt = cnt + 1
	gameMap = str(conn.recvuntil(b'(estart)'), encoding='utf-8')
	print(gameMap)
	if len(gameMap) > 2000 and not level3:
		level3 = True
		startPos = input("StartPos: ")
		trySeq = ops[startPos]
		cnt = 0
	if "E" in gameMap.split("Avail")[0]:
		print("Warning: Endpoint is available")
	op = input("round" + str(cnt) + ": ")
	if len(op) == 0:
		possible = gameMap.split("Available directions: ")[1].split(" ")[0]
		if len(possible) == 1:
			op = possible + 'u'
		else:
			for c in trySeq:
				if c in possible:
					op = c + 'u'
					break
	if "#" in op:
		sop = op[:-1]
		conn.sendline(bytes(op,encoding='utf-8'))
		break
	conn.sendline(bytes(op,encoding='utf-8'))

print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))
print(str(conn.recvline(),encoding='utf-8'))