#!/usr/bin/env python3


import sys


INSTS = [
    # name, mask,     opcode
    ('nop', 0b1111111, 0b0000000),
    ('dup', 0b1111111, 0b0000001),
    ('swap', 0b1111111, 0b0000010),
    ('ld', 0b1111111, 0b0000011),
    ('st', 0b1111111, 0b0000100),
    ('out', 0b1111111, 0b0000101),
    ('halt', 0b1111111, 0b0000110),
    ('inc', 0b1111111, 0b0000111),
    ('add', 0b1111111, 0b0001000),
    ('sub', 0b1111111, 0b0001001),
    ('and', 0b1111111, 0b0001010),
    ('or', 0b1111111, 0b0001011),
    ('not', 0b1111111, 0b0001100),
    ('xor', 0b1111111, 0b0001101),
    ('shl', 0b1111111, 0b0001110),
    ('shr', 0b1111111, 0b0001111),
    ('sar', 0b1111111, 0b0010000),
    ('lt', 0b1111111, 0b0010001),
    ('ltu', 0b1111111, 0b0010010),
    ('eq', 0b1111111, 0b0010011),
    ('bt', 0b1111000, 0b0100000),
    ('bf', 0b1111000, 0b0101000),
    ('j', 0b1111000, 0b0110000),
    ('li', 0b1000000, 0b1000000),
]


DIRS = [
    'xp',
    'xn',
    'yp',
    'yn',
    'zp',
    'zn',
]


def decode_dir(b: int) -> str:
  return ['xp', 'xn', 'yp', 'yn', 'zp', 'zn'][b & 0b111]


def decode_imm(b: int) -> str:
  imm = b & 0b0111111
  if imm & 0b100000:
    imm = -((~imm + 1) & 0b111111)
  return str(imm)


def decode_byte(b: int) -> str:
  for name, mask, opcode in INSTS:
    if b & mask == opcode:
      if name in ['bt', 'bf', 'j']:
        return f'{name} {decode_dir(b)}'
      elif name == 'li':
        return f'{name} {decode_imm(b)}'
      else:
        return name
  raise RuntimeError('unknown byte')


def decode_file(file: str) -> str:
  with open(file, 'rb') as f:
    bs = f.read()
    asm = []
    for z in range(16):
      plane = []
      for y in range(16):
        line = []
        for x in range(16):
          line.append(decode_byte(bs[z * 16 ** 2 + y * 16 + x]))
        plane.append(','.join(line))
      asm.append('\n'.join(plane))
  return '\n\n'.join(asm)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} ROM')
    exit(1)

  print(decode_file(sys.argv[1]))
