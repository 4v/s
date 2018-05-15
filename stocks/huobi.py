# -*- coding: utf-8 -*-
#author: 半熟的韭菜

from websocket import create_connection
import gzip
import time
import threading
import json
import calendar
import datetime

class Huobi:
    def __init__(self):
        self.ws = create_connection("wss://api.huobipro.com/ws")
        self.rpc_thread = threading.Thread(target=self.rpc_thread_proc)
        self.rpc_thread.start()
        self.request_counter = 0
        self.request_counter_lock = threading.Lock()
        self.request_in_flight = dict()
    
    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.close()

    def close(self):
        self.ws.close()

    def rpc_thread_proc(self):
        while True:
            # 接收一条消息
            packet = self.ws.recv()

            # 没有消息，说明已经断开连接了，退出
            if not packet:
                break

            # 对数据包进行解码
            packet = gzip.decompress(packet).decode('utf-8')
            packet = json.loads(packet)

            # 如果是心跳包，那么返回心跳结果
            if list(packet) == ['ping']:
                self.ws.send(json.dumps({'pong':packet['ping']}))
                continue

            # 如果包含id，就通知相应的线程
            if 'id' in packet:
                id = packet['id']
                self.request_in_flight[id].resolve(packet)
                del self.request_in_flight[id]
                continue

            # 如果是其他不认识的包，就打印一下
            print(packet)

    def get_kline(self, type, period, start_time, end_time):
        id = self.create_request_id()
        req = {
            "req": "market.%s.kline.%s" % (type, period),
            "id": id,
            "from": self.timestamp(start_time),
            "to": self.timestamp(end_time)
        }
        self.ws.send(json.dumps(req))
        message = self.wait_response(id)
        return message

    def wait_response(self, id):
        return self.request_in_flight[id].get()
    
    def create_request_id(self):
        with self.request_counter_lock:
            # 计数器增加
            self.request_counter = self.request_counter + 1

            # 通知机制
            self.request_in_flight[self.request_counter] = Future()
            return self.request_counter
    
    def timestamp(self, dt):
        return calendar.timegm(dt.timetuple())

class Future:
    def __init__(self):
        self.lock = threading.Lock()
        self.lock.acquire()
    
    def resolve(self, message):
        self.message = message
        self.lock.release()

    def get(self):
        self.lock.acquire()
        self.lock.release()
        return self.message
