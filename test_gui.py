import itertools
a = {"name": "Zaheeb", "last name": "Shamsi"}

b = {"name": "Ritika", "class": "MCA"}

c = {"college": "VIT"}

print(a.keys(), b.keys(), c.keys())

aaa = []

for k in a.keys(), b.keys(), c.keys():
    print(list(k))
    aaa.append(list(k))
print(aaa)
bbb = list(itertools.chain.from_iterable(aaa))
res=[]
[res.append(x) for x in bbb if x not in res]

print(res)

# for k in a.keys():
#     aaa.append(k)
#     print(k)
# print(aaa)
# for k in b.keys():
#     aaa.append(k)
#     print(k)
# print(aaa)
# for k in c.keys():
#     aaa.append(k)
#     print(k)
# print(aaa)

