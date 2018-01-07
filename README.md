# WebTraffic-Generator

网站流量生成器，通过挂载代理对多个目标链接访问，可配置控制代理线程、随机访问频次/频率等；  
本程序作用有限，仅供学习使用。

## 运行环境

* Python 3

## 安装

#### 安装依赖

`$ pip install -r requirements.txt`

#### 配置

进入 webtraffic 目录，修改 spider.py 里的爬虫代码，然后调整 config.py 内的参数；  
proxy.py 内的 Redis 是依赖于 [IP 代理池][1]，如有固定代理可修改相关代码(内有注释)。

#### 运行

`$ python3 run.py `

## 文件结构

* config.py
> 参数配置模块

* engine.py
> 网页请求模块，支持重试和多线程

* process.py
> 进程模块，包括更新链接进程与流量进程

* spider.py
> 定义爬取目标链接的爬虫

* proxy.py
> 代理过滤器，控制同一个代理使用的时间间隔


  [1]: https://github.com/zkqiang/ProxyPool