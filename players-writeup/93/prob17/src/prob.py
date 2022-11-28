import sys, random

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
args=sys.argv[1:]
if len(args)!=1 and len(args)!=2:
    print("Usage: python3 prob.py <input file> <key (optional)>")
    exit()

if len(args)==1:
    args.append(''.join(random.sample(letters,26)))

filename, key=args
key=key.strip().upper()
if ''.join(sorted(key))!=letters:
    print("Invalid key")
    exit()

keymap={letters[i]:key[i] for i in range(26)}
current_key={letters[i]:letters[i] for i in range(26)}
with open(filename) as f:
    plain_text=f.read()

cipher_text=""
for i in plain_text:
    if i not in letters and i not in letters.lower():
        cipher_text=cipher_text+i
    else:
        if i in letters:
            cipher_text=cipher_text+current_key[i]
        else:
            cipher_text=cipher_text+current_key[i.upper()].lower()
        current_key={i:keymap[current_key[i]] for i in current_key}

print(cipher_text)
