#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 单个代理访问间隔随机区间
PROXY_WAIT = [10, 30]
# 单个代理连续访问页数随机区间
PROXY_SPAN = [6, 12]
# 代理被使用后的休息最小间隔
PROXY_SLEEP = 1800
# 代理线程数（建议少量多次）
THREAD = 5

# 更新链接间隔
UPDATE_SLEEP = 1800
# 流量进程间隔
TRAFFIC_SLEEP = 30

# 如有固定代理，可存在这里并在`proxy.py`里替换
PROXIES = []

# 目标网站的原始Cookie
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'device-uid=955651c0-f1e0-11e7-a188-a97caed0d959; aliyungf_tc=AQAAAAC0UER3UgUA2t14ffLVmTRSVZLg; '
              'krnewsfrontss=cea1dc86d68c3d4321b9b8310d25fcb7; '
              'M-XSRF-TOKEN=33f6bebab609855236c8d7616f41ac3ab6ce11181e5b677b05ded3328166e99f; '
              'TY_SESSION_ID=17f707cb-e401-4242-a8b6-e7479fa47e81; kr_stat_uuid=eN5Qw25255374; '
              'Hm_lvt_713123c60a0e86982326bae1a51083e1=1515322447; identity_id=4244703549849808; '
              'download_animation=1; ktm_ab_test=t.6_v.deploy!t.7_v.deploy!t.9_v.18!t.13_v.26!t.'
              '21_v.deploy!t.5_v.deploy; laravel_session=eyJpdiI6InRtRFwvOFZXeVRLV2RXcVo0Yklqd0lBP'
              'T0iLCJ2YWx1ZSI6InhKR1dPN1NhY2h2RzR1blwvZVAxditPZVgyNXUrZ2RqR1hsOUlLc3lhS1wvVGFFTFN3'
              'OEhJS1wvVWRqYXVmUkxacEEyYXhSQ3BuVFd0QjdKb21ROTFrRDd3PT0iLCJtYWMiOiI1ZGI5Mzk2YTczODM4O'
              'GVhNjVjNGVmNTU0ODZjMzk4OWNhZjI5NTM3MDJkMGFhNDlmNjEwN2Q1NjdjYmZiYWY4In0%3D; Hm_lpvt_71'
              '3123c60a0e86982326bae1a51083e1=1515329255; arp_scroll_position=4681.60009765625',
    'Host': '36kr.com',
    'Referer': 'http://36kr.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'X-Tingyun-Id': 'Dio1ZtdC5G4;r=329256016',
}
