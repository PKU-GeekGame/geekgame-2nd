from pathlib import Path

prob_template='''
flag=input("Flag: ").encode()
if len(set(flag)-set(range(127)))>0:
    print("Wrong")
else:
    num=int.from_bytes(flag,"big")^NNN
    num_len=len(hex(num))-2
    for i in range(1,num_len+1):
        if (num>>((num_len-i)*4))%i>0:
            print("Wrong")
            exit()
    print("Correct")
'''

def gen(user, chall) -> Path:
    flag = [f.correct_flag(user) for f in chall.flags][0]
    assert 20<=len(flag)<=25
    n=int.from_bytes(flag.encode(),"big")
    import random
    n=str(random.choice([18872900738885736149574055538327802527212537551, 60753927368683934227793588395570842550542338031, 89515749136034833729775437005460258167590093634])^n)
    p = Path('_gen') / f'{user._store.id}.txt'
    p.parent.mkdir(exist_ok=True)
    with p.open('w') as f:
        f.write(prob_template.replace("NNN",n).strip())
    return p