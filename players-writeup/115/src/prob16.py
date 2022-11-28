alpha = "abcdef1234567890"

def dfs(h):
    if(len(h)>=39):
        print(h, len(h))
        return
    for i in range(16):
        h += alpha[i]
        if int(h, 16) % len(h) == 0:
            dfs(h)
        h = h[:-1]

dfs("")
# aa44ce207c78fc30003c3cc0d8382e2078d07ef 39
# fae06678c2e884607eb8b4e0b0a0f0603420342 39
# 34e4a468166cd8604ec0f8106ab4326098286cf 39

num=int("aa44ce207c78fc30003c3cc0d8382e2078d07ef", 16)  # flag{fOUnd_mAGic_number}
#num=int("34e4a468166cd8604ec0f8106ab4326098286cf", 16) # flagr\x8cI\xf1\xe8\xc5\x1d(E\xa8\xa5.TF\xb4\xa9lj\xf3]
#num=int("fae06678c2e884607eb8b4e0b0a0f0603420342", 16) # flag~l\x05\xd0\xe5\x8dX\xe8F\xaf!\xe1Y\xe7\xf8\x89f\xaav\xd0
k=num^2511413510786744838119565865056609615595993472546783131026
p = k.to_bytes(24, 'big')
print(p)