# -*- coding: utf-8 -*-
#author: 半熟的韭菜

import huobi
import datetime
import time
import json

def main():
    pass

def decode_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def get_days_backward(begin):
    while True:
        start = begin - datetime.timedelta(days=1)
        end = begin
        yield (start, end)
        begin = start

def download():
    start_time = decode_datetime('2017-12-30 00:00:00')
    client = huobi.Huobi()
    with open('crawl_log', 'a') as f:
        for (start, end) in get_days_backward(start_time):
            response = client.get_kline('btcusdt', '5min', start, end)
            if not response['data']: break
            print('%s get %s items' % (start, len(response['data'])))
            f.write(json.dumps(response))
            f.write('\n')
            time.sleep(1)

def load_kline():
    req='market.btcusdt.kline.5min'
    result = dict()
    with open('crawl_log') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            line = json.loads(line)
            assert line['rep'] == req
            assert line['status'] == 'ok'
            items = line['data']
            for item in items:
                result[item['id']] = item
    return [e[1] for e in sorted(result.items())]

main()