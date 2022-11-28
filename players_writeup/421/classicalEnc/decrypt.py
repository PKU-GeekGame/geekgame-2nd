with open("crypt1.txt") as f:
	cipher_text = f.read()
letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
key  =  'YNKDFMRAWJQPLTZCHIEGUVXOBS'
unknown = ""
keymap={letters[i]:key[i] for i in range(26)}
current_key={letters[i]:letters[i] for i in range(26)}
plain_text = ""
for i in cipher_text:
	if i not in letters and i not in letters.lower():
		plain_text=plain_text+i
	else:
		if i in unknown or i in unknown.lower():
			plain_text = plain_text + '?'
		elif i in letters:
			for k in current_key:
				if current_key[k] == i:
					plain_text=plain_text+k
					break
		else:
			for k in current_key:
				if current_key[k] == i.upper():
					plain_text=plain_text+k.lower()
					break
		current_key={i:keymap[current_key[i]] for i in current_key}
print(plain_text)