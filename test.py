import random

keys = ['blue', 'red', 'black']
stocks = ['blue']
tmp_keys = []
for item in keys:
    if item not in stocks:
        tmp_keys.append(item)

if len(stocks) == 1 and len(tmp_keys) == 1:
    stocks.append(tmp_keys[0])
elif len(stocks) == 1 and len(tmp_keys) >=2:
    stocks += random.sample(tmp_keys, k=2)
elif len(stocks) == 2 and stocks[0] != stocks[1] and len(tmp_keys) == 1:
    stocks.append(tmp_keys[0])
elif len(stocks) == 2 and stocks[0] != stocks[1] and len(tmp_keys) >= 2:
    stocks += random.sample(tmp_keys, k=1)
    
print(stocks)