import collections
import math
import re

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# key = "BCA"
# keymap={letters[i]:key[i] for i in range(3)}
# current_key={letters[i]:letters[i] for i in range(3)}
# for i in range(3):
#     print(current_key)
#     current_key={i:keymap[current_key[i]] for i in current_key}
# exit()

def main() -> None:
    with open('crypt1.txt', 'r') as f:
        c = f.read()
    single_words = []
    for m in re.finditer(' ([a-z])\W', c):
        single_words.append((m.span()[0] + 1))
    # print(len(single_words))
    # print(repr(c[single_words[0] - 1: single_words[0] + 2]))
    appearance = collections.defaultdict(list)
    phase = 0
    for i in range(len(c)):
        if i in single_words:
            appearance[c[i]].append(phase)
        if c[i].upper() in letters:
            phase += 1
    # print(len(appearance))
    # 20
    # print(appearance)
    diffs = []
    for v in appearance.values():
        for i in range(1, len(v)):
            diffs.append(v[i] - v[i - 1])
    print(diffs)
    print(math.gcd(*diffs))
    # 22
    # observed = dict((k, v[0] % 22) for k, v in appearance.items())
    partial = ['?'] * 22
    for k, v in appearance.items():
        partial[v[0] % 22] = k
    print(partial)
    # print(set(letters.lower()) - set(partial))
    # vdrumj
    phase = 0
    # for offset in range(22):
    if True:
        partial[partial.index('?')] = 'r'
        partial[partial.index('?')] = 'm'
        plaintext = []
        for i in range(len(c)):
            if c[i].lower() in partial:
                plaintext.append(partial[(partial.index(c[i].lower()) - phase % 22 + 22) % 22])
                if c[i] in letters:
                    plaintext[-1] = plaintext[-1].upper()
            else:
                plaintext.append(c[i])
            if c[i].upper() in letters:
                phase += 1
        # with open(f'{offset}.txt', 'w') as f:
        with open(f'plaintext.txt', 'w') as f:
            f.write(''.join(plaintext))


if __name__ == "__main__":
    main()
