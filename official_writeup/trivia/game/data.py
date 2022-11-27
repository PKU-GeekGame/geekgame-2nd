import re
import random
import sympy

# BEGIN BV https://www.zhihu.com/question/381784377/answer/1099438784

bv_table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
bv_tr={}
for i in range(58):
    bv_tr[bv_table[i]]=i
bv_s=[11,10,3,8,4,6]
bv_xor=177451812
bv_add=8728348608

def bv_decode(x: str) -> int:
    assert x.startswith('BV')
    r=0
    for i in range(6):
        r+=bv_tr[x[bv_s[i]]]*58**i
    return (r-bv_add)^bv_xor

# END BV

BVIDS = ['BV1EV411s7vu']
'''
BVIDS = [
    'BV1yG411F7Fv', 'BV1Td4y1b7cN', 'BV1R84y1v7eF', 'BV11v4y1U7Fn', 'BV1he4y1x7q1', 'BV1hd4y1F7pY',
    'BV1gt4y1T72i', 'BV1vt4y1K7fU', 'BV1iP411w7DL', 'BV1cD4y1874g', 'BV1ng411h7da', 'BV1Bt4y1F78j',
    'BV1ut4y1A71J', 'BV1cV4y1K7y6', 'BV19B4y1L7ar', 'BV1RG411J74a', 'BV1ee4y1z7R3', 'BV1AB4y1E71k',
    'BV1UP411n7yo', 'BV1be4y1H7rT', 'BV1GR4y1d7tJ', 'BV1j8411476s', 'BV1vP411J7WV', 'BV1RG4y1q7yF',
    'BV1TG4y1z798', 'BV1He4y1o7Nu', 'BV1W14y1s7Lo', 'BV1Ug411U7B4', 'BV1rB4y1g78h', 'BV1Sa411g7Dq',
    'BV1jN4y1c7M9', 'BV1Ze4y1o79d', 'BV1FN4y157kn', 'BV1Ge4y1D7xV', 'BV1vt4y1V78o', 'BV1PG4y1v7Qj',
    'BV1PW4y1172R', 'BV1QF411K7YA', 'BV1ZW4y117ma', 'BV1Hr4y177BU', 'BV1bB4y187yd', 'BV1YU4y1i7KY',
    'BV1SN4y1T767', 'BV1J94y1Q7SQ', 'BV11t4y147uD', 'BV1fe4y1R7Qa', 'BV1Hg411f782', 'BV1rS4y1E7xv',
    'BV1gS4y1H7tk', 'BV1BL4y1w7rF', 'BV1Ma411s788', 'BV1XG411s7Hw', 'BV1PB4y1B7Jc', 'BV1FY411K7fW',
    'BV1BY4y1n7sy', 'BV1P34y1p7HE', 'BV1wa411s79w', 'BV1gv4y1u73U', 'BV1QY411N7WW', 'BV1jL4y1P7a5',
]
'''

def gen_problem():
    pygame_lv = random.randrange(5, 15)
    
    primes = []
    while len(primes)<=8:
        prime_range_lower = random.randrange(9000000000, 9990000000)
        primes = [x for x in range(prime_range_lower, prime_range_lower+500) if sympy.isprime(x)]
    prime_range_upper = primes[8]-1
    the_prime = random.choice(primes[:8])
    assert prime_range_lower<=the_prime<=prime_range_upper
    
    bvid = random.choice(BVIDS)
    avid = bv_decode(bvid)

    problist = [
        [ #1
            'domain_punycode',
            '访问网址 “http://ctf.世界一流大学.com” 时，向该主机发送的 HTTP 请求中 Host 请求头的值是什么？',
            'ctf.xn--4gqwbu44czhc7w9a66k.com',
            re.compile(r'^[^:\s]+$'),
        ],
        [ #2
            'gstore_doi',
            '北京大学某实验室曾开发了一个叫 gStore 的数据库软件。最早描述该软件的论文的 DOI 编号是多少？',
            '10.14778/2002974.2002976',
            re.compile(r'^[\d.]+\/[\d.]+$'),
        ],
        [ #3
            'pygame_money',
            f'在第一届 PKU GeekGame 比赛的题目《电子游戏概论》中，通过第 {pygame_lv} 级关卡需要多少金钱？',
            str((lambda level: 300+int(level**1.5)*100)(pygame_lv)),
            re.compile(r'^\d+$'),
        ],
        [ #4
            'firefox_webp',
            '支持 WebP 图片格式的最早 Firefox 版本是多少？',
            '65',
            re.compile(r'^\d+$'),
        ],
        [ #5
            'runner_package',
            '每个 Android 软件都有唯一的包名。北京大学课外锻炼使用的最新版 PKU Runner 软件的包名是什么？',
            'cn.edu.pku.pkurunner',
            re.compile(r'^[a-z.]+$'),
        ],
        [ #6
            'wifi_zipcode',
            '我有一个朋友在美国，他无线路由器的 MAC 地址是 d2:94:35:21:42:43。请问他所在地的邮编是多少？',
            '80304',
            re.compile(r'^\d+$'),
        ],
        [ #7
            'bilibili_avid',
            f'视频 bilibili.com/video/{bvid} 也可以通过 bilibili.com/video/av_____ 访问。下划线内应填什么数字？',
            str(avid),
            re.compile(r'^\d+$'),
        ],
        [ #8
            'rand_prime',
            f'我刚刚在脑海中想了一个介于 {prime_range_lower} 到 {prime_range_upper} 之间的质数。猜猜它是多少？',
            str(the_prime),
            re.compile(r'^\d+$'),
        ]
    ]
    
    problist.pop(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 7]))
    random.shuffle(problist)
    return problist