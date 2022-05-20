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
        if len(self.get_affordable_cards(state['Board'])) == 0:
            most_viable_unaffordable, _ = self.target_card(state)
            for key, val in self.get_stocks_need(most_viable_unaffordable):
                for _ in range(val):
                        stocks.append(key)  #TODO: finish this (can phai check so luong stock tren board)
                if len(stocks) == 3:
                    break
            stock_return = self.get_stock_return(stocks=stocks, my_board=state['Board'])
            #TODO: finish this function
        
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
            a list of cards that the player can get (include upside down cards)
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


    def get_stock_return(self, stocks, my_board):
        '''
            param:
                stocks: list of string 
                my_board: (class Board) - get the board from the state
            return:
                a list of excess chips based on the least chips on board
        '''

        # get number of excess chips
        my_dict = self.stocks
        ret = []
        for item in stocks:
            if item in my_dict.keys():
                my_dict[item] += 1
        excess = max(0, sum(my_dict.values()) - 10)

        # get stocks on board and sort in ascending order
        if excess > 0:
            stocks_onboard = my_board.stocks.pop('auto_color')  # dict
            list_stock_onboard = list(stocks_onboard.items())
            list_stock_onboard.sort(key=lambda x : x[1], reverse=False)
        for _ in range(excess):
            for i in range(len(list_stock_onboard)):
                item = list_stock_onboard[i]
                if item[0] in my_dict.keys() and my_dict[item[0]] > 0:
                    list_stock_onboard[i][1] += 1
                    ret.append(item[0])
                    list_stock_onboard.sort(key=lambda x : x[1], reverse=False)
                    my_dict[item[0]] -= 1
                    break  #TODO: finish this function
        return ret


    def target_card(self, state):
        '''
        return the most viable card
            param: 
                state: dictionary
            return:
                the most viable card (card object)
        '''
        board = state['Board']  # board obj
        affordable_cards = self.get_affordable_cards(board)
        cards_onboard = board.dict_Card_Stocks_Show  # dictionary
        cards_deposit = self.card_upside_down  # list
        list_card = cards_deposit + cards_onboard['I'] + cards_onboard['II'] + cards_onboard['III']

        # get unaffordable cards
        unaffordable = []
        for card in list_card:
            if card not in affordable_cards:
                unaffordable.append(card)
        unaffordable.sort(key=self.evaluate_unaffordable_card)

        diff = self.evaluate_unaffordable_card(unaffordable[0])
        return unaffordable[0], diff
        
    
    def get_most_viable_affordable_card(self, affordable_card_list):
        '''
        return the most viable affordable card
            param:
                affordable_card_list: list of card object
            return:
        '''
        affordable_card_list.sort(key=self.evaluate_affordable_card)
        return affordable_card_list[0]


        
    def evaluate_unaffordable_card(self, unaffordable_card):
        '''
        calculate the difference between score of the card and the ultilities
            param:
                unaffordable_card: card obj
            return:
                difference between score of the card and the ultilities
        '''
        needed_stocks = self.get_stocks_need(unaffordable_card)
        return sum(needed_stocks.values()) - unaffordable_card.score


    def evaluate_affordable_card(self, affordable_card):

        dict_buy = affordable_card.stocks
        chips_buy = {}
        for key in self.stocks_const:
            chips_buy.update({key: max(0, dict_buy[key] - self.stocks_const[key])})
            
        return sum(chips_buy.values())