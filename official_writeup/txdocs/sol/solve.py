import json
from pathlib import Path

WIDTH = 11
HEIGHT = 300

def trans(i):
    return i//WIDTH, i%WIDTH

def solve(har_p):
    with har_p.open('r', encoding='utf-8') as f:
        reqs = json.load(f)['log']['entries']
    target = [(idx, req) for idx, req in enumerate(reqs) if 'Below is your flag' in json.dumps(req)]
    assert len(target)==1, f'got {len(target)} targets'
    print(f'{len(reqs)} requests, target is {target[0][0]+1}')
    
    target = target[0][1]
    res = target['response']['content']['text']
    assert '{\"0\":{\"0\":5,\"2\":[1,\"Below is your flag\"],\"3\":0},' in res
    
    res = '{' + (
        res
            .partition('{\"0\":{\"0\":5,\"2\":[1,\"Below is your flag\"],\"3\":0},')[2]
            .partition('{\"0\":5,\"2\":[1,\"Above is your flag\"],\"3\":0}')[0]
    ) + 'null}'
    points = [trans(int(k)) for k, v in json.loads(res).items() if v]
    
    canvas = [[' ' for x in range(WIDTH)] for y in range(HEIGHT)]
    for r, c in points:
        canvas[r][c] = 'x'
        
    with (har_p.parent / 'res.txt').open('w') as f:
        f.write('\n'.join(''.join(c for c in r) for r in canvas))

solve(Path('challenge.har'))