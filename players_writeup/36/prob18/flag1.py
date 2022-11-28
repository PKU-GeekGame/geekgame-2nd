from collections import defaultdict
from Crypto.Cipher import AES

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

tset = set(TUDOU)
bset = set(BYTEMARK)

alpha = TUDOU + BYTEMARK + ['：']
utf8_codes = {x.encode('utf-8'): x for x in alpha}

possible = defaultdict(set)
for x in utf8_codes:
    possible[b''].add(x[0])
    possible[x[:1]].add(x[1])
    possible[x[:2]].add(x[2])

mid = defaultdict(set)
front = defaultdict(set)
for x in utf8_codes:
    mid[x[:1] + x[2:]].add(utf8_codes[x])
    front[x[1:]].add(utf8_codes[x])


def Decrypt(ciphertext):
    KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
    IV = b'Potato@Key@_@=_='

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


def dfs(i, now, jis):
    if i >= len(jis):
        return ''.join(now)

    if jis[i:i+3] in utf8_codes:
        val = utf8_codes[jis[i:i+3]]
        if not (len(now) > 0 and now[-1] in bset and val in bset):
            now.append(val)
            enc = ''.join(now).encode('utf-8').decode('shift_jis',
                                                      errors='ignore').encode('shift_jis')
            l = min(len(enc), len(jis))
            if enc[:l] == jis[:l]:
                res = dfs(i+3, now, jis)
                if res is not None:
                    return res
            now.pop()

    if i + 1 < len(jis):
        for x in possible[jis[i:i+2]]:
            val = utf8_codes[jis[i:i+2] + bytes([x])]
            if not (len(now) > 0 and now[-1] in bset and val in bset):
                now.append(val)
                enc = ''.join(now).encode('utf-8').decode('shift_jis',
                                                          errors='ignore').encode('shift_jis')
                l = min(len(enc), len(jis))
                if enc[:l] == jis[:l]:
                    res = dfs(i+2, now, jis)
                    if res is not None:
                        return res
                now.pop()

        for val in mid[jis[i:i+2]]:
            if not (len(now) > 0 and now[-1] in bset and val in bset):
                now.append(val)
                enc = ''.join(now).encode('utf-8').decode('shift_jis',
                                                          errors='ignore').encode('shift_jis')
                l = min(len(enc), len(jis))
                if enc[:l] == jis[:l]:
                    res = dfs(i+2, now, jis)
                    if res is not None:
                        return res
                now.pop()

        for val in front[jis[i:i+2]]:
            if not (len(now) > 0 and now[-1] in bset and val in bset):
                now.append(val)
                enc = ''.join(now).encode('utf-8').decode('shift_jis',
                                                          errors='ignore').encode('shift_jis')
                l = min(len(enc), len(jis))
                if enc[:l] == jis[:l]:
                    res = dfs(i+2, now, jis)
                    if res is not None:
                        return res
                now.pop()

    return None


enc1 = open('flag1.enc', 'r').read()
jis1 = enc1.encode('shift_jis')
foyue1 = dfs(0, [], jis1)
print(foyue1)
flag1 = Decrypt(foyue1)
print('Flag 1:', flag1)
