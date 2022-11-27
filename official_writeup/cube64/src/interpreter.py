#!/usr/bin/env python3


from dataclasses import dataclass
from enum import Enum, auto, unique
import sys
from typing import List, Tuple, Union
from encrypt import b64_int_to_ascii


'''
NOP:  0000000
DUP:  0000001
SWAP: 0000010
LD:   0000011
ST:   0000100
OUT:  0000101
HALT: 0000110
INC:  0000111
ADD:  0001000
SUB:  0001001
AND:  0001010
OR:   0001011
NOT:  0001100
XOR:  0001101
SHL:  0001110
SHR:  0001111
SAR:  0010000
LT:   0010001
LTU:  0010010
EQ:   0010011
BT:   0100XXX
BF:   0101XXX
J:    0110XXX
LI:   1XXXXXX
'''


@unique
class Direction(Enum):
  XP = 0
  XN = 1
  YP = 2
  YN = 3
  ZP = 4
  ZN = 5


@unique
class OpCode(Enum):
  NOP = auto()
  DUP = auto()
  SWAP = auto()
  LD = auto()
  ST = auto()
  OUT = auto()
  HALT = auto()
  INC = auto()
  ADD = auto()
  SUB = auto()
  AND = auto()
  OR = auto()
  NOT = auto()
  XOR = auto()
  SHL = auto()
  SHR = auto()
  SAR = auto()
  LT = auto()
  LTU = auto()
  EQ = auto()
  BT = auto()
  BF = auto()
  J = auto()
  LI = auto()


Operand = Union[Direction, int, None]


@dataclass(frozen=True)
class DebugInfo:
  stack_write_en: bool
  stack_write_sp: int
  stack_write_data_en: bool
  stack_write_data: int
  stack_swap: bool

  def __str__(self) -> str:
    def b2s(b): return 't' if b else 'f'
    wen = b2s(self.stack_write_en)
    wden = b2s(self.stack_write_data_en)
    swap = b2s(self.stack_swap)
    return f'{wen} {self.stack_write_sp} {wden} {self.stack_write_data} {swap}'


Trace = List[DebugInfo]


class CPU:
  def __init__(self, rom: bytes) -> None:
    assert len(rom) == 16 ** 3
    self.__rom = list(rom)
    self.mem = [0] * 2 ** 6
    self.__stack = [0] * 32
    self.__sp = 0
    self.__x = 0
    self.__y = 0
    self.__z = 0
    self.__dir = Direction.XP
    self.__output = []
    self.__halt = False

  @property
  def output(self) -> List[int]:
    return self.__output

  def run(self) -> Trace:
    trace = []
    while not self.__halt:
      trace.append(self.step())
    return trace

  def step(self) -> DebugInfo:
    # fetch
    pc = self.__z * 16 ** 2 + self.__y * 16 + self.__x
    inst = self.__rom[pc]
    # decode
    opcode, opr = CPU.__decode(inst)
    # execute
    self.__execute(opcode, opr)
    # update position
    xo, yo, zo = {
        Direction.XP: (1, 0, 0),
        Direction.XN: (-1, 0, 0),
        Direction.YP: (0, 1, 0),
        Direction.YN: (0, -1, 0),
        Direction.ZP: (0, 0, 1),
        Direction.ZN: (0, 0, -1),
    }[self.__dir]
    self.__x = (self.__x + xo) % 16
    self.__y = (self.__y + yo) % 16
    self.__z = (self.__z + zo) % 16
    # generate debug information
    return self.__gen_debug(opcode)

  @staticmethod
  def __decode(inst: int) -> Tuple[OpCode, Operand]:
    if inst & 0b1100000 == 0b0000000:
      opcode = [
          OpCode.NOP,
          OpCode.DUP,
          OpCode.SWAP,
          OpCode.LD,
          OpCode.ST,
          OpCode.OUT,
          OpCode.HALT,
          OpCode.INC,
          OpCode.ADD,
          OpCode.SUB,
          OpCode.AND,
          OpCode.OR,
          OpCode.NOT,
          OpCode.XOR,
          OpCode.SHL,
          OpCode.SHR,
          OpCode.SAR,
          OpCode.LT,
          OpCode.LTU,
          OpCode.EQ,
      ][inst & 0b0011111]
      opr = None
    elif inst & 0b1100000 == 0b0100000:
      opcode = [
          OpCode.BT,
          OpCode.BF,
          OpCode.J,
      ][(inst >> 3) & 0b11]
      opr = [
          Direction.XP,
          Direction.XN,
          Direction.YP,
          Direction.YN,
          Direction.ZP,
          Direction.ZN,
      ][inst & 0b111]
    else:
      opcode = OpCode.LI
      opr = inst & 0b0111111
    return (opcode, opr)

  def __gen_debug(self, opcode: OpCode) -> DebugInfo:
    is_swap = opcode == OpCode.SWAP
    no_result = {
        OpCode.NOP,
        OpCode.SWAP,
        OpCode.ST,
        OpCode.OUT,
        OpCode.HALT,
        OpCode.BT,
        OpCode.BF,
        OpCode.J,
    }
    return DebugInfo(not is_swap, self.__sp, opcode not in no_result,
                     self.__peek(), is_swap)

  def __execute(self, opcode: OpCode, opr: Operand) -> None:
    if opcode == OpCode.NOP:
      pass
    elif opcode == OpCode.DUP:
      self.__push(self.__peek())
    elif opcode == OpCode.SWAP:
      x = self.__pop()
      y = self.__peek()
      self.__poke(x)
      self.__push(y)
    elif opcode == OpCode.LD:
      addr = self.__peek()
      self.__poke(self.mem[addr])
    elif opcode == OpCode.ST:
      addr = self.__pop()
      self.mem[addr] = self.__pop()
    elif opcode == OpCode.OUT:
      self.__output.append(self.__pop())
    elif opcode == OpCode.HALT:
      self.__halt = True
      return
    elif opcode == OpCode.INC:
      self.__poke((self.__peek() + 1) & 0b111111)
    elif opcode == OpCode.NOT:
      self.__poke(~self.__peek())
    elif opcode == OpCode.BT:
      assert isinstance(opr, Direction)
      if self.__pop() != 0:
        self.__dir = opr
    elif opcode == OpCode.BF:
      assert isinstance(opr, Direction)
      if self.__pop() == 0:
        self.__dir = opr
    elif opcode == OpCode.J:
      assert isinstance(opr, Direction)
      self.__dir = opr
    elif opcode == OpCode.LI:
      assert isinstance(opr, int)
      self.__push(opr)
    else:
      rhs = CPU.__sign_ext(self.__pop())
      lhs = CPU.__sign_ext(self.__peek())
      if opcode == OpCode.ADD:
        ans = lhs + rhs
      elif opcode == OpCode.SUB:
        ans = lhs - rhs
      elif opcode == OpCode.AND:
        ans = lhs & rhs
      elif opcode == OpCode.OR:
        ans = lhs | rhs
      elif opcode == OpCode.XOR:
        ans = lhs ^ rhs
      elif opcode == OpCode.SHL:
        ans = lhs << (rhs & 0b111)
      elif opcode == OpCode.SHR:
        ans = (lhs & 0b111111) >> (rhs & 0b111)
      elif opcode == OpCode.SAR:
        ans = lhs >> (rhs & 0b111)
      elif opcode == OpCode.LT:
        ans = int(lhs < rhs)
      elif opcode == OpCode.LTU:
        ans = int((lhs & 0b111111) < (rhs & 0b111111))
      elif opcode == OpCode.EQ:
        ans = int(lhs == rhs)
      else:
        assert False
      self.__poke(ans & 0b111111)

  def __push(self, x: int) -> None:
    self.__sp += 1
    self.__poke(x)

  def __pop(self) -> int:
    x = self.__peek()
    self.__sp -= 1
    return x

  def __poke(self, x: int) -> None:
    self.__stack[self.__sp] = x

  def __peek(self) -> int:
    return self.__stack[self.__sp]

  @staticmethod
  def __sign_ext(x: int) -> int:
    return ~0b111111 | x if x & 0b100000 else x


'''
# i = 0
li 0

# generate `cur`
dup
li 3
and
# generate `output`
dup
ld
li {data_x}
xor
out
# swap keys in memory
# store key at `cur` to memory
dup
ld
dup
li -1
st
# store `cur` to memory
swap
li -2
st
# generate `target`
li 3
and
# store key at `target` to `cur`
dup
ld
li -2
ld
st
# store key at `cur` to `target`
li -1
ld
swap
st
# i = i + 1
inc

# stop
halt
'''


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print(f'usage: {sys.argv[0]} ROM TRACE')
    exit(1)
  with open(sys.argv[1], 'rb') as f:
    cpu = CPU(f.read())
    cpu.mem[0] = 0b100100
    cpu.mem[1] = 0b111001
    cpu.mem[2] = 0b100101
    cpu.mem[3] = 0b101110
    trace = cpu.run()
    print(bytes(map(b64_int_to_ascii, cpu.output)).decode())
  with open(sys.argv[2], 'w') as f:
    f.write('\n'.join(map(str, trace)))
