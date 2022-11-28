import typing

from prob import TUDOU, BYTEMARK, Decrypt

Start = '佛曰：'
All_characters = TUDOU + BYTEMARK


def read_japanese(filename: str) -> str:
    with open(filename, 'rb') as f:
        b = f.read()
    return b.decode('utf-8')

count = 0

def search(japanese: str, cipher_text: typing.List[str]) -> None:
    global count
    count += 1
    if count % 10000 == 0:
        print(count)
    for c in All_characters:
        # possible optimization: only consider the end
        cipher_text.append(c)
        joined_cipher_text = ''.join(cipher_text)
        new_japanese = joined_cipher_text.encode('utf-8').decode("shift_jis",errors="ignore")
        if japanese == new_japanese:
            print(joined_cipher_text)
            try:
                print(Decrypt(joined_cipher_text))
            except UnicodeDecodeError as e:
                print(e)
        elif (japanese.startswith(new_japanese)
            or (len(new_japanese) < len(japanese)
                and len(new_japanese[-1].encode('shift_jis')) == 1)
                and japanese.startswith(new_japanese[:-1])):
            # The last Japanese character may change when new character is
            # appended.
            search(japanese, cipher_text)
        cipher_text.pop()


def main() -> None:
    japanese = read_japanese('flag1.enc')
    # flag{s1mp1e_Tud0uc0d3}
    # japanese = read_japanese('flag2.enc')
    # RecursionError
    # import sys
    # sys.setrecursionlimit(100000)
    # Crashes silently, return value is 127.
    cipher_text = [Start]
    search(japanese, cipher_text)
    print(count)
    # 279


if __name__ == "__main__":
    main()
