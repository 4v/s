#encoding: utf8

import requests
from ws4py.client.geventclient import WebSocketClient
import calendar
import datetime
import json

# K线游戏
# 随机给一段K线，判断下一格是涨是跌
# websocket没有搞定，尝试用nodejs

def main():
   hb = Huobi()
   start_time = decode_datetime('2017-01-01 00:00:00')
   end_time = decode_datetime('2017-01-02 00:00:00')
   print hb.get_btcusdt_kline(start_time, end_time)

def decode_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

class Huobi:
    def __init__(self):
        self.ws = WebSocketClient('wss://api.huobi.pro/ws', protocols=['http-only', 'chat'])
        self.ws.connect()

    def get_btcusdt_kline(self, start_time, end_time):
        req = {
            "req": "market.btcusdt.kline.5min",
            "id": "fdfadsfd",
            "from": self.timestamp(start_time),
            "to": self.timestamp(end_time)
        }
        print req
        self.send_json(req)
        return self.receive_json()

    def send_json(self, req):
        req = json.dumps(req)
        self.ws.send(req.encode('utf8'))

    def timestamp(self, dt):
        return calendar.timegm(dt.timetuple())

    def receive_json(self):
        while True:
            print self.ws.receive()

# if __name__ == '__main__':
#     try:
#         ws = DummyClient('ws://localhost:9000/', protocols=['http-only', 'chat'])
#         ws.connect()
#         ws.run_forever()
#     except KeyboardInterrupt:
#         ws.close()


if __name__ == '__main__':
    main()