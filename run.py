#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webtraffic.process import SpiderProcess, TrafficProcess
from multiprocessing import Queue


def run():
    queue = Queue(1)
    p1 = SpiderProcess(queue)
    p2 = TrafficProcess(queue)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    run()
