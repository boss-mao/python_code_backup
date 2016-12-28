# -*- coding: utf-8 -*-
# !/usr/bin/env python
from db.db_Client import DbClient
from db.redis_hash_client import RedisHashClient
from db.redis_queue_client import RedisQueueClient
from util.GetConfig import GetConfig


class FreeProxyBase():
    def __init__(self):
        self.config = GetConfig()
        self.client =RedisHashClient(name="proxy_queue", host=self.config.db_host, port=self.config.db_port)

    def add_proxy_to_redis(self, proxy):
        self.client.put(proxy)

    def get_proxy(self):
        raise  NotImplemented()

