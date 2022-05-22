import copy

def get_stock_return(my_stocks, wanted_stocks, wanted_card_stocks):  #TODO: finish this function
    # get num of excess chips
    my_stocks_dict = copy.deepcopy(my_stocks)
    for item in wanted_stocks:
        if item in my_stocks_dict.keys():
            my_stocks_dict[item] += 1
    excess = max(0, sum(my_stocks_dict.values()) - 10)
    if excess == 0:
        return []
    print('excess: ', excess)
    print('my_stocks_dict: ', my_stocks_dict)
    # print('wanted_card_stocks: ', wanted_card_stocks)

    # get list of returnable stocks
    returnable_stocks = {}
    for item in my_stocks_dict:
        if item in wanted_card_stocks and item != 'auto_color':
            returnable_stocks.update({item : max(0, my_stocks_dict[item] - wanted_card_stocks[item])})
    list_returnable_stocks = []
    for key, val in returnable_stocks.items():
        list_returnable_stocks.append([key, val])
    list_returnable_stocks.sort(key=lambda x:x[1], reverse=True)
    print('list_returnable_stocks: ', list_returnable_stocks)

    # get stocks_return
    ret = []
    if sum(returnable_stocks.values()) >= excess:
        for _ in range(excess):
            ret.append(list_returnable_stocks[0][0])
            list_returnable_stocks[0][1] -= 1
            list_returnable_stocks.sort(key=lambda x:x[1], reverse=True)
    else:
        # get new_returnable_list
        card_stocks_dict = {}
        for key, val in wanted_card_stocks.items():
            if val != 0:
                card_stocks_dict.update({key : val})
        print('card_stocks_dict: ', card_stocks_dict)
        new_returnable_list = []
        for key in card_stocks_dict:
            if my_stocks_dict[key] != 0:
                new_returnable_list.append([key, my_stocks_dict[key], card_stocks_dict[key]])
        new_returnable_list.sort(key=lambda x : x[2], reverse=False)
        print('new_returnable_list: ', new_returnable_list)

        # get unnecessary type stocks
        unnecessary_stocks = []
        for key in my_stocks_dict:
            if key not in card_stocks_dict and key != 'auto_color' and my_stocks_dict[key] != 0:
                unnecessary_stocks.append(key)
        print('unnecessary_stocks: ', unnecessary_stocks)

        #
        if len(unnecessary_stocks) == 0:
            if excess == 1:
                ret.append(new_returnable_list[0][0])
            elif excess == 2:
                ret.append(new_returnable_list[0][0])
                ret.append(new_returnable_list[1][0])
            elif excess == 3:
                ret.append(new_returnable_list[0][0])
                ret.append(new_returnable_list[1][0])
                ret.append(new_returnable_list[2][0])
        elif len(unnecessary_stocks) > 0:
            for type_stock in unnecessary_stocks:
                if len(ret) < excess:
                    for _ in range(returnable_stocks[type_stock]):
                        ret.append(type_stock)
            new_excess = excess - len(ret)
            if new_excess == 1:
                ret.append(new_returnable_list[0][0])
            elif new_excess == 2:
                ret.append(new_returnable_list[0][0])
                ret.append(new_returnable_list[1][0])
            elif new_excess == 3:
                ret.append(new_returnable_list[0][0])
                ret.append(new_returnable_list[1][0])
                ret.append(new_returnable_list[2][0])
    print(ret)


stocks = ['red', 'black', 'white']
my_stocks = {"red": 6, "blue": 0, "green": 0, "black": 3, "white": 0, "auto_color": 1}
wanted_card_stocks = {"red": 7, "blue": 0, "green": 0, "black": 3, "white": 0}

get_stock_return(my_stocks, stocks, wanted_card_stocks)