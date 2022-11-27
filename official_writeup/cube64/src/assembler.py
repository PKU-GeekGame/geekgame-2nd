#!/usr/bin/env python3


import sys


OPCODES = {
    'nop': 0b0000000,
    'dup': 0b0000001,
    'swap': 0b0000010,
    'ld': 0b0000011,
    'st': 0b0000100,
    'out': 0b0000101,
    'halt': 0b0000110,
    'inc': 0b0000111,
    'add': 0b0001000,
    'sub': 0b0001001,
    'and': 0b0001010,
    'or': 0b0001011,
    'not': 0b0001100,
    'xor': 0b0001101,
    'shl': 0b0001110,
    'shr': 0b0001111,
    'sar': 0b0010000,
    'lt': 0b0010001,
    'ltu': 0b0010010,
    'eq': 0b0010011,
    'bt': 0b0100000,
    'bf': 0b0101000,
    'j': 0b0110000,
    'li': 0b1000000,
}

DIRS = {
    'xp': 0,
    'xn': 1,
    'yp': 2,
    'yn': 3,
    'zp': 4,
    'zn': 5,
}


def gen_inst(inst: str) -> int:
  ops = inst.split()
  op = ops[0].lower()
  opcode = OPCODES[op]
  if op in ['bt', 'bf', 'j']:
    dir = DIRS[ops[1].lower()]
    return opcode | dir
  elif op == 'li':
    imm = int(ops[1], 0) & 0b111111
    return opcode | imm
  else:
    return opcode


def gen_asm(file: str) -> bytes:
  with open(file, 'r') as f:
    rom = []
    for l in f.readlines():
      l = l.strip()
      if l:
        insts = l.split(',')
        assert len(insts) == 16
        for inst in insts:
          rom.append(gen_inst(inst.strip()))
    assert len(rom) <= 16 ** 3
    if len(rom) < 16 ** 3:
      rom += [gen_inst('nop')] * (16 ** 3 - len(rom))
  return bytes(rom)


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print(f'usage: {sys.argv[0]} ASM_FILE OUTPUT')
    exit(1)
  with open(sys.argv[2], 'wb') as f:
    f.write(gen_asm(sys.argv[1]))
