#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time
from requests import ConnectionError, Timeout
from requests.exceptions import ProxyError, ChunkedEncodingError
from .config import HEADERS, PROXY_WAIT, PROXY_SPAN
from concurrent import futures


class TrafficEngine(object):

    def __init__(self):
        """初始化代理池和代理"""
        self._target_urls = None
        self._counter = 0

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
        if times <= 0 or retry <= 0:
            return
        if not url:
            url = random.choice(self._target_urls)
        try:
            resp = requests.get(url, headers=HEADERS, proxies=proxy, timeout=15)
            print('%s 请求成功，正在访问 %s' % (proxy['http'], url))
            self._counter += 1
            # 按配置产生随机间隔，并根据请求时长调整
            sleep_parm = 1
            if resp.elapsed.seconds > 10:
                sleep_parm = 0.75
            time.sleep(random.uniform(PROXY_WAIT[0], PROXY_WAIT[1])*sleep_parm)
            return self.proxy_request(proxy, times=times-1)
        except (ConnectionError, Timeout, ProxyError, ChunkedEncodingError):
            print('%s 请求失败，即将重试 %s' % (proxy['http'], url))
            time.sleep(2)
            return self.proxy_request(proxy, times, url, retry=retry-1)

    def start(self, proxies, urls):
        """传入代理组和链接组产生流量
        :param proxies: 一组代理
        :param urls: 一组链接，用于随机选择链接
        :return: True
        """
        start_time = time.clock()
        self._target_urls = urls
        tmp = self._counter
        with futures.ThreadPoolExecutor(max_workers=len(proxies)) as executor:
            future_to_down = {executor.submit(self.proxy_request, {'http': proxy},
                                              random.randint(PROXY_SPAN[0], PROXY_SPAN[1]))
                              : proxy for proxy in proxies}
            futures.as_completed(future_to_down)
        print('='*64, '\n  本组结束，耗时 %d 秒，成功请求 %d 次，目前累计成功 %d 次\n'
              % (time.clock()-start_time, self._counter-tmp, self._counter), '='*64, sep='')
