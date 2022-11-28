import sys
letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
with open('crypt1.txt','r') as f:
    plain_text=f.read()
with open('1.txt','w') as f:
    for i in plain_text:
        if i in letters or i in letters.lower():
            f.write(i)
            f.write('\n')
        elif i==' ':
            f.write(i)