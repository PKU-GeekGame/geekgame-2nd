import base64

s = 'MzkuM8gmZJ6jZJHgnaMuqy4lMKM4'


def rot13(s):
    ans = []
    for ch in s:
        if 'a' <= ch <= 'm' or 'A' <= ch <= 'M':
            ans.append(chr(ord(ch) + 13))
        elif 'n' <= ch <= 'z' or 'N' <= ch <= 'Z':
            ans.append(chr(ord(ch) - 13))
        elif '0' <= ch <= '4':
            ans.append(chr(ord(ch) + 5))
        elif '5' <= ch <= '9':
            ans.append(chr(ord(ch) - 5))
        else:
            ans.append(ch)
    return ''.join(ans)


flag = base64.b64decode(rot13(s))
print(flag)
