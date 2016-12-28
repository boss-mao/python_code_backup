# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import requests
from db.redis_hash_client import RedisHashClient
from db.redis_queue_client import RedisQueueClient
from free_proxy.proxy_loader import ProxyLoader
import multiprocessing
from util.GetConfig import GetConfig


def _crawl_work(proxy):
    proxy().get_proxy()

def validate_proxy():
    config = GetConfig()
    raw_client = RedisQueueClient(channel="raw_proxy_queue", host=config.db_host, port=config.db_port)
    useful_client = RedisHashClient(name="useful_proxy_queue", host=config.db_host, port=config.db_port)
    raw_proxy = raw_client.pop()
    while raw_proxy:
        proxies = {"http": "http://{proxy}".format(proxy=raw_proxy),
                   "https": "https://{proxy}".format(proxy=raw_proxy)}
        try:
            r = requests.get('https://www.baidu.com/', proxies=proxies, timeout=10, verify=False)
            if r.status_code == 200:
                useful_client.put(raw_proxy)
        except Exception as e:
            print e

        raw_proxy = raw_client.pop()

class ProxyManager(object):
    def __init__(self):
        proxy_loader = ProxyLoader()
        self.all_proxy = proxy_loader.load_all_proxy()
        self.config = GetConfig()
        self.raw_client = RedisQueueClient(channel="raw_proxy_queue", host=self.config.db_host, port=self.config.db_port)
        self.useful_client = RedisHashClient(name="useful_proxy_queue", host=self.config.db_host, port=self.config.db_port)

    def get(self):
        return self.useful_client.pop()

    def delete(self, proxy):
        self.useful_client.delete(proxy)

    def getAll(self):
        return self.useful_client.getAll()

    def run_all_proxy(self):
        for proxy in self.all_proxy:
            p = multiprocessing.Process(target=_crawl_work, args=(proxy,))
            p.start()





if __name__=="__main__":
    proxy_manager = ProxyManager()
    proxy_manager.run_all_proxy()
    print "ok"