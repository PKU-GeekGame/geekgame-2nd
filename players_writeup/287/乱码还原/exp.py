from Crypto.Cipher import AES
from base64 import b16decode, b32decode, b64decode, b85decode, a85decode
import re
import time

start = time.time()

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
ALL = TUDOU + BYTEMARK
# 所有佛元的base16
ALL_HEX = []

for i in ALL:
    ALL_HEX.append(i.encode("utf-8").hex())

# flag1相关的文件名
flag = "flag1.enc"
flag_fo_broken = "flag1_fo_broken.txt"
flag_fo = "flag1_fo.txt"
flag_base = "flag1.txt"

# flag2相关的文件名
# flag = "flag2.enc"
# flag_fo_broken = "flag2_fo_broken.txt"
# flag_fo = "flag2_fo.txt"
# flag_base = "flag2_base.txt"

f = open(flag,"r", encoding="utf-8")
# 获取所给的shift_jis字符串
original_shift_jis = f.read()

# 佛码的broken_utf8字符串
original_broken_utf8 = original_shift_jis.encode("shift_jis").decode("utf-8", errors="backslashreplace")
original_broken_utf8 = original_broken_utf8.replace("\\x", "")
with open(flag_fo_broken, "w", encoding="utf-8") as f:
    f.write(original_broken_utf8)


l = list(original_broken_utf8)
# 弹出标头<佛曰bc9a>
for i in range(6):
    l.pop(0)
possible_block_list = ["佛曰："]


# 获取原始佛码
def get_fo():
    global possible_block_list
    print(possible_block_list)
    while True:
        print(len(possible_block_list[0]))
        if len(l) == 0:
            break
        next_char = l[0]
        if next_char in ALL:
            new_possible_block_list = []
            for one_block in possible_block_list:
                one_block += next_char
                new_possible_block_list.append(one_block)
            possible_block_list = new_possible_block_list
            c = l.pop(0)
            # print(c)
            # print("读取一个字符后的possible_block列表:")
            # print(possible_block_list)
            continue
        
        elif next_char in [hex(j)[2] for j in range(16)]:
            read_number()
            check_aes()
        else:
            c = l.pop(0)
            print(c)
            print("下一个字符不符合要求")
            exit()
        # if count >= 16:
        #     break

    print("最终得到的可能的佛码的个数：", len(possible_block_list))
    with open(flag_fo, "w", encoding="utf-8") as f:
        for i in possible_block_list:
            f.write(i + "\n\n")

    fo = possible_block_list[0]
    print("得到的佛码：")
    print(fo)
    return fo

# 将一个字符的hex_string截取成三个字符串形成的列表
def cut(obj, length):
    return [
        obj[i:i + length]
        for i in range(0, len(obj), length)
        ]

# 恢复broken的片段，即number
def read_number():
    global possible_block_list
    
    number_string = ""
    for i in l:
        if i in [hex(j)[2] for j in range(16)]:
            number_string += i
        else:
            break
    
    length = len(number_string)
    for i in range(length):
        l.pop(0)
    number_list = re.findall(r"(e.)([^e].{1}){0,1}", number_string)
    # print("将要处理的number_string:\n", number_string)
    # print("将要处理的number_list:\n", number_list)
    
    # 遍历数字列表，生成block的所有可能列表
    for i in number_list:
        # if i[1] == "":
        f = False
        match_char_list = []
        # 遍历字集的十六进制字符串列表，如果符合条件则
        for one_char in ALL_HEX:
            if i[0] in cut(one_char,2) and (True if i[1] == "" else (i[1] in cut(one_char,2))):
            # if i[0] in one_char:
                f = True
                # print(one_char)
                match_char_list.append(one_char)
            else:
                if (not f) and (ALL_HEX.index(one_char) == len(ALL_HEX) - 1):
                    print("NO!")
                    exit()
        new_possible_block_list=  []
        # 遍历possible_block列表，生成新的possible_block列表
        if len(possible_block_list) == 0:
            for match_char in match_char_list:
                new_possible_block_list.append(bytes.fromhex(match_char).decode("utf-8"))
        else:
            for one_block in possible_block_list:
                for match_char in match_char_list:
                    new_possible_block_list.append(one_block + bytes.fromhex(match_char).decode("utf-8"))
        possible_block_list = new_possible_block_list
    # print("处理number后得到的列表:\n", possible_block_list)

    # 每处理一次number，检测一下是否与original_shift_jis符合
    check_shift_jis()

# 检查佛码经过utf8编码再经过shift_jis解码后是否和所给的shift_jis一致
def check_shift_jis():
    global possible_block_list
    new_possible_block_list = []
    for i in possible_block_list:
        possible_shift_jis = i.encode("utf-8").decode("shift_jis", errors="ignore")
        if possible_shift_jis == original_shift_jis[:len(possible_shift_jis)]:
            new_possible_block_list.append(i)
    if new_possible_block_list == []:
        print("没有符合shift_jis的！")
        exit()
    else:
        possible_block_list = new_possible_block_list
        # print("符合shift_jis的！")
        # print(possible_block_list)


# 检查是否可以成功解密
def check_aes():
    global possible_block_list
    new_possible_block_list = []

    for one_possible_block in possible_block_list:
        is_base = False
        try:
            flag_base = Decrypt(one_possible_block)
            is_base = check_flag_base(flag_base)
            if is_base:
                new_possible_block_list.append(one_possible_block)
        except:
            continue
    
    if new_possible_block_list == []:
        # print(">>>>>>>>>>>>>AES解密后不符合要求")
        return
    else:
        possible_block_list = new_possible_block_list
        print(">>>>>>>>>>>>>AES解密后符合要求!")
        return


# 检查是否是base字符串
def check_flag_base(flag_base):
    printable_char_list = [chr(i) for i in range(32, 127)]
    for i in flag_base:
        if i not in printable_char_list:
            return False
    return True



# 解密佛码，得到base字符串并写入文件
def get_base(fo):
    base = Decrypt(fo)
    with open(flag_base, "w", encoding="utf-8") as f:
        f.write(base)
    print("解密得到的base")
    print(base)
    return base

# 解密佛码
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
        # print(result)
        # 3. Remove Paddings (PKCS7)
        flag = result[-1]
        if flag < 16 and result[-flag] == flag:
            result = result[:-flag]
        # 4. Decode Plaintext with UTF-16 Little Endian
        return result.decode('utf-16le')
    else:
        return ''

# 解码base字符串
def decode_base(base):

    def check_ischar(mid_base, tmp, type):
        nonlocal base
        if b"flag{" in mid_base:
            print("得到flag!")
            print(type + "解码后")
            print(mid_base.decode("utf-8"))
            return
        for i in mid_base:
            if i >= ord(" ") and i <= ord("~"):
                continue
            else:
                base = tmp
                raise Exception("存在不可见字符" + type)
                # print(base)
                # print(type)
                # os._exit(0)
        print("全部都是可见字符！")
        print(type + "解码后")
        print(mid_base)
        print("==============================================================")

    
    for i in range(10):
        try:
            # 如果 s 被错误地填写或输入中存在字母表之外的字符，将抛出 binascii.Error
            # 每次解码前都需要使用tmp保存解码之前的文本，万一解码后的不符合要求则恢复原来的文本
            tmp = base
            base = b16decode(base)
            check_ischar(base, tmp, "base16")
        except:
            try:
                tmp = base
                base = b32decode(base)
                check_ischar(base, tmp, "base32")

            except:
                try:
                    # 必须加上validate=True，不然会尝试忽略不在字母表中的字符以使用base64解码
                    tmp = base
                    base = b64decode(base, validate=True)
                    check_ischar(base, tmp, "base64")
                except:
                    try:
                        tmp = base
                        base = b85decode(base)
                        check_ischar(base, tmp, "base85")
                    except:
                        try:
                            tmp = base
                            base = a85decode(base)
                            check_ischar(base, tmp, "ascii85")
                        except Exception as e:
                            print("所有都不符合要求！")
                            print(e)
                            print(base)
                            exit()


fo  = get_fo()
base = get_base(fo)
decode_base(base.encode("utf-8"))

print("所使用时间")
print(time.time() - start)