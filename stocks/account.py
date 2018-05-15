#encoding: utf8

'''
资金账户，模拟买卖，最后计算收益。
'''
class Account:
    def __init__(self, initialMoney, trade_fee):
        self.money = initialMoney
        self.goods = 0
        self.trade_fee = trade_fee
    
    def buy(self, price):
        if self.money == 0: return
        self.goods = self.money / float(price) * (1-self.trade_fee)
        self.money = 0

    def sell(self, price):
        if self.goods == 0: return
        self.money = self.goods * price * (1-self.trade_fee)
        self.goods = 0

    def get_value(self, price):
        return self.money + self.goods * price