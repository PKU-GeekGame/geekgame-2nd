#!/usr/bin/env python3


from base64 import b64decode, b64encode
from typing import List


def ascii_to_b64_int(c: int) -> int:
  if c >= ord('A') and c <= ord('Z'):
    return c - ord('A')
  if c >= ord('a') and c <= ord('z'):
    return c - ord('a') + 26
  if c >= ord('0') and c <= ord('9'):
    return c - ord('0') + 52
  if c == ord('+'):
    return 62
  if c == ord('/'):
    return 63
  raise RuntimeError('invalid base64 character')


def encrypt(flag: str, key: int) -> List[int]:
  ks = [
      (key >> 0) & 0b111111,
      (key >> 6) & 0b111111,
      (key >> 12) & 0b111111,
      (key >> 18) & 0b111111,
  ]
  ans = []
  for i, b in enumerate(b64encode(flag.encode())):
    cur = i & 0b11
    target = ks[cur] & 0b11
    ans.append(ascii_to_b64_int(b) ^ ks[cur])
    ks[cur], ks[target] = ks[target], ks[cur]
  return ans


def b64_int_to_ascii(c: int) -> int:
  if c >= 0 and c <= 25:
    return c + ord('A')
  if c >= 26 and c <= 51:
    return c - 26 + ord('a')
  if c >= 52 and c <= 61:
    return c - 52 + ord('0')
  if c == 62:
    return ord('+')
  if c == 63:
    return ord('/')
  raise RuntimeError('invalid base64 character')


def decrypt(data: List[int], key: int) -> str:
  ks = [
      (key >> 0) & 0b111111,
      (key >> 6) & 0b111111,
      (key >> 12) & 0b111111,
      (key >> 18) & 0b111111,
  ]
  ans = []
  for i, b in enumerate(data):
    cur = i & 0b11
    target = ks[cur] & 0b11
    ans.append(b64_int_to_ascii(b ^ ks[cur]))
    ks[cur], ks[target] = ks[target], ks[cur]
  return b64decode(bytes(ans)).decode(errors='replace')


FIRST_PLANE = '''
nop,nop,nop,nop,nop,nop,nop,li 0,j yp,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,halt,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,li 0,nop,nop,nop,nop,nop,nop,nop
j yp,nop,nop,nop,nop,nop,nop,nop,bf xn,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
j zp,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
'''.strip()

LOOP_BODY = '''
j zp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data7},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data6},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data5},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data4},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data3},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data2},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data1},xor,out,dup,ld,dup,li -1,st,swap,j yn
j yn,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data0},xor,out,dup,ld,dup,li -1,st,swap,j yn

j xp,dup,li 3,and,dup,ld,li {data8},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data9},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data10},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data11},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data12},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data13},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data14},xor,out,dup,ld,dup,li -1,st,swap,j yp
j yp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
j xp,dup,li 3,and,dup,ld,li {data15},xor,out,dup,ld,dup,li -1,st,swap,j yp
j zp,inc,st,swap,ld,li -1,st,ld,li -2,ld,dup,and,li 3,st,li -2,j xn
'''.strip()

NOPS = '''
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
'''.strip()

LAST_PLANE = '''
j xp,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,j yp
nop,j xp,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,j yp,nop
nop,nop,j xp,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,j yp,nop,nop
nop,nop,nop,j xp,nop,nop,nop,nop,nop,nop,nop,nop,j yp,nop,nop,nop
nop,nop,nop,nop,j xp,nop,nop,nop,nop,nop,nop,j yp,nop,nop,nop,nop
nop,nop,nop,nop,nop,j xp,nop,nop,nop,nop,j yp,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,j xp,nop,nop,j yp,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,j xp,halt,nop,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,nop,j yn,nop,j xn,nop,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,nop,j yn,nop,nop,nop,j xn,nop,nop,nop,nop,nop
nop,nop,nop,nop,nop,j yn,nop,nop,nop,nop,nop,j xn,nop,nop,nop,nop
nop,nop,nop,nop,j yn,nop,nop,nop,nop,nop,nop,nop,j xn,nop,nop,nop
nop,nop,nop,j yn,nop,nop,nop,nop,nop,nop,nop,nop,nop,j xn,nop,nop
nop,nop,j yn,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,j xn,nop
nop,j yn,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,j xn
j yn,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop
'''.strip()


def gen_asm(data: List[int]) -> str:
  assert len(data) % 16 == 0
  assert len(data) // 8 + 2 <= 16
  asms = [FIRST_PLANE]
  for i in range(len(data) // 16):
    body = LOOP_BODY
    for k, d in enumerate(data[i * 16: i * 16 + 16]):
      body = body.replace(f'{{data{k}}}', str(d))
    asms.append(body)
  asms += [NOPS] * (16 - (len(data) // 8 + 2))
  asms.append(LAST_PLANE)
  return '\n\n'.join(asms)


FLAG = 'flag{s1mulat3_the_E@rth_with_A_Cube64_clus7er!!}'
KEY = 0xba5e64


if __name__ == '__main__':
  enc = encrypt(FLAG, KEY)
  assert decrypt(enc, KEY) == FLAG
  print(gen_asm(enc))
