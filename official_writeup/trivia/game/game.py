from flag import getflag, checktoken
import logger
import sys
import time
import os
import functools

print = functools.partial(print, flush=True)

from data import gen_problem

#token = input('Token: ')
token = os.environ['hackergame_token']
uid = checktoken(token)
if not uid:
    print('bad token!')
    sys.exit(1)
    
problems = gen_problem()
assert len(problems)==7

logger.write(uid, ['gen_problem', [x[0] for x in problems]])

print('\n欢迎来到小北问答·极速版。下面将有 7 道题目，每道题目 14 分。还有 2 分将会根据你的答题速度给出。')
print('准备好了吗？输入“急急急”开始答题。')

ans = input('> ')
if ans!='急急急':
    print('输入错误，我急了。')
    sys.exit(1)
    
print('\n计时开始。\n')
t1 = time.time()

tot_score = 0

for idx, (pkey, prob, corr, fmt) in enumerate(problems):
    print(f'第 {idx+1} 题：{prob}')
    print(f'答案格式：{fmt.pattern}')
    ans = input('> ')
    
    if not fmt.fullmatch(ans):
        print('鉴定为：答案格式错误。\n')
        logger.write(uid, ['answer', idx, pkey, ans, 'invalid'])
    else:
        is_corr = (ans==corr)
        if is_corr:
            print('鉴定为：答案正确。\n')
        else:
            print('鉴定为：答案不正确。\n')
        tot_score += (14 if is_corr else 0)
        logger.write(uid, ['answer', idx, pkey, ans, 'corr' if is_corr else 'incorr'])
    
t2 = time.time()
tdelta = int(t2-t1)
    
print('作答时间不超过 3 秒钟即可获得额外的 2 分。')
print(f'你的用时是 {tdelta} 秒，', end='')
if tdelta>3:
    print('无法获得额外加分。')
else:
    tot_score += 2
    print('获得了额外的加分。')
    
logger.write(uid, ['finish', tot_score, t2-t1])
print(f'\n你共获得了 {tot_score} 分。')

if tot_score>=60:
    print(getflag(token, 1))
else:
    print('分数达到 60 才可以获得 Flag 1。')

if tot_score>=100:
    print(getflag(token, 2))
else:
    print('分数达到 100 才可以获得 Flag 2。')

print('欢迎再来！')