local p, c = 5, 8
b = 10
nn = {}
a = {x = 5, y = 100.5, ['15'] = 111, ["22"] = 222}
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

a["x"]['cc']["ff"] = 100
a[20] = 1000
a["20"] = 142
a["22"] = 1515151
a['22'] = 11111111111

a.ff = 144

print(a.x)
print(a.fff)
print(a[20])

