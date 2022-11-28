import sys


def main() -> None:
    with open(sys.argv[1], 'rb') as f:
        c = f.read()
    offset = 200
    # pad to multiple of 8
    c = c + b'\x00' * ((8 - len(c) % 8) % 8)
    # https://9to5answer.com/difference-between-movq-and-movabsq-in-x86-64
    # movabsq means that the machine-code encoding will contain a 64-bit value
    # Even if the number is small, like movabs $1, %rax, you still get the 10-byte version
    # capstone reports movabs and mov
    # for i in range(0, len(c), 8):
    #     print(f'movabsq\t$0x{bytes(reversed(c[i: i+8])).hex()}, %rax')
    #     print(f'mov\t%rax, {offset+i}(%rdx)')
    for i in range(0, len(c), 4):
        print(f'movl\t$0x{bytes(reversed(c[i: i+4])).hex()}, {offset+i}(%rdx)')


if __name__ == "__main__":
    main()
