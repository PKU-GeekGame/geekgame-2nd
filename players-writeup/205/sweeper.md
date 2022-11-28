# 扫雷 II

## 解题过程
只解了 Level2。
先去看了去年扫雷的 writeup。了解了要去推测 RNG 的内部状态。读了 go 里面 math.rand 的 rng 代码。

~~~go
// Uint64 returns a non-negative pseudo-random 64-bit integer as an uint64.
func (rng *rngSource) Uint64() uint64 {
	rng.tap--
	if rng.tap < 0 {
		rng.tap += rngLen
	}

	rng.feed--
	if rng.feed < 0 {
		rng.feed += rngLen
	}

	x := rng.vec[rng.feed] + rng.vec[rng.tap]
	rng.vec[rng.feed] = x
	return uint64(x)
}
~~~

发现是个 LFSR，故只需拿到足够长度的输出，就确定的其内部的状态。代码如下：

~~~python
import requests
import json

status = []

for i in range(160):
    for j in range(16):
        done = False
        for k in range(16):
            t = requests.post(
                'https://prob14-7d937mvc.geekgame.pku.edu.cn/click', data=dict(x=j, y=k))
            t = json.loads(t.text)
            boom = t.get('boom', None)
            if boom is not None:
                done = True
                break
        if done:
            break
    state = []
    for line in boom:
        for c in line:
            # Boom
            if c == -1:
                state.append('1')
            else:
                state.append('0')
    for i in range(4):
        number = 0
        for j in range(4):
            n_n = state[:16]
            n_n.reverse()
            n_n = int(''.join(n_n), 2)
            number = number + (n_n << 16 * j)
            state = state[16:]
        status.append(number)


def check_alg():
    init_s = status[:607]
    left_s = status[607:]
    for new_s in left_s:
        tab_s = init_s[-273]
        feed_s = init_s[0]
        assert (tab_s + feed_s) & 0xffffffffffffffff == new_s
        init_s = init_s[1:]
        init_s.append(new_s)
    return init_s


def predict(init_s):
    for i in range(4):
        tab_s = init_s[-273]
        feed_s = init_s[0]
        new_s = (tab_s + feed_s) & 0xffffffffffffffff
        init_s = init_s[1:]
        init_s.append(new_s)
    return init_s[-4:]


init_s = check_alg()
t = predict(init_s)
field = []
for bn in t:
    for i in range(4):
        number = bn >> (i * 16)
        bits = [str(number >> j & 1) for j in range(16)]
        field.extend(bits)
        print(bits)
for i, b in enumerate(field[:-16]):
    if b == '0':
        print('x', i // 16, 'y', i % 16)
        t = requests.post('https://prob14-7d937mvc.geekgame.pku.edu.cn/click', data=dict(x=i//16, y=i%16))
~~~

