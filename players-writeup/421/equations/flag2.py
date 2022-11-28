import pulp
from math import sqrt
right = ['19106.6119577929', '19098.1846041713', '19124.6925013201', '19072.8591005901', '19063.3797914261', '19254.8741381550', '19410.9493230296', '18896.7331405884', '19021.3167024024', '18924.6509997019', '18853.3351082021', '18957.2296714145', '18926.7035797566', '18831.7182995672', '18768.8192204100', '18668.7452791590', '18645.9207293335', '18711.1447224940']
primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
neq = len(right)
nx = neq + 10
mylp = pulp.LpProblem("lp1", pulp.LpMinimize)
x = []
spx = {
	0: 102, #f
	1: 108, #l
	2: 97, #a
	3: 103, #g
	4: 123, #{
	nx-1: 125, #}
}
for i in range(nx):
	if i in spx:
		x.append(pulp.LpVariable("x"+str(i),spx[i],spx[i],'Integer'))
	else:
		x.append(pulp.LpVariable("x"+str(i),32.5,127.5,'Integer'))

# bound = [(31.9,127.1) for i in range(nx)]
# bound[0] = (101.99,102.01)
# bound[1] = (107.99,108.01)
# bound[2] = (96.99,97.01)
# bound[3] = (102.99,103.01)
# bound[4] = (122.99,123.01)
# bound[-1] = (124.99,125.01)
p = list(map(sqrt,primes[:nx]))
for r in right:
	expression = 0
	for i in range(nx):
		expression += p[i] * x[i]
	mylp += expression <= float(r) + 0.01
	mylp += expression >= float(r) - 0.01
	# a.append(p)
	# b.append(float(r) + 0.01)
	# fan = list(map(lambda x:-x, p))
	# a.append(fan)
	# b.append(- float(r) + 0.01)
	p = p[-1:] + p[:-1]
# res=linprog(c,a,b,None,None,bound)
status = mylp.solve()
print(pulp.LpStatus[status])
for i in range(nx):
	print(chr(int(0.01+pulp.value(x[i]))), end="")
