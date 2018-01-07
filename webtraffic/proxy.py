#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import PROXY_SLEEP
from datetime import datetime
from random import choices
import redis
import time


class ProxyFilter(object):
    """代理过滤器，被使用过的代理自动被登记
    在配置参数指定的时间内将无法使用
    """

    def __init__(self):
        self.register_table = {}
        self.pool = ProxyPool()

    def register(self, proxy):
        """登记代理，标记目前的时间"""
        self.register_table[proxy] = datetime.now()

    def remove_expired(self):
        """检查并去除登记过期的代理"""
        for k, v in self.register_table.copy().items():
            if (datetime.now() - v).seconds > PROXY_SLEEP:
                self.register_table.pop(k)

    def get_usable(self, total):
        """返回没有登记过的代理，并自动登记
        :param total:
        :return:
        """
        # 先检查过期时间
        self.remove_expired()
        # 如果是代理列表，可以引入替换这里的`pool.get_all()`
        usable = list(set(self.pool.get_all()) ^
                      set(self.register_table.keys()))
        if len(usable) < total:
            print('当前无可用代理，将在5分钟后重试')
            time.sleep(300)
            return self.get_usable(total)
        chosen = choices(usable, k=total)
        for each in chosen:
            self.register(each)
        return chosen


class ProxyPool(object):
    """这里用的是作者实现的代理IP池：
    https://github.com/zkqiang/ProxyPool
    如果有固定的代理IP可加在`config.py`里然后引用
    """

    def __init__(self):
        """初始化 Redis 连接"""
        self.redis = redis.StrictRedis(host='localhost', port=6379,
                                       decode_responses=True)
        self.key_name = 'proxies'

    def get_all(self):
        """返回所有可用代理
        """
        return self.redis.zrevrangebyscore(self.key_name, 100, 40)
