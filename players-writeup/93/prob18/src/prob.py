# The following code is copied from https://github.com/zyt717/CTFCodecTool/blob/master/ctfcodecs/tudoucode.py
from Crypto.Cipher import AES
from random import choice

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

if __name__ == '__main__':
    with open("flag1","r",encoding="utf-8") as f:
        x=f.read()
    with open("flag1.enc","w",encoding="utf-8") as f:
        f.write(Encrypt(x).encode("utf-8").decode("shift_jis",errors="ignore"))   

    with open("flag2","rb") as f:
        x=f.read()
    from base64 import b16encode, b32encode, b64encode, b85encode, a85encode
    for i in range(10):
        x=choice([b16encode, b32encode, b64encode, b85encode, a85encode])(x)
    with open("flag2.enc","w",encoding="utf-8") as f:
        f.write(Encrypt(x.decode("utf-8")).encode("utf-8").decode("shift_jis",errors="ignore"))