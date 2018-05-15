#encoding: utf8

import os
import struct
import util
import json
import datetime
import huobi
import pytz
import time

'''
数据格式：
[Stock, Stock, ...]
Stock: {'code':xxx, 'prices': Prices}
Prices: [Price, Price, ...]
Price: {'close':xxx,'open':xxx,'time':datetime.datetime}
'''

TIMEZONE = pytz.timezone('Asia/Shanghai')

class DayDayFund:
    def load(self, code):
        # 请求天天基金的接口，拿到累计净值数据
        url = 'http://fund.eastmoney.com/pingzhongdata/%s.js' % code
        result = util.http_get(url)
        prices = self.parse_prices(result)
        return {'code': code, 'prices': prices}

    def parse_prices(self, response):
        v = self.get_var_define(response, 'var Data_ACWorthTrend = ');
        v = json.loads(v)
        last_price = None
        result = []
        for timestamp,price in v:
            time = datetime.datetime.fromtimestamp(timestamp / 1000, TIMEZONE)
            if last_price is None:
                open,high,low,close = price, price, price, price
            else:
                open,high,low,close = last_price, max(last_price, price), min(last_price, price), price
            last_price = price
            result.append({
                'time': time,
                'open': open,
                'close': close,
                'high': high,
                'low': low,
            })
        return result

    def get_var_define(self, response, prefix):
        for line in response.splitlines():
            if not line.startswith(prefix):
                continue
            return line[len(prefix):-1]
        raise Exception('not find var')

class Huobi:
    LOG_FILE = 'huobi.log'
    
    def __init__(self):
        self.TIMEZONE = TIMEZONE

    def load(self, code, period):
        # 先从文件中加载
        local_responses = self.load_from_file(code, period)
        local_kline = self.unpack_responses(local_responses)
        print('local responses count', len(local_responses))

        # 获取最后加载的时间
        if local_kline:
            last_time = local_kline[-1]['id']
            last_time = datetime.datetime.fromtimestamp(last_time, self.TIMEZONE)
        else:
            last_time = None
        
        # 增量下载数据
        if last_time is None:
            remote_responses = self.initial_download(code, period)
            print('initial download', len(remote_responses))
        elif (datetime.datetime.now(self.TIMEZONE) - last_time).total_seconds() < 600:
            # 下载太频繁，不需要下载了
            remote_responses = []
        else:
            remote_responses = self.incremental_download(code, period, last_time)
            print('incremental download', len(remote_responses))
        remote_kline = self.unpack_responses(remote_responses)
        
        # 保存下载结果
        self.save_download(remote_responses)

        # 合并两边的结果
        merged_kline = self.merge_huobi_kline(local_kline, remote_kline)

        # 封装结果
        return {
            'code': code,
            'prices': self.as_prices(merged_kline)
        }

    def load_from_file(self, code, period):
        # 生成请求的Key
        request_key = 'market.%s.kline.%s' % (code, period)

        # 如果文件不存在，就直接返回空白的结果
        if not os.path.exists(self.LOG_FILE):
            return []

        # 文件存在，就从文件中读取
        result = []
        with open(self.LOG_FILE) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                line = json.loads(line)
                if 'rep' not in line: continue
                if line['rep'] != request_key: continue
                result.append(line)
        return result
    
    def initial_download(self, code, period):
        start_time = self.start_of_day(datetime.datetime.now(self.TIMEZONE) + datetime.timedelta(days=1))
        days = self.get_days_backward(start_time)
        return self.download_kline(code, period, days)

    def download_kline(self, code, period, days):
        with huobi.Huobi() as client:
            result = []
            for (start, end) in days:
                response = client.get_kline(code, period, start, end)
                if response['status'] != 'ok': raise Exception('error from server: ' + str(response))
                if not response['data']: break
                print('%s get %s items' % (start, len(response['data'])))
                result.append(response)
                time.sleep(1)
            return result

    def start_of_day(self, dt):
        return datetime.datetime(dt.year, dt.month, dt.day, tzinfo=self.TIMEZONE)

    def get_days_backward(self, start_time):
        pointer = start_time
        while True:
            start = pointer - datetime.timedelta(days=1)
            end = pointer
            yield (start, end)
            pointer = start

    def incremental_download(self, code, period, start_time):
        days = self.get_days_between(start_time, datetime.datetime.now(self.TIMEZONE))
        return self.download_kline(code, period, days)

    def get_days_between(self, start_time, end_time):
        day = self.start_of_day(start_time)
        while day < end_time:
            day_end = day + datetime.timedelta(days=1)
            yield (day, day_end)
            day = day_end

    def save_download(self, responses):
        with open(self.LOG_FILE, 'a') as f:
            for e in responses:
                f.write(json.dumps(e))
                f.write('\n')

    def merge_huobi_kline(self, kline1, kline2):
        return self.normalize_kline(kline1 + kline2)

    def normalize_kline(self, kline):
        # 去重、按时间排序
        result = dict()
        for item in kline:
            result[item['id']] = item
        return [e[1] for e in sorted(result.items())]

    def unpack_responses(self, responses):
        # 取出应答中的数据，组合成kline数据
        result = []
        items = []
        for e in responses:
            if e['status'] != 'ok':
                raise Exception('bad response, status is not ok')
            items.extend(e['data'])
        return self.normalize_kline(items)

    def as_prices(self, kline):
        result = []
        for e in kline:
            result.append({
                'time': self.get_datetime_from_timestamp(e['id']),
                'open': e['open'],
                'close': e['close'],
                'high': e['high'],
                'low': e['low'],
            })
        return result

    def get_datetime_from_timestamp(self, ts):
        return datetime.datetime.fromtimestamp(ts, self.TIMEZONE)

class EastMoney:
    def load_one(self, stockCode):
        # 解析股票代码
        if stockCode.startswith('sh'):
            stockId = stockCode[2:] + '1'
        elif stockCode.startswith('sz'):
            stockId = stockCode[2:] + '2'
        else:
            raise Exception('bad stock code: ' + str(stockCode))

        # 请求东方财富的接口，拿到前复权的数据
        # 前复权
        url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=k&rtntype=5&isCR=false&authorityType=fa' % stockId
        result = util.http_get(url)
        prices = self.parse_prices(result)
        return {'code': stockCode, 'prices': prices}

    def parse_prices(self, text):
        text = text[1:-1]
        j = json.loads(text)
        prices = []
        for e in j['data']:
            split = e.split(',')
            price = {
                'time':datetime.datetime.strptime(split[0], '%Y-%m-%d'),
                'open':float(split[1]),
                'close':float(split[2]),
                'high':float(split[3]),
                'low':float(split[4]),
            }
            prices.append(price)
        return prices

class Tongdaxin:
    def __init__(self, path):
        self.path = path
    
    def load(self):
        files = self.getFiles()
        files = files
        # files = [e for e in files if '600004' in e]
        return [self.loadOneFile(e) for e in files]
    
    def getFiles(self):
        path1 = self.path + '/vipdoc/sh/lday'
        path2 = self.path + '/vipdoc/sz/lday'
        r1 = self.getDayFilesIn(path1)
        r2 = self.getDayFilesIn(path2)
        return r1 + r2
    
    def getDayFilesIn(self, path):
        li = os.listdir(path)
        result = [os.path.join(path, e) for e in li]
        return result

    def loadOneFile(self, file):
        prices = []
        with open(file, 'rb') as f:
            content = f.read()
            assert len(content) % 32 == 0
            count = len(content) / 32
            for i in range(count):
                i = i * 32
                line = content[i:i+32]
                date,op,high,low,close,amount,volumn,lclose = struct.unpack('<iiiiifii', line)
                prices.append({
                    'time':date,
                    'open':op/100.0,
                    'close':close/100.0
                })
        result = dict()
        result['code'] = file.split('/')[-1].split('.')[0]
        result['prices'] = prices
        return result

'''
股本变迁文件解密方法：
http://blog.csdn.net/fangle6688/article/details/50956609

 while (len)
 {
  for (i = 0; i < 3; i++)
  {
   eax = *((int*)(pCodeNow + 0x44));
   ebx=*((int*)(pDataNow));
   num = eax^ebx;
   numold = *((int*)(pDataNow + 0x4));

   for (j = 0x40; j > 0; j = j - 4)
   {
    ebx = (num & 0xff0000) >> 16;
    eax = *((int*)(pCodeNow + ebx * 4 + 0x448));
    ebx = num >> 24;
    eax += *((int*)(pCodeNow + ebx * 4 + 0x48));
    ebx = (num & 0xff00) >> 8;
    eax ^= *((int*)(pCodeNow + ebx * 4 + 0x848));
    ebx = num & 0xff;
    eax += *((int*)(pCodeNow + ebx * 4 + 0xC48));
    eax ^= *((int*)(pCodeNow + j));

    ebx = num;
    num = numold^eax;
    numold = ebx;
   }
   numold ^= *((int*)pCodeNow);
   pInt = (unsigned int*)pDataNow;
   *pInt = numold;
   pInt = (unsigned int*)(pDataNow+4);
   *pInt = num;
   pDataNow = pDataNow + 8;
  }
  pDataNow = pDataNow + 5;
  len--;
 }


len = '记录条数'
code = '？'
data = '？'
for _ in range(len):
    for i in range(4):
        a = decode_int(code[0x44])
        b = decode_int(data[:4])
        num = a ^ b
        numold = decode_int(data[4])
        


  for (i = 0; i < 3; i++)
  {
   eax = *((int*)(pCodeNow + 0x44));
   ebx=*((int*)(pDataNow));
   num = eax^ebx;
   numold = *((int*)(pDataNow + 0x4));

   for (j = 0x40; j > 0; j = j - 4)
   {
    ebx = (num & 0xff0000) >> 16;
    eax = *((int*)(pCodeNow + ebx * 4 + 0x448));
    ebx = num >> 24;
    eax += *((int*)(pCodeNow + ebx * 4 + 0x48));
    ebx = (num & 0xff00) >> 8;
    eax ^= *((int*)(pCodeNow + ebx * 4 + 0x848));
    ebx = num & 0xff;
    eax += *((int*)(pCodeNow + ebx * 4 + 0xC48));
    eax ^= *((int*)(pCodeNow + j));

    ebx = num;
    num = numold^eax;
    numold = ebx;
   }
   numold ^= *((int*)pCodeNow);
   pInt = (unsigned int*)pDataNow;
   *pInt = numold;
   pInt = (unsigned int*)(pDataNow+4);
   *pInt = num;
   pDataNow = pDataNow + 8;
  }
  pDataNow = pDataNow + 5;

'''