x=dict()
x['a']=4
x['b']=2
x['c']=1

x['d']=1
x['e']=2

x['f']=45
x['g']=2

x['h']=25
x['i']=7

for y in range(5):
	if('d' not in x.keys()):
		x['d']=1
	else:
		x['d']+=1

print(sorted(x.items(), key=lambda j: j[1]))