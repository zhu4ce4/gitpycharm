# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/27 17:11
@author: Jack Luo
@job:
//todo:待优化！一次性获取网易财经首页内容
'''
from scrapy.cmdline import execute

execute('scrapy crawl moneynews'.split())
