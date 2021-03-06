from socket import ntohl

from colorama import Fore, Style
from gym_splendor.envs.base import error
class Player:
    def __init__(self, name):
        self.__name = name
        self.reset()

    def reset(self):
        self.message = ""
        self.__score = 0
        self.__stocks = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0,
            "auto_color": 0,
        }
        self.__stocks_const = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0,
        }
        self.__card_open = []
        self.__card_upside_down = []
        self.__card_noble = []
# Name

    @property
    def name(self):
        return self.__name

    def setName(self, value):
        self.__name = value
# Score

    @property
    def score(self):
        return self.__score

    @score.setter
    def setScore(self, value):
        self.__score = value
# Stock

    @property
    def stocks(self):
        return self.__stocks.copy()

    @stocks.setter
    def setStocks(self, value):
        self.__stocks = value
# Stocks Const

    @property
    def stocks_const(self):
        return self.__stocks_const.copy()

    @stocks_const.setter
    def setStocks_const(self, value):
        self.__stocks_const = value
# card_open

    @property
    def card_open(self):
        return self.__card_open

    @card_open.setter
    def setCard_open(self, value):
        self.__card_open = value
# card_upside_down

    @property
    def card_upside_down(self):
        return self.__card_upside_down

    @card_upside_down.setter
    def setCard_open(self, value):
        self.__card_upside_down = value
# card_noble

    @property
    def card_noble(self):
        return self.__card_noble

    @card_noble.setter
    def setCard_noble(self, value):
        self.__card_noble = value

    def action_space(self, state, stocks=[], card=None, stock_return=[], prioritize=0):
        if prioritize == 1 and len(stocks) != 0:
            self.get_stocks(stocks, state, stock_return)
        elif prioritize == 2 and self.check_get_card(card) == True:
            self.get_card(state, card)
        elif prioritize == 3 and self.check_upsite_down(card) == True:
            self.get_upside_down(state, card, stock_return)
        else:
            if len(stocks) != 0:
                self.get_stocks(stocks, state, stock_return)
            else:
                if self.check_get_card(card):
                    self.get_card(state, card)
                elif self.check_upsite_down(card):
                    self.get_upside_down(state, card, stock_return)
                    
# p
    def get_stocks(self, stocks, state, stock_return):
        l = self.check_input_stock(stocks, state)
        t = self.check_return(stock_return, stocks)
        if t == False:
            print(Fore.LIGHTRED_EX, str(self.name), "KH??NG TH??? L???Y NGUY??N LI???U DO ?????U V??O B??? L???I", 'stock:', stocks, 'return:', stock_return, end='')
            print(Style.RESET_ALL)
            return None
        if l == 1:
            for stock in stocks:
                self.__stocks[stock] += 1
            state["Board"].getStock(stocks)
        elif l == 2:
            self.__stocks[stocks[0]] += 2
            state["Board"].getStock(stocks)
        if sum(self.__stocks.values())>10 :
            self.return_stock(state, stock_return)
        print(Fore.LIGHTGREEN_EX, str(self.name), "L???Y NGUY??N LI???U", stocks, 'TR???', stock_return, end='')
        print(Style.RESET_ALL)            

    def validate_stock(self, arr_stock):
        '''
        0: arr_stock bi loi khong dung dinh dang
        1: lay 1,2,3 loai nguyen lieu
        2: lay 2 cua loai 1 nguyen lieu
        '''
        amount_stock = len(arr_stock)
        types_stock = len(list(set(arr_stock)))
        scale = amount_stock/types_stock
        if "auto_color" in arr_stock:
            print(Fore.LIGHTRED_EX, str(self.name), "L???I ?????U V??O L???Y STOCK AUTO_COLOR", arr_stock, end='')
            print(Style.RESET_ALL)
            return 0
        if amount_stock > 3 or scale == 3 or scale == 1.5:
            print(Fore.LIGHTRED_EX, str(self.name), "L???I ?????U V??O L???Y KH??NG ????NG S??? L?????NG LO???I, HO???C S??? L?????NG STOCK", arr_stock, end='')
            print(Style.RESET_ALL)
            return 0
        if scale == 1:
            return 1
        if scale == 2:
            return 2

    def check_input_stock(self, arr_stock, state):
        if self.validate_stock(arr_stock) == 1:
            for stock in arr_stock:
                if state["Board"].stocks[stock] == 0:
                    print(Fore.LIGHTRED_EX, str(self.name), "KH??NG ????? ??I???U KI???N NGUY??N LI???U TR??N B??N", arr_stock, end='')
                    print(Style.RESET_ALL)
                    return 0
            return 1
        if self.validate_stock(arr_stock) == 2:
            if state["Board"].stocks[arr_stock[0]] < 4:
                print(Fore.LIGHTRED_EX, str(self.name), "kh??ng ????? ??i???u ki???n tr??n b??n".upper(), arr_stock, end='')
                print(Style.RESET_ALL)
                return 0
            return 2

    def return_stock(self, state, stock_return):
        if sum(self.__stocks.values()) + len(stock_return) > 10:
            for stock in stock_return:
                self.__stocks[stock] = self.__stocks[stock] - 1
            state["Board"].postStock(stock_return)

    def check_get_card(self, Card):
        if Card == None:
            print(Fore.LIGHTRED_EX, str(self.name), "th??? truy???n v??o b??? r???ng".upper(), end='')
            print(Style.RESET_ALL)
            return False
        auto_color = self.__stocks["auto_color"]
        for i in Card.stocks.keys():
            if self.__stocks[i] + self.__stocks_const[i] < Card.stocks[i]:
                if self.__stocks[i] + self.__stocks_const[i] + auto_color >= Card.stocks[i]:
                    auto_color = self.__stocks[i] + self.__stocks_const[i] + auto_color - Card.stocks[i]
                else:
                    return False
        return True

    def check_return(self, stock_return, stocks):
        if sum(self.__stocks.values()) + len(stocks) > 10:
            stock_current = self.stocks
            for stock in stocks:
                stock_current[stock] +=1
            for stock in stock_return:
                stock_current[stock] -= 1
                if stock_current[stock] < 0:
                    return False
            if sum(stock_current.values())> 10:
                return False
        return True

    def get_upside_down(self, state, Card, stock_return):
        a = self.get_position_card_on_board(state, Card)
        if a == None:
            return
        else:
            if state["Board"].stocks["auto_color"] >= 1:
                if self.check_return(stock_return, ["auto_color"]):
                    self.__stocks["auto_color"] += 1
                    state["Board"].getStock(["auto_color"])
                    if sum(self.__stocks.values())>10 :
                        self.return_stock(state, stock_return)
            # -------
            show = a["show"]
            key = a["key"]
            if show == True:
                self.__card_upside_down.append(Card)
                state["Board"].deleteUpCard(key, Card)
            else:
                self.__card_upside_down.append(
                    state["Board"].dict_Card_Stocks_UpsiteDown[key][1])
                state["Board"].deleteCardInUpsiteDown(
                    key, state["Board"].dict_Card_Stocks_UpsiteDown[key][1])
            print(Fore.LIGHTGREEN_EX, str(self.name),"??p Th???".upper(), Card.id, 'TR???', stock_return, end='')
            print(Style.RESET_ALL)
        

    def get_card(self, state, Card):
        stock_return = {"red": 0,
                        "blue": 0,
                        "green": 0,
                        "white": 0,
                        "black": 0,
                        "auto_color": 0}
        self.__card_open.append(Card)
        self.__score += Card.score
        
        try:
            a = self.get_position_card(state, Card)
            mine = a["mine"]
        except:
            return

        if mine == False:
            state["Board"].deleteUpCard(a["key"], Card)
        else:
            self.__card_upside_down.remove(Card)

        print(Fore.LIGHTCYAN_EX, 'Card stocks:', str(Card.stocks), end='')
        print(Style.RESET_ALL)
        for i in Card.stocks.keys():
            stocks_late = self.__stocks[i]
            if stocks_late + self.__stocks_const[i] < Card.stocks[i]:
                auto_color = self.__stocks["auto_color"]
                self.__stocks["auto_color"] = self.__stocks["auto_color"] - (Card.stocks[i] - self.__stocks[i] -
                                                                             self.__stocks_const[i])
                self.__stocks[i] = self.__stocks[i] + (auto_color-self.__stocks["auto_color"]) + self.__stocks_const[i] - Card.stocks[i]
                stock_return["auto_color"] += auto_color - self.__stocks["auto_color"]
                stock_return[i] = stocks_late
            else:
                if self.__stocks_const[i] >= Card.stocks[i]:
                    stock_return[i] = 0
                else:
                    self.__stocks[i] = stocks_late + self.__stocks_const[i] - Card.stocks[i]
                    stock_return[i] = stocks_late - self.__stocks[i]
        self.__stocks_const[Card.type_stock] += 1
        self.getNoble(state)
        print(Fore.LIGHTYELLOW_EX, 'Stock return:', str(stock_return), end='')
        print(Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, str(self.name), "l???t th???".upper(), end='')
        print(Style.RESET_ALL)
        stock_return = list(self.coverdicttolist(stock_return))
        state["Board"].postStock(stock_return)
    
    def coverdicttolist(self,stock_return):
        for key,value in stock_return.items():
            for i in range(value):
                yield key

    def get_position_card(self, state, card):
        for i in self.__card_upside_down:
            if i.id == card.id:
                return {
                    "mine": True,
                }
        for i in state["Board"].dict_Card_Stocks_Show.keys():
            for j in state["Board"].dict_Card_Stocks_Show[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "mine": False,
                        "show": True,
                    }
        for i in state["Board"].dict_Card_Stocks_UpsiteDown.keys():
            for j in state["Board"].dict_Card_Stocks_UpsiteDown[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "show": False,
                    }

    def get_position_card_on_board(self, state, card):
        for i in state["Board"].dict_Card_Stocks_Show.keys():
            for j in state["Board"].dict_Card_Stocks_Show[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "show": True,
                    }
        for i in state["Board"].dict_Card_Stocks_UpsiteDown.keys():
            for j in state["Board"].dict_Card_Stocks_UpsiteDown[i]:
                if j.id == card.id:
                    return{
                        "key": i,
                        "show": False,
                    }

# L???y th??? Qu?? t???c n???u c?? th???
    def getNoble(self, state):
        b = []
        for card_Noble in state["Board"].dict_Card_Stocks_Show["Noble"]:
            check = True
            for i in card_Noble.stocks.keys():
                if self.__stocks_const[i] < card_Noble.stocks[i]:
                    check = False
            b.append(check)
        arr = []
        for i in range(len(b)):
            if b[i] == True:
                card_Noble = state["Board"].dict_Card_Stocks_Show["Noble"][i]
                self.__score += card_Noble.score

                arr.append(card_Noble)
                # print("Da lay the noble----------------------------------------------------------------------------------")
        
        for i in arr:
            self.__card_noble.append(i)
            state["Board"].deleteCardNoble(i)
            

    def check_upsite_down(self, card):
        if len(self.__card_upside_down) < 3 and card !=None:
            return True
        else:
            return False
