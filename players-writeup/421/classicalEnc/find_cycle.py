import re
with open("crypt1.txt") as f:
	cipher_text = f.read()
letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_letters = ""
targets = ["glsipbqapech","zaceywtrykbg","ohpsaingacyt","qloxehmgomn","spaonxrwmm","bmxqlzhniy","qzglsiphnk",
	"zzctyneor","ttzklcrnh","dnzssrfgi","dhiwwboyn"]
gaps = []
for c in cipher_text:
	if c in letters or c in letters.lower():
		all_letters += c
for target in targets:
	this_pos = []
	for i in range(len(all_letters)):
		if all_letters[i:i+len(target)] == target:
			this_pos.append(i)
	for i in range(1,len(this_pos)):
		gaps.append(this_pos[i]-this_pos[i-1])
	# print(target, this_pos)
	print(target, this_pos[0] % 22)
print(gaps)
def gcd(a,b):
	return a if b == 0 else gcd(b, a%b)
dev = gaps[0]
for g in gaps:
	dev = gcd(dev, g)
print(dev)

print(all_letters.index('d') % 4, 'd')
print(all_letters.index('u') % 4, 'u')
print(all_letters.index('v') % 4, 'v')
print(all_letters.index('j') % 4, 'j')