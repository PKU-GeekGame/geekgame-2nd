raw = 'fa{aeAGetTm@ekaev!lgHv__ra_ieGeGm_1}'
n = len(raw)
ans = []
for i in range(n):
    if i % 2 == 0:
        ans.append(raw[i // 2])
    else:
        ans.append(raw[n // 2 + i // 2])
print(''.join(ans))
