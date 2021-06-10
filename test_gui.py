# import itertools
# a = {"name": "Zaheeb", "last name": "Shamsi"}
#
# b = {"name": "Ritika", "class": "MCA"}
#
# c = {"college": "VIT"}
#
# print(a.keys(), b.keys(), c.keys())
#
# aaa = []
#
# for k in a.keys(), b.keys(), c.keys():
#     print(list(k))
#     aaa.append(list(k))
# print(aaa)
# bbb = list(itertools.chain.from_iterable(aaa))
# res=[]
# [res.append(x) for x in bbb if x not in res]
#
# print(res)
#
# # for k in a.keys():
# #     aaa.append(k)
# #     print(k)
# # print(aaa)
# # for k in b.keys():
# #     aaa.append(k)
# #     print(k)
# # print(aaa)
# # for k in c.keys():
# #     aaa.append(k)
# #     print(k)
# # print(aaa)
#


import json
#
# with open('snow.json', 'r') as j:
#     data = json.load(j)
#     # print(data)
#
# for e in data['entities']:
#     # print(e)
#     for key, value in e['properties'].items():
#         print(key)
#         print(value)


# initializing list
test_list = ["zaheeb", "shamsiii", "zaheeb"]
print("The original list is : " + str(test_list))

# using list comprehension
# to remove duplicated
# from list
res = []
[res.append(x) for x in test_list if x not in res]

# printing list after removal
print("The list after removing duplicates : " + str(res))
