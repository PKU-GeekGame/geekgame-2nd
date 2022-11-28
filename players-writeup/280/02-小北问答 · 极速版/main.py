import pwn
import sympy
import time

with open('../token.txt', 'rb') as f:
    token = f.readline().rstrip(b'\n')

def main() -> None:
    # pwn.context(log_level='debug')
    next_zip_code = 0
    while True:
        c = pwn.remote('prob01.geekgame.pku.edu.cn', 10001)
        if token:  # Pylance deems code following sendline to be unreachable
            c.sendlineafter(b'Please input your token: ', token)
        if token:  # Pylance deems code following sendline to be unreachable
            c.sendlineafter(b'> ', '急急急'.encode())
        for _ in range(7):
            print(c.recvuntil(' 题：'.encode()).decode())
            description = c.recvline().decode()
            print(f'{description=}')
            known_answers = {
                'Firefox': '65',
                'PKU Runner': 'cn.edu.pku.pkurunner',
                'BV1EV411s7vu': '418645518',
                'gStore': '10.14778/2002974.2002976',
                'http://ctf.世界一流大学.com': 'ctf.xn--4gqwbu44czhc7w9a66k.com',
            }

            answer = None
            for part, known_answer in known_answers.items():
                if part in description:
                    answer = known_answer
                    break

            if 'd2:94:35:21:42:43' in description:
                answer = f'{next_zip_code:05d}'
                next_zip_code += 1
            elif '之间的质数' in description:
                _, lower_bound_str, _, upper_bound_str, _ = description.split()
                lower_bound = int(lower_bound_str)
                upper_bound = int(upper_bound_str)
                for x in range(lower_bound, upper_bound + 1):
                    if sympy.ask(sympy.Q.prime(x)):
                        # Just pick the first one
                        answer = str(x)
                        break
            elif '《电子游戏概论》' in description:
                # https://github.com/PKU-GeekGame/geekgame-1st/blob/master/src/pygame/game/server/libtreasure.py#L19
                GOAL_OF_LEVEL = lambda level: 300+int(level**1.5)*100
                level = int(description.split()[-2])
                answer = str(GOAL_OF_LEVEL(level))

            if answer is None:
                print(f'Unknown problem {description}')
                answer = '?'

            print(f'{answer=}')
            if token:  # Pylance deems code following sendline to be unreachable
                c.sendline(answer.encode())
            c.recvuntil(b'> ')
            result_text = c.recvline().decode()
            print(f'{result_text=}')
            if 'd2:94:35:21:42:43' in description and '答案正确' in result_text:
                print(f'{next_zip_code=}')
                exit()
        final_result = c.recvall().decode()
        print(f'{final_result=}')
        if final_result.count('flag') > 1:
            break
        # flag{i-aM-the-KIng-of-anxietY}
        # flag{noW-you-hAve-leaRnt-hoW-to-use-pwntools}
        time.sleep(30 / 3)


if __name__ == "__main__":
    main()
