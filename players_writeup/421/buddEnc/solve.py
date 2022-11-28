# The following code is copied from https://github.com/zyt717/CTFCodecTool/blob/master/ctfcodecs/tudoucode.py
from Crypto.Cipher import AES
from random import choice
import sys

sys.setrecursionlimit(100000)
KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
IV = b'Potato@Key@_@=_='

TUDOU = [
	'滅', '苦', '婆', '娑', '耶', '陀', '跋', '多', '漫', '都', '殿', '悉', '夜', '爍', '帝', '吉',
	'利', '阿', '無', '南', '那', '怛', '喝', '羯', '勝', '摩', '伽', '謹', '波', '者', '穆', '僧',
	'室', '藝', '尼', '瑟', '地', '彌', '菩', '提', '蘇', '醯', '盧', '呼', '舍', '佛', '參', '沙',
	'伊', '隸', '麼', '遮', '闍', '度', '蒙', '孕', '薩', '夷', '迦', '他', '姪', '豆', '特', '逝',
	'朋', '輸', '楞', '栗', '寫', '數', '曳', '諦', '羅', '曰', '咒', '即', '密', '若', '般', '故',
	'不', '實', '真', '訶', '切', '一', '除', '能', '等', '是', '上', '明', '大', '神', '知', '三',
	'藐', '耨', '得', '依', '諸', '世', '槃', '涅', '竟', '究', '想', '夢', '倒', '顛', '離', '遠',
	'怖', '恐', '有', '礙', '心', '所', '以', '亦', '智', '道', '。', '集', '盡', '死', '老', '至']

BYTEMARK = ['冥', '奢', '梵', '呐', '俱', '哆', '怯', '諳', '罰', '侄', '缽', '皤']

possibleUTF8Chars = TUDOU + BYTEMARK + ["佛","曰","："]

def Encrypt(plaintext):
	# 1. Encode Plaintext in UTF-16 Little Endian
	data = plaintext.encode('utf-16le')
	# 2. Add Paddings (PKCS7)
	pads = (- len(data)) % 16
	data = data + bytes(pads * [pads])
	# 3. Use AES-256-CBC to Encrypt
	cryptor = AES.new(KEY, AES.MODE_CBC, IV)
	result = cryptor.encrypt(data)
	# 4. Encode and Add Header
	return '佛曰：' + ''.join([TUDOU[i] if i < 128 else choice(BYTEMARK) + TUDOU[i - 128] for i in result])

def Decrypt(ciphertext):
	# 1. Remove Header and Decode
	if ciphertext.startswith('佛曰：'):
		ciphertext = ciphertext[3:]
		data = b''
		i = 0
		while i < len(ciphertext):
			if ciphertext[i] in BYTEMARK:
				i = i + 1
				data = data + bytes([TUDOU.index(ciphertext[i]) + 128])
			else:
				data = data + bytes([TUDOU.index(ciphertext[i])])
			i = i + 1
		# print(len(data))
		# 2. Use AES-256-CBC to Decrypt
		cryptor = AES.new(KEY, AES.MODE_CBC, IV)
		result = cryptor.decrypt(data)
		# 3. Remove Paddings (PKCS7)
		flag = result[-1]
		if flag < 16 and result[-flag] == flag:
			result = result[:-flag]
		# 4. Decode Plaintext with UTF-16 Little Endian
		return result.decode('utf-16le')
	else:
		return ''

with open("flag2.enc","r",encoding="utf-8") as f:
	jis_text = f.read()
broken_bytes = jis_text.encode("shift-jis")
char_array_output = ["佛","曰","："]
bytes_input = broken_bytes[8:]
global_progress = 0
confirmed_prefix = "佛曰："
fout = open("out.txt","w")

def search(parsed_bytes, tudou_len):
	global bytes_input
	global char_array_output
	global global_progress
	global confirmed_prefix
	if tudou_len  == 16:
		try:
			Decrypt("".join(char_array_output)).encode('ascii')
			global_progress = parsed_bytes
			confirmed_prefix = "".join(char_array_output)
			return
		except:
			return
	if parsed_bytes == len(bytes_input):
		return
	assert (bytes_input[parsed_bytes] & 0xf0) == 0xe0 
	if len(bytes_input) - parsed_bytes < 5:
		to_decode = bytes_input[parsed_bytes:]
	for i in range(parsed_bytes + 1, len(bytes_input)):
		if (bytes_input[i] & 0xf0) == 0xe0:
			to_decode = bytes_input[parsed_bytes:i]
			break
	l = len(to_decode)
	if l == 3:
		c = to_decode.decode("utf-8")
		incTudou = 1 if c in TUDOU else 0
		char_array_output.append(c)
		search(parsed_bytes + l, tudou_len + incTudou)
		char_array_output.pop()
	else:
		assert l < 3
		for c in possibleUTF8Chars:
			b3 = c.encode("utf-8")
			for b in to_decode:
				if b not in b3:
					break
			else:
				incTudou = 1 if c in TUDOU else 0
				char_array_output.append(c)
				search(parsed_bytes + l, tudou_len + incTudou)
				char_array_output.pop()

if __name__ == '__main__':
	while global_progress != len(bytes_input):
		search(global_progress, 0)
		fout.write(Decrypt(confirmed_prefix)[-8:])
		fout.flush()
		char_array_output = list(confirmed_prefix)
	fout.close()