#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time
from requests import ConnectionError, Timeout
from requests.exceptions import ProxyError, ChunkedEncodingError
from .config import HEADERS, PROXY_WAIT, PROXY_SPAN
from threading import Thread


class TrafficEngine(object):

    def __init__(self):
        """初始化代理池和代理"""
        self.target_urls = None

    def proxy_request(self, proxy, times, url=None, retry=2):
        """加载代理并发出请求
        可以从`start`方法里随机获得`url`
        并且有重试次数防止代理不稳定
        :param proxy: 加载的代理
        :param url: 请求的链接，不指定会从`start`方法里随机获取
        :param times: 代理请求次数，不指定会从参数中随机获取
        :param retry: 请求失败后的重试次数
        :return: 递归进入下个请求
        """
        # 随机间隔，避免请求过于规律
        time.sleep(random.uniform(PROXY_WAIT[0], PROXY_WAIT[1]))
        if times <= 0 or retry <= 0:
            return
        if not url:
            url = random.choice(self.target_urls)
        try:
            requests.get(url, headers=HEADERS, proxies=proxy, timeout=30)
            print('%s 请求成功，正在访问 %s' % (proxy['http'], url))
            return self.proxy_request(proxy, times=times-1)
        except (ConnectionError, Timeout, ProxyError, ChunkedEncodingError):
            print('%s 请求失败，即将重试 %s' % (proxy['http'], url))
            return self.proxy_request(proxy, times, url, retry=retry-1)

    def start(self, proxies, urls):
        """传入代理组和链接组产生流量
        :param proxies: 一组代理
        :param urls: 一组链接，用于随机选择链接
        :return: True
        """
        self.target_urls = urls
        index = range(len(proxies))
        threads = [Thread(
            target=self.proxy_request,
            args=({'http': proxy},
                  random.randint(PROXY_SPAN[0], PROXY_SPAN[1])))
            for proxy in proxies]
        for i in index:
            threads[i].start()
        for i in index:
            threads[i].join()
