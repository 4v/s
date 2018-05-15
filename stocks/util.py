#encoding: utf8

import hashlib
import pickle
import os.path
import json
import datetime
import requests

# 缓存执行方法，加快程序速度
def file_cache(func):
    def result(*k, **kw):
        hash = call_hash(func, k, kw)
        loaded,result2 = load_cache(hash)
        if loaded:
            return result2
        result2 = func(*k, **kw)
        save_cache(hash, result2)
        return result2
    return result

def load_cache(hash):
    path = get_cache_path(hash)
    if not os.path.exists(path):
        return False, None
    with open(path, 'rb') as f:
        return True, pickle.loads(f.read())

def save_cache(hash, value):
    path = get_cache_path(hash)
    with open(path, 'wb') as f:
        return f.write(pickle.dumps(value))

def call_hash(func, k, kw):
    code = func.func_code.co_code
    d = pickle.dumps((code, k, kw))
    return hashlib.md5(d).hexdigest()

def get_cache_path(hash):
    return '/tmp/mtree-%s' % hash

def timer(message):
    return Timer(message)

class Timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self, *k):
        self.start = datetime.datetime.now()
        print(self.message)
    
    def __exit__(self, *k):
        duration = datetime.datetime.now() - self.start
        seconds = duration.total_seconds()
        print(seconds, 'seconds')

def http_get(url):
    try:
        r = requests.get(url,timeout=10)
        return r.text
    finally:
        r.close()

def format_date(d):
    return d.strftime('%Y-%m-%d')

def format_datetime(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')