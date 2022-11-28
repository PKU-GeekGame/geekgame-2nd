from Crypto.Util.number import long_to_bytes

m = 2511413510804011656777027853309658460397322340334414819647
# print(len(hex(m)) - 2)
# Subtracting 2 removes the prefix "0x"
# 48

# (num >> ((num_len - 1) * 4)) % 1
# (num >> ((num_len - 2) * 4)) % 2
# ...
# (num >> 0) % num_len
# The leftmost i hex digits need to be multiple of i.

# while m > 0:
#     print(m % 2 ** 8)
#     m >>= 8
# The 6th is 200, so we can't just make num 0.

# for i in range(999):
#     byte = m % 2 ** 8
#     if byte >= 127:
#         print(i, byte)
#     m >>= 8
#     if m == 0:
#         break
# 9 226
# 10 140
# 13 215
# 15 226
# 18 200
# The most significant bit of each byte can not be controlled. So the minimum
# length is 19 * 2 = 38 hex digits.

# km * 16 + x = (k+1)n
# 16mk + x = nk + n
# (16m - n)k = n - x
# Uh, this doesn't help.

print(long_to_bytes(m))
# b"flagt\xc8I\x12\xe2J\xd7+f\x8c\xe2\rTdZkA'q?"
# So I guess the input will be flag{...}
# print(len(long_to_bytes(m)))
# 24
# print(ord('t') ^ ord('{'))
# 15
# print(ord('?') ^ ord('}'))
# 66
# 4 zeros, 15, then 18 bytes, 66, that's 39 hex digits in total

count = 0
def solve(i: int, x: int) -> None:
    """finding ith (starts from 1) hex digit, current number is x"""
    global count
    count += 1
    # print(f'{i=} {x=}')
    # if i > 3:
    #     exit()
    if i == 39 - 1:
        if ((x << 4) | (66 >> 4)) % 38 == 0 and ((x << 8) | 66) % 39 == 0:
            ans = (x << 8) | 66
            print(ans)
            print(long_to_bytes(ans ^ m))
            # flag{fOund_magiC_nUmBer}
            exit()
        return
    start = (i - (x << 4) % i) % i
    # TODO: Add constraint
    for digit in range(start, 2 ** 4, i):
        solve(i + 1, (x << 4) | digit)

solve(2, 15)
print(count)
