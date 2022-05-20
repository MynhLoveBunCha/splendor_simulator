dict = {'a' : 1, 'b' : 2, 'c' : 3}
lst = list(dict.items())
# def min_val(tup):
#     return tup[1]
lst.sort(key=lambda x : x[1], reverse=False)
print(lst)