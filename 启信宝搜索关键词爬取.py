# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:01
@author: Jack Luo
@file: 启信宝搜索关键词爬取.py
'''
import requests, re
from lxml import etree
from selenium import webdriver
import pymysql
import datetime
from decimal import Decimal

brs = webdriver.Chrome()
url = 'https://www.qixin.com/'
brs.get(url)
pscode = brs.page_source
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianxi', charset='utf8')
cursor = db.cursor()
sql = 'create table if not exists 港桥分析 (单位名称 VARCHAR(50),法人 VARCHAR(20),电话 VARCHAR(20),邮箱 VARCHAR(30),地址 VARCHAR(80),状态 VARCHAR(8),`资本(万)` VARCHAR(8),成立日期 VARCHAR(20));'
cursor.execute(sql)
pattern = re.compile(
    '<div.*?queryid.*?>(.*?)</a>.*?代表人：(.*?)</div>.*?(?:电话：(.*?)</span>.*?)?(?:font-f2">(.*?)</a>.*?)?地址：(.*?)<a.*?label-red">(.*?)</span>.*?content-text">(.*?)</div>.*?content-text">(.*?)</div>',
    re.S)
datalist = re.findall(pattern, pscode)
datalist
for i in datalist:
    insertsql = 'insert into 港桥数据 values("{}","{}","{}","{}","{}","{}",{},"{}");'.format(
        i[0].replace('<em>', '').replace('</em>', ''), i[1], i[2], i[3], i[4].replace('<em>', '').replace('</em>', ''),
        i[5], Decimal(i[6][:-5]), i[7])
    cursor.execute(insertsql)
    db.commit()
sqlcx = "select * from lianxi.港桥数据;"
cursor.execute(sqlcx)
db.close()
