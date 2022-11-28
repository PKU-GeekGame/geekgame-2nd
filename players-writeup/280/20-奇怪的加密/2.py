import collections
import hashlib
import math
import string


digests = {chr(i): hashlib.md5(chr(i).encode()).hexdigest() for i in range(2 ** 8)}

# for s in (' m', 'es'):
#     digests[s] = hashlib.md5(s.encode()).hexdigest()

for a in range(32, 127):
    for b in range(32, 127):
        s = chr(a) + chr(b)
        digests[s] = hashlib.md5(s.encode()).hexdigest()
# flag{md5_1s_re41ly_1n5ecur3}


def match(a: str, b: str) -> bool:
    for i in range(len(a)):
        if a[i] in string.digits and a[i] != b[i]:
            return False
    return True


def get_father(f, x):
    if f[x] == x:
        return x
    else:
        f[x] = get_father(f, f[x])
        return f[x]


def union(f, a, b):
    f[get_father(f, b)] = get_father(f, a)


def most_frequent(l):
    d = collections.defaultdict(int)
    for x in l:
        d[x] += 1
    ll = sorted(d.items(), key=lambda t: t[1], reverse=True)
    print(ll)
    if len(ll) == 1 or ll[0][1] > ll[1][1]:
        return ll[0][0]
    return None


def main() -> None:
    plaintext = []
    matched_lines = {}
    with open('crypt2.txt', 'r') as f:
        line_number = 0
        for line in f:
            matched = False
            for k, v in digests.items():
                if match(line.rstrip('\n'), v):
                    plaintext.append(k)
                    matched = True
                    break
            if not matched:
                plaintext.append('?')
            if matched:
                matched_lines[line_number] = v
            line_number += 1
    print(repr(''.join(plaintext)))
    # print(matched_lines)
    # The MD5??sag?di???l?r?????c?pto?????y??k?????w???u????????n??????28-b???v??.??{m?_1??4??????}??????????????????????????????????,?????f??????????x???????????
    # https://en.wikipedia.org/wiki/MD5
    # The MD5 message-digest algorithm is a cryptographically broken but still widely used hash function producing a 128-bit hash value
    # The MD5 message-digest algorithm is a cryptographically broken?t ??widely used hash function p?ucing ?28-b??h value.?ag{md5_1s_re41ly_1n5ecur3} Althoug?D5 was?????gned to be u???crypto?phic h??nction,???een found? suffer from extensive vulnerabil?s.
    father = list(range(26))
    appearance = collections.defaultdict(list)
    with open('crypt2.txt', 'r') as f:
        line_number = 0
        phase = 0
        for line in f:
            # if line_number in matched_lines:
            #     assert match(line.rstrip('\n'), matched_lines[line_number])
            for i, c in enumerate(line):
                if c in string.ascii_lowercase:
                    if line_number in matched_lines:
                        appearance[c].append(phase)
                        union(father, ord(c) - ord('a'), ord(matched_lines[line_number][i]) - ord('a'))
                    phase += 1
            line_number += 1
    visited = [False] * 26
    for i in range(26):
        if not visited[i]:
            s = ''
            for j in range(26):
                if get_father(father, i) == get_father(father, j):
                    s += chr(ord('a') + j)
                    visited[j] = True
            # print(s)
            # abcdefghijklmnopqrstuvwxyz
    diffs = []
    print(appearance)
    for v in appearance.values():
        for i in range(1, len(v)):
            diffs.append(v[i] - v[i - 1])
    # print(diffs)
    # print(math.gcd(*diffs))
    # 1
    # The data is tampered
    for c, l in appearance.items():
        print(c, most_frequent([x % 26 for x in l]))
    # key = ['?'] * 26
    # for k, v in appearance.items():
    #     key[v[0] % 26] = k
    # print(''.join(key))



if __name__ == "__main__":
    main()
