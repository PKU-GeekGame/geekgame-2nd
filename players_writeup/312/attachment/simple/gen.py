import capstone
import subprocess
import base64


if __name__ == "__main__":
    code = ""
    l = []
    with open("code.asm", "r") as f:
        for line in f.readlines():

            _line = line.strip().split()
            for x in _line:
                l.append(int("0x"+x, 16))
    code = bytes(l)
    real_code = []
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.skipdata = True
    pos = 0
    for inst in md.disasm(code, 0):
        # print("0x%x+%d:\t%s\t%s" % (inst.address, inst.size, inst.mnemonic, inst.op_str))
        sz = inst.size
        real_code += [0xe9, 5-sz, 0, 0, 0]
        real_code += [0xe9]
        for x in range(4-sz):
            real_code += [0]
        for x in range(sz):
            real_code += [l[pos]]
            pos += 1
    assert(pos == len(code))
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.skipdata = True
    print(base64.b64encode(bytes(real_code)))
    # for inst in md.disasm(bytes(real_code), 0):
    #     print("0x%x+%d:\t%s\t%s" % (inst.address, inst.size, inst.mnemonic, inst.op_str))
