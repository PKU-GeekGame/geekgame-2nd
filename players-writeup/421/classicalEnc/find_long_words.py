with open("crypt1.txt") as f:
	cipher_text = f.read()
letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
longWordSet=set()
for w in cipher_text.split(' '):
	if len(w) == 9 and w[-1]!='.':
		if w in longWordSet:
			print(w)
		longWordSet.add(w)