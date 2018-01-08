#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from multiprocessing import Process
from .spider import urls_spider
from .proxy import ProxyFilter
from .config import THREAD, TRAFFIC_SLEEP, UPDATE_SLEEP
from .engine import TrafficEngine


class SpiderProcess(Process):
    """周期性更新链接进程
    由于链接通常不会太多，这里只存储在实例属性里
    """
    def __init__(self, queue):
        Process.__init__(self)
        self.target_urls = []
        self.queue = queue

    def run(self):
        while True:
            print('开始更新链接...')
            len_tmp = len(self.target_urls)
            crawl_urls = urls_spider()
            for url in crawl_urls:
                if url not in self.target_urls:
                    self.target_urls.append(url)
            # 将最新链接列表推送给另一个进程
            self.queue.put(self.target_urls)
            print('更新了 %s 个链接' % (len(self.target_urls)-len_tmp))
            time.sleep(UPDATE_SLEEP)


class TrafficProcess(Process):
    """周期性访问链接进程
    """
    def __init__(self, queue):
        Process.__init__(self)
        self.queue = queue

    def run(self):
        proxies = ProxyFilter()
        engine = TrafficEngine()
        target_urls = self.queue.get(timeout=120)
        while True:
            print('开始重新加载代理产生流量...')
            if not self.queue.empty():
                target_urls = self.queue.get(timeout=5)
            engine.start(proxies.get_usable(THREAD), target_urls)
            time.sleep(TRAFFIC_SLEEP)
