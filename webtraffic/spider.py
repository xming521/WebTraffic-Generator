#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import JSONDecodeError
import requests
import json
import time


def urls_spider():
    """用于获取目标链接的爬虫，可以指定页数
    这里是示例代码，可以仿照代码实现自己的类
    """
    url = 'http://36kr.com/api/feed-stream?per_page=100&feed_id=270'
    try:
        json_data = json.loads(requests.get(url).text)['data']['items']
    except (JSONDecodeError, IndexError) as e:
        print(url, e, sep='\n')
        return
    time.sleep(4.5)
    article_url = 'http://36kr.com/p/{}.html'
    return [article_url.format(i.get('entity_id')) for i in json_data]
