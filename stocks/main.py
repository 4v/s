#encoding: utf8

import datasource
import model
import util
import account
import json

def main():
    # stock = datasource.Huobi().load('btcusdt', '5min') # load_east('sz002174')
    stock = datasource.DayDayFund().load('001986')
    all_prices = stock['prices']
    # for parameter in range(5, 100):
        # results = []
        # for i in range(5):
            # block = 2000
            # stock['prices'] = # all_prices[-block*i-block-1:-block*i-1]
    m = model.SlopeModel(stock['prices'])
    m.run()
    ops = m.get_actions()
    result = simulate_trade(stock, ops, 0)
    result = '%.2f%%' % (result*100)
        # results.append(result)
    print('收益率：%s' % (result))

def backTest():
    with util.timer('loading data'):
        stocks = load_tdx()

    with util.timer('running model'):
        results = []
        for stock in stocks:
            prices = stock['prices']
            ops = model.SlopeModel(prices).run()
            result = simulate_trade(stock, ops)
            results.append((stock['code'], result))

    print('show result')
    results = list(sorted(results, key=lambda x:-x[1]))
    for a,b in results:
        print(a,b)

def simulate_trade(stock, ops, trade_fee):
    initialMoney = 10000.0
    acc = account.Account(initialMoney, trade_fee)
    prices = [e['close'] for e in stock['prices']]
    assert len(prices) == len(ops)
    for price,op in zip(prices, ops):
        if op == 'B':
            acc.buy(price)
        elif op == 'S':
            acc.sell(price)
    return (acc.get_value(prices[-1]) - initialMoney) / initialMoney

def print_stock_ops(stock, ops):
    print('stock: ' + stock['code'])
    dates = [e['time'] for e in stock['prices']]
    assert len(dates) == len(ops)
    for date, op in zip(dates, ops):
        print(date, op)

@util.file_cache
def load_tdx():
    return datasource.Tongdaxin('/Users/caipeichao/Desktop/new_tdx').load()

@util.file_cache
def load_east(code):
    ds = datasource.EastMoney()
    return ds.load_one(code)

if __name__ == '__main__':
    main()
