import typing

from prob import TUDOU, BYTEMARK, Decrypt

Start = '佛曰：'
All_characters = TUDOU + BYTEMARK


def read_japanese(filename: str) -> str:
    with open(filename, 'rb') as f:
        b = f.read()
    return b.decode('utf-8')


def main() -> None:
    japanese = read_japanese('flag2.enc')
    # print(len(japanese[-1].encode('shift_jis')))
    # 2
    # Because the final character of flag2.enc is two bytes in shift_jis, when
    # we got a one-byte character, it's definitely not the end.
    start_japanese = Start.encode('utf-8').decode("shift_jis",errors="ignore")
    assert japanese.startswith(start_japanese)
    start_index = 0
    while start_index < len(japanese) - 10:
        cipher_text = [Start]
        # index_in_japanese, left_bytes, next_char_index
        stack = [[start_index, b'' if start_index > 0 else b'\x9a', 0]]
        # Possible optimization: memorize state transitions.
        # Further optimization: pre-compute all possible state transitions.
        max_cipher_text_length = 0
        longest_cipher_text = None
        largest_index_in_Japanese = 0
        while len(stack) > 0:
            index_in_japanese, left_byte, next_char_index = stack[-1]
            new_state_appended = False
            for char_index in range(next_char_index, len(All_characters)):
                char = All_characters[char_index]
                new_japanese = (left_byte + char.encode('utf-8')).decode("shift_jis",errors="ignore")
                trimmed_new_japanese = new_japanese
                # Some values aren't valid single-byte shift_jis character, but is
                # the first byte of a valid two-byte shift_jis character, so we need
                # to keep that byte and try later.
                # >>> ('佛曰：'.encode('utf-8')).decode("shift_jis",errors="ignore")
                # '菴帶峅ｼ'
                # >>> ('佛曰：麼'.encode('utf-8')).decode("shift_jis",errors="ignore")
                # '菴帶峅ｼ夐ｺｼ'
                # There may be one or two bytes discarded, but the second last
                # discarded byte is already dead, so we only keep the last discarded
                # byte.
                if (
                    len(new_japanese[-1].encode('shift_jis')) == 1
                    or new_japanese.encode('shift_jis')[-1] != char.encode('utf-8')[-1]
                ):
                    new_left_byte = bytes((char.encode('utf-8')[-1],))
                    if new_japanese[-1].encode('shift_jis') == bytes((char.encode('utf-8')[-1],)):
                        trimmed_new_japanese = new_japanese[:-1]
                else:
                    new_left_byte = b''
                new_index_in_japanese = index_in_japanese + len(trimmed_new_japanese)
                if trimmed_new_japanese != japanese[index_in_japanese: new_index_in_japanese]:
                    continue
                if index_in_japanese + len(new_japanese) == len(japanese) and japanese.endswith(new_japanese):
                    cipher_text.append(char)
                    joined_cipher_text = ''.join(cipher_text)
                    print(joined_cipher_text)
                    try:
                        plaintext = Decrypt(joined_cipher_text)
                    except UnicodeDecodeError as e:
                        print(e)
                    else:
                        print(plaintext)
                    cipher_text.pop()
                elif new_index_in_japanese < len(japanese):
                    stack[-1][2] = char_index + 1
                    cipher_text.append(char)
                    stack.append([new_index_in_japanese, new_left_byte, 0])
                    new_state_appended = True
                    if len(cipher_text) > max_cipher_text_length:
                        max_cipher_text_length = len(cipher_text)
                        longest_cipher_text = list(cipher_text)
                        largest_index_in_Japanese = new_index_in_japanese
                    break
            if not new_state_appended:
                cipher_text.pop()
                stack.pop()
        if longest_cipher_text is None:
            start_index += 1
            continue
        start_index = largest_index_in_Japanese
        for num_prepend in range(16):
            plaintext = Decrypt(''.join(longest_cipher_text), num_prepend)
            if sum(1 for c in plaintext if ord(c) < 128) >= len(plaintext) / 2:
                print(plaintext)
                break
            # Try removing 1 byte to align to utf-16
            plaintext= Decrypt(''.join((longest_cipher_text[0], *longest_cipher_text[2:])), num_prepend)
            if sum(1 for c in plaintext if ord(c) < 128) >= len(plaintext) / 2:
                print(plaintext)
    # Still no result for flag2, maybe because we pruned valid branch, making
    # count smaller?
    # Or write an automated duipai.

if __name__ == "__main__":
    main()
