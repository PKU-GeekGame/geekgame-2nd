import sys
sys.setrecursionlimit(1 << 16)

from Crypto.Cipher import AES
from random import choice
# with open("flag1.bak", "r") as f:
#     s = f.readline().strip()

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

with open("flag2.bak", "r") as f:
    x = f.read().strip()

s = x.encode("shift_jis").decode("utf-8", errors = "ignore")
s = s[:2] + "：" + s[2:]

std = x

ans = ""
result = ""

text = ""
temp = []

def check(ans):
    global temp
    temp = ans.encode("utf-8").decode("shift_jis", errors = "ignore")
    return temp == std[:len(temp)]

def win(ans):
    global temp
    temp = ans.encode("utf-8").decode("shift_jis", errors = "ignore")
    return temp == std

def lose(ans):
    global temp
    temp = ans.encode("utf-8").decode("shift_jis", errors = "ignore")
    return len(temp) > len(std)

def Decrypt(ciphertext):
    # 1. Remove Header and Decode
    if ciphertext.startswith('佛曰：'):
        ciphertext = ciphertext[3:]
        data = b''
        i = 0
        while i < len(ciphertext):
            if ciphertext[i] in BYTEMARK:
                i = i + 1
                if i < len(ciphertext):
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
        i = 1
        _l = len(result)
        while i < _l:
            if result[i] != 0:
                raise Exception("GG")
            if result[i-1] > 127:
                raise Exception("GG")
            i += 2
        # 4. Decode Plaintext with UTF-16 Little Endian
        return result.decode('utf-16le')
    else:
        return ''

def cut_decrypt(ciphertext):

    ciphertext = ciphertext[3:]
    data = b''
    i = 0
    while i < len(ciphertext):
        if ciphertext[i] in BYTEMARK:
            i = i + 1
            if i < len(ciphertext):
                data = data + bytes([TUDOU.index(ciphertext[i]) + 128])
        else:
            data = data + bytes([TUDOU.index(ciphertext[i])])
        i = i + 1
    # 2. Use AES-256-CBC to Decrypt
    l = len(data) // 16 * 16
    data = data[:l]
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    result = cryptor.decrypt(data)
    # 3. Remove Paddings (PKCS7)
    temp = result[:-50]
    i = 17
    _l = len(temp)
    while i < _l:
        if temp[i] != 0:
            return False
        i += 2
    return True

# real_ans = []

# def test(i, n, flag):
#     global ans
#     global real_ans
#     if i % 200 == 0:
#         print(i)
#         if i != 0:
#             if not cut_decrypt(ans):
#                 return False
#     if win(ans):
#         real_ans.append(ans)
#         # try:
#         #     real_result = Decrypt(ans)
#         # except:
#         #     return False
#         # with open("flag2.ans", "w", encoding="utf-8") as f:
#         #     f.write(result)
#         # with open("flag2.key", "w", encoding="utf-8") as f:
#         #     f.write(real_result)
#         return True
#     if lose(ans):
#         return False
#     if i < n:
#         ans += s[i]
#         if check(ans):
#             test(i+1, n, True)
#         ans = ans[:-1]
#     for x in TUDOU:
#         if i >= n or s[i] != x:
#             ans += x
#             if check(ans):
#                 test(i, n, True)
#             ans = ans[:-1]
#     if flag:
#         for x in BYTEMARK:
#             if i >= n or s[i] != x:
#                 ans += x
#                 if check(ans):
#                     test(i, n, False)
#                 ans = ans[:-1]
#     return False

# test(0, len(s), True)
# real_ans = list(map(lambda x: x[:950], real_ans))
# real_ans = list(set(real_ans))
# print(len(real_ans))

with open("flag2.ans.bak", "r", encoding="utf-8") as f:
    ans = f.read()

ans = ans[:-50]

def dfs(i, n):
    global ans
    if i % 200 == 0:
        if i != 0:
            if not cut_decrypt(ans):
                return False
    if win(ans):
        try:
            real_result = Decrypt(ans)
        except:
            return False
        with open("flag2.ans", "w", encoding="utf-8") as f:
            f.write(ans)
        with open("flag2.key", "w", encoding="utf-8") as f:
            f.write(real_result)
        return True
    if lose(ans):
        return False
    if i < n:
        ans += s[i]
        if check(ans) and dfs(i+1, n):
            return True
        ans = ans[:-1]
    for x in TUDOU+BYTEMARK:
        if i >= n or s[i] != x:
            ans += x
            if check(ans):
                if dfs(i, n):
                    return True
            ans = ans[:-1]
    return False

print(dfs(0, len(s)))

# for i in s:
#     ans.append(i)
#     text = "".join(ans)
#     temp = show(text.encode("utf-8").decode("shift_jis", errors = "ignore").encode("shift_jis"))
#     while temp != std[:len(temp)]:

#         ans.pop()
#         res = []

#         for x in TUDOU + BYTEMARK:
#             ans.append(x)
#             text = "".join(ans)
#             temp = show(text.encode("utf-8").decode("shift_jis", errors = "ignore").encode("shift_jis"))
#             if temp == std[:len(temp)]:
#                 res.append(x)
#             ans.pop()

#         print(res)

#         ans.append(res[-1])
#         ans.append(i)
#         text = "".join(ans)
#         temp = show(text.encode("utf-8").decode("shift_jis", errors = "ignore").encode("shift_jis"))

