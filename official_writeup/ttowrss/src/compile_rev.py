#!/usr/bin/env python3

'''
Tool for compiling a program that runs in reverse order.

Your program should be written in a single C file, and include `rev.h`.
A Dockerfile is also provided to run this script.

Written by MaxXing, 2022-10.
License GPL-v3.
'''

from math import ceil
from os import path
import os
import random
import re
import shlex
import subprocess
from typing import Dict, List, Optional, Tuple


# Garbage instructions, used to fill the gaps in the reversed program.
GARBAGE_INSTS = [
    'testl\t%edx, %edx',
    'cmpl\t$1, %eax',
    'retq',
    'shlq\t$4, %rcx',
    'movl\t8(%rcx,%rdx), %esi',
    'popq\t%rbx',
    'movslq\t%edi, %r8',
    'movabsq\t$4294967296, %rsi',
    'addq\t%rdi, %r10',
    'xorl\t%edx, %edx',
    'pushq\t%rax',
    'notl\t%eax',
    'cltd',
    'idivl\t%ecx',
    'incl\t%edi',
    'vmovsd\t%xmm0, 72(%rsp)',
    'vcvtsi2sd\t%ebx, %xmm1, %xmm1',
    'vsubsd\t24(%rsp), %xmm0, %xmm0',
    'vcvttsd2si\t%xmm0, %ebp',
    'vmulsd\t%xmm1, %xmm0, %xmm0',
    'vdivsd\t%xmm1, %xmm0, %xmm0',
    'movzwl\t%r15w, %r15d',
    'movb\t$4, %al',
    'vcvttpd2dqx\t80(%rsp), %xmm0',
    'vxorpd\t%xmm0, %xmm0, %xmm0',
    'vfnmadd213sd\t40(%rsp), %xmm0, %xmm7',
    'vfmadd213sd\t72(%rsp), %xmm1, %xmm0',
    'vucomisd\t%xmm5, %xmm6',
    'decl\t%r12d',
    'vpsrlw\t$4, %xmm1, %xmm2',
    'vextracti128\t$1, %ymm3, %xmm4',
    'vpshufd\t$238, %xmm3, %xmm3',
    'vpand\t%xmm0, %xmm1, %xmm1',
]


# Functions that should be skipped when reversing a program.
# Must sync with the `rev.h`.
SKIPPED_FUNCS = {
    'rev_is_inst_start',
    'rev_signal_handler',
    'rev_toggle_tf',
    'rev_initialize',
    'rev_terminate',
}


# Regex to match functions in assembly.
RE_FUNC = re.compile(r'^\s+\.type\s+(\w+), @function\n((.+\n)+?)^\s+\.size\s+(\w+).+$',
                     re.MULTILINE)


# Type of a label list.
Labels = List[str]

# Type of an instruction-labels pair.
InstLabels = Tuple[str, Labels]


def run_or_fail(cmd: str, stdin: Optional[str] = None) -> str:
  '''
  Runs the given command line, abort if error returned.

  Returns the standard output.
  '''
  ret = subprocess.run(shlex.split(cmd), input=stdin,
                       capture_output=True, text=True)
  if ret.returncode:
    raise RuntimeError(f'failed to run "{cmd}", returned {ret.returncode}')
  return ret.stdout


def gen_linker_script(ld_file: str):
  '''
  Generates linker script to the given script file.
  '''
  # get verbose output of the linker
  out = run_or_fail('gcc -x c - -o /dev/null -Wl,--verbose', 'int main() {}')
  # generate linker script
  with open(ld_file, 'w') as f:
    in_lds = False
    in_text = False
    # for each line in the output
    for line in out.splitlines(keepends=True):
      if line.startswith('=' * 10):
        # begin or end of the linker script
        if not in_lds:
          in_lds = True
        else:
          break
      elif in_lds:
        if line.strip().startswith('.text'):
          # begin of the text section
          in_text = True
          f.write('  PROVIDE (rev_text_start = .);\n')
          f.write(line)
        elif in_text and line.strip() == '}':
          # end of the text section
          in_text = False
          f.write(line)
          f.write('  PROVIDE (rev_text_end = .);\n')
        else:
          # other lines
          f.write(line)


def compile(c_file: str, asm_file: str, bitmap_size: Optional[int] = None, trace: bool = False):
  '''
  Compiles the given C source file to assembly,
  stores the compiled assembly to the given file.
  '''
  define = '' if bitmap_size is None else f'-DREV_BITMAP_SIZE={bitmap_size}'
  define += ' -DREV_TRACE' if trace else ''
  flags = '-I. -O3'
  flags += ' -fno-asynchronous-unwind-tables -fno-dwarf2-cfi-asm -fcf-protection=none'
  flags += ' -fno-reorder-blocks-and-partition -fno-align-loops -fno-align-labels'
  flags += ' -fno-align-jumps'
  run_or_fail(f'gcc {c_file} -S -o {asm_file} {define} {flags}')


def find_funcs(asm: str) -> Dict[str, List[InstLabels]]:
  '''
  Finds out all functions from the given assembly.

  Returns a dictionary which key is function name and
  value is a list of instruction-labels pairs in the function.
  '''
  funcs = {}
  for func_name, func_asm, _, func_name2 in RE_FUNC.findall(asm):
    # check if matched a valid function
    if func_name != func_name2:
      raise RuntimeError(f'something wrong in finding functions')
    # get instruction-labels pairs
    func_asm: str
    inst_labels = []
    last_labels = []
    for line in func_asm.splitlines():
      line = line.strip()
      if line.endswith(':'):
        # label found
        last_labels.append(line)
      elif line.startswith('.'):
        # directive found
        raise RuntimeError(f'unexpected directive "{line}" in assembly')
      elif not line.startswith('#'):
        # instruction found
        inst_labels.append((line, last_labels))
        last_labels = []
    # add to the dictionary
    funcs[func_name] = inst_labels
  return funcs


def reverse_inst_labels(inst_labels: List[InstLabels]) -> List[InstLabels]:
  '''
  Reverses the given instruction-labels list and returns the reversed list.
  '''
  # insert two garbage instructions to the beginning of the list
  for _ in range(2):
    inst = random.choice(GARBAGE_INSTS)
    inst_labels.insert(0, (inst, []))
  # shift labels
  for i, (inst, _) in enumerate(inst_labels):
    inst_labels[i] = (inst, inst_labels[i + 2][1]
                      if i + 2 < len(inst_labels) else [])
  # reverse
  inst_labels.reverse()
  return inst_labels


def gen_func_asm(inst_labels: List[InstLabels]) -> str:
  '''
  Generates the assembly for the given instruction-labels list.
  '''
  asms = []
  for inst, labels in inst_labels:
    labels_asm = '\n'.join(labels) + '\n' if labels else ''
    asms.append(f'{labels_asm}\t{inst}')
  return '\n'.join(asms)


def reverse_asm(asm_file: str):
  '''
  Reverses the given assembly file (in place).
  '''
  # initialize random seed
  random.seed(asm_file)
  # get the content of the assembly file
  with open(asm_file, 'r') as f:
    asm = f.read()
  # find all functions
  funcs = find_funcs(asm)
  # reverse and generate assembly for all functions
  func_asms = {}
  for name, inst_labels in funcs.items():
    if name in SKIPPED_FUNCS:
      func_asms[name] = gen_func_asm(inst_labels)
    else:
      func_asm = gen_func_asm(reverse_inst_labels(inst_labels))
      func_asms[name] = f'{name}$begin:\n{func_asm}\n{name}$end:'
  # apply to the original assembly
  asm = RE_FUNC.sub('{{\\1}}', asm)
  for name, func_asm in func_asms.items():
    asm = re.sub(f'^\\{{\\{{{name}\\}}\\}}$',
                 func_asm, asm, flags=re.MULTILINE)
  # write to file
  with open(asm_file, 'w') as f:
    f.write(asm)


def asm_link(asm_file: str, ld_file: str, exe_file: str):
  '''
  Assembles and links the given assembly file by the given linker script,
  generates the executable file to the given path.
  '''
  run_or_fail(f'gcc {asm_file} -o {exe_file} -Wl,-T{ld_file} -lm')


def get_sym_addr(exe_file: str, sym: str) -> int:
  '''
  Returns the address of the given symbol in the executable.
  '''
  addr = None
  for line in run_or_fail(f'readelf -s {exe_file}').splitlines():
    cols = re.split(r'\s+', line.strip())
    if cols[-1].endswith(sym):
      addr = int(cols[1], 16)
  if addr is None:
    raise RuntimeError(f'symbol "{sym}" not found in "{exe_file}"')
  return addr


def gen_bitmap(exe_file: str) -> bytes:
  '''
  Generates a bitmap for the given executable.
  '''
  # get location of the text section
  text_start = get_sym_addr(exe_file, 'rev_text_start')
  text_end = get_sym_addr(exe_file, 'rev_text_end')
  # initialize bitmap
  bitmap = [0] * ceil((text_end - text_start) / 8)
  # check the disassembly
  mark_inst = False
  for line in run_or_fail(f'objdump -S -j .text {exe_file}').splitlines():
    line = line.strip()
    if line.endswith('$begin>:'):
      # begin tag, enable instruction marking
      mark_inst = True
    elif line.endswith('$end>:'):
      # end tag, disable instruction marking
      mark_inst = False
    elif (mark_inst and ':' in line and not line.endswith('>:')
          and not line.endswith(' 00') and not line.endswith('\t00')):
      # mark the current instruction in bitmap
      ip = int(line.split(':')[0], 16)
      index = ip - text_start
      bitmap[index // 8] |= 1 << (index % 8)
  return bytes(bitmap)


def get_file_offset(exe_file: str, addr: int) -> int:
  '''
  Returns the offset in the executable file of the given address.
  '''
  # get program header info
  lines = run_or_fail(f'readelf -l {exe_file}').splitlines()
  # check all program headers
  in_phdr = False
  i = 0
  while i < len(lines):
    line = lines[i].strip()
    if not in_phdr and line == 'Program Headers:':
      # the following lines are program header info
      in_phdr = True
      i += 3
      continue
    elif in_phdr and not line:
      # end of the program header info
      break
    elif in_phdr and not line.startswith('['):
      # parse program header info
      cols = re.split(r'\s+', line)
      offset, vaddr = int(cols[1], 16), int(cols[2], 16)
      cols = re.split(r'\s+', lines[i + 1].strip())
      size = int(cols[0], 16)
      # check if the given address is in the current header
      if addr >= vaddr and addr < vaddr + size:
        return offset + addr - vaddr
      i += 2
      continue
    i += 1
  # not found
  raise RuntimeError(f'address {addr} not found in "{exe_file}"')


def write_bitmap(exe_file: str, bitmap: bytes):
  '''
  Writes the given bitmap to the executable file,
  and then strip the executable.
  '''
  # get the offset of the bitmap
  bitmap_addr = get_sym_addr(exe_file, 'rev_text_bytes')
  bitmap_offset = get_file_offset(exe_file, bitmap_addr)
  # write bitmap to file
  with os.fdopen(os.open(exe_file, os.O_WRONLY), 'wb') as f:
    f.seek(bitmap_offset)
    f.write(bitmap)
  # strip the executable
  run_or_fail(f'strip --strip-unneeded {exe_file}')


if __name__ == '__main__':
  # initialize argument parser
  import argparse
  parser = argparse.ArgumentParser(
      description='Compile script for programs using `rev.h`.')
  parser.add_argument('input', type=str, help='the input C source file')
  parser.add_argument('-o', '--output', default=None,
                      help='the output executable file')
  parser.add_argument('-t', '--trace', default=False,
                      action='store_true', help='enable trace output')

  # parse command line arguments
  args = parser.parse_args()
  c_file = path.abspath(args.input)
  exe_file = path.abspath(args.output) \
      if args.output else path.splitext(c_file)[0]
  trace = args.trace

  # get working directory and necessary file names
  wd = path.dirname(c_file)
  ld_file = path.join(wd, 'linker.ld')
  asm_file = f'{c_file}.S'
  bitmap_file = f'{c_file}.bitmap'

  # generate linker script if does not exist
  if not path.exists(ld_file):
    gen_linker_script(ld_file)

  # stage 1: compile, reverse and link
  compile(c_file, asm_file, trace=trace)
  reverse_asm(asm_file)
  asm_link(asm_file, ld_file, exe_file)

  # stage 2: generate bitmap
  bitmap = gen_bitmap(exe_file)
  with open(bitmap_file, 'wb') as f:
    # for debugging
    f.write(bitmap)

  # stage 3: recompile, reverse and link
  compile(c_file, asm_file, trace=trace, bitmap_size=len(bitmap))
  reverse_asm(asm_file)
  asm_link(asm_file, ld_file, exe_file)

  # stage 4: verify and write bitmap
  assert gen_bitmap(exe_file) == bitmap
  write_bitmap(exe_file, bitmap)
