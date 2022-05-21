def check_get_stocks(stocks_need, stocks_onboard):
    '''
    check whether the player can get the stocks needed
        param:
            stocks_need: dict
            my_board: Board obj get from state
        return:
            lack_stocks_onboard, need_stocks_can_get, list_stocks_onboard
    '''
    stocks_onboard_can_get = {}
    wanted_stocks = []

    # get intersect keys betweenn stock_onboard and stock_need
    for key, val in stocks_onboard.items():
        if key != 'auto_color' and val != 0:
            stocks_onboard_can_get.update({key: val})
    intersect_keys = find_intersection(list(stocks_need.keys()), list(stocks_onboard_can_get.keys()))

    # get list_stocks_onboard
    list_stocks_onboard = list(stocks_onboard_can_get.items())
    list_stocks_onboard.sort(key=lambda x:x[1], reverse=True)

    # get list_stocks_need
    list_stocks_need = list(stocks_need.items())
    list_stocks_need.sort(key=lambda x:x[1], reverse=True)

    print(list_stocks_need)
    # print(stocks_onboard_can_get)
    print(list_stocks_onboard)
    print(intersect_keys)
    
    # get wanted_stocks
    if len(intersect_keys) == 0:
        tmp_length = len(list_stocks_onboard)
        if tmp_length == 1:
            if list_stocks_onboard[0][1] >= 4:
                wanted_stocks.append(list_stocks_onboard[0][0])
                wanted_stocks.append(list_stocks_onboard[0][0])
            elif list_stocks_onboard[0][1] < 4:
                wanted_stocks.append(list_stocks_onboard[0][0])
        elif tmp_length == 2:
            wanted_stocks.append(list_stocks_onboard[0][0])
            wanted_stocks.append(list_stocks_onboard[1][0])
        elif tmp_length == 3:
            wanted_stocks.append(list_stocks_onboard[0][0])
            wanted_stocks.append(list_stocks_onboard[1][0])
            wanted_stocks.append(list_stocks_onboard[2][0])
        elif tmp_length == 4:
            wanted_stocks.append(list_stocks_onboard[-1][0])
            wanted_stocks.append(list_stocks_onboard[-2][0])
            wanted_stocks.append(list_stocks_onboard[-3][0])
    elif len(intersect_keys) == 1:
        if stocks_onboard_can_get[intersect_keys[0]] >= 4:
            wanted_stocks.append(intersect_keys[0])
            wanted_stocks.append(intersect_keys[0])
        elif stocks_onboard_can_get[intersect_keys[0]] < 4:
            wanted_stocks.append(intersect_keys[0])
    elif len(intersect_keys) == 2:
        wanted_stocks.append(intersect_keys[0])
        wanted_stocks.append(intersect_keys[1])
    elif len(intersect_keys) == 3:
        wanted_stocks.append(intersect_keys[0])
        wanted_stocks.append(intersect_keys[1])
        wanted_stocks.append(intersect_keys[2])
    elif len(intersect_keys) == 4:
        wanted_stocks.append(list_stocks_need[0][0])
        wanted_stocks.append(list_stocks_need[1][0])
        wanted_stocks.append(list_stocks_need[2][0])
    return wanted_stocks

def find_intersection(lst1, lst2):
        # Use of hybrid method
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3


stock_need = {
    'red' : 1,
    'blue' : 1
}

stocks_onboard = {'red': 1, 'blue': 0, 'green': 5, 'black': 6, 'white': 4, 'auto_color': 5}

stocks = []
stocks = check_get_stocks(stock_need, stocks_onboard)
test_list = [('a', 1)]
test_list[0][1] += 1
print(test_list)