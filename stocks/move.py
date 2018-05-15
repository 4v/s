#encoding: utf8

# 搬砖套现

def main():
    usdt_to_btc = 14240
    btc_to_usdt = 1.0 / usdt_to_btc
    buy_btc = 105999
    sell_btc = 104700
    buy_usdt = 7.33
    sell_usdt = 7.3
    print 'CNY,USDT,BTC,CNY', 100.0 / buy_usdt / usdt_to_btc * sell_btc
    print 'CNY,BTC,USDT,CNY', 100.0 / buy_btc / btc_to_usdt * sell_usdt

main()