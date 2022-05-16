from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        
        list_affordable_card = self.get_affordable_cards(state['Board'])
        list_II_card_show = state['Board'].dict_Card_Stocks_Show['II']
        if len(list_affordable_card):
            card = list_affordable_card[random.randint(0, len(list_affordable_card) - 1)]
        else:
            wanted_card = list_II_card_show[random.randint(0, len(list_II_card_show) - 1)]
            dict_needed_stocks = self.get_stocks_need(wanted_card)
            for key in dict_needed_stocks.keys():
                if dict_needed_stocks[key] != 0:
                    stocks.append(key)
                if len(stocks) > 3:
                    break
            stock_return = self.get_stock_return(stocks)
        return stocks, card, stock_return
    

    def get_stocks_need(self, wanted_card):
        '''
        Return a dictionary containing the stocks needed to buy the wanted_card
            param: 
                wanted_card(class Card)
            return: 
                a dictionary containing the stocks needed to buy the wanted_card
        '''
        price = wanted_card.stocks # dict
        needed_stocks = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0
        }
        stock_dict = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0,
            "auto_color": 0
        }
        for key in stock_dict.keys():
            if key != 'auto_color':
                stock_dict[key] += self.stocks[key]
                stock_dict[key] += self.stocks_const[key]
            else:
                stock_dict[key] += self.stocks[key]
        for key in price.keys():
            needed_stocks[key] = max(0, price[key] - stock_dict[key])
        auto_color = stock_dict['auto_color']
        for _ in range(auto_color):
            if sum(needed_stocks.values()) == 0:
                break
            for key in needed_stocks.keys():
                if needed_stocks[key] != 0:
                    needed_stocks[key] -= 1
                    break
        return needed_stocks
    

    def get_affordable_cards(self, my_board):
        '''
        param:
            my_board(class Board) - get the board from the state
        return:
            a list of cards that the player can get
        '''
        card_onboard = my_board.dict_Card_Stocks_Show  # dict
        card_deposit = self.card_upside_down # list
        ret = []
        for item in card_deposit:
            if self.check_get_card(item):
                ret.append(item)
        for key in card_onboard.keys():
            if key != 'Noble':
                for item in card_onboard[key]:
                    if self.check_get_card(item):
                        ret.append(item)
        return ret


    def get_stock_return(self, stocks):
        '''
            param:
                stocks: list of string 
            return:
                a list of excess chips
        '''
        my_dict = self.stocks
        ret = []
        for item in stocks:
            if item in my_dict.keys():
                my_dict[item] += 1
        excess = sum(my_dict.values()) - 10
        if excess > 0:
            for _ in range(excess):
                for key in my_dict.keys():
                    if my_dict[key] > 1:
                        my_dict[key] -= 1
                        ret.append(key)
                        break
        return ret
