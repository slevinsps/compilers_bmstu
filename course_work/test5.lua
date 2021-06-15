local p, c = 5, 8
b = 10
nn = {}
a = {x = 5, y = 100.5}
a['x'] = 10
a[20] = 'aa'
a['fff'] = 144
a[20] = 'bbb'
a.fff = 14
a.x = {bb = 2, cc = 100}

a['x']['bb'] = 10
a.x['bb'] = 50
a.x.bb = 20
a['x']['cc'] = {ff = 170}

a['x']['cc']['ff'] = 21
print(a.x)
print(a.fff)
print(a[20])

