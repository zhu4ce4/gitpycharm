# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:45
@author: Jack Luo
@file: 百度明星排行榜.py
'''
# 终极目标!怎么把数据写入sql
# url=https://baike.baidu.com/starrank?fr=lemmaxianhua
# 首要目标:抓取所有页面的本周的paiming,xingming,xianhua,topfs
import requests
from lxml import etree
from selenium import webdriver
import time
# 在使用webdriver时,一定要用timesleep,因为网页加载需要时间
import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianxi', charset='utf8')
# 一定要charset吗?
cursor = db.cursor()
sql = 'create table if not exists mingxing(paiming int(20),xingming VARCHAR(50),xianhua int(20),topfs VARCHAR (50));'
# 上面代码后面的分号;不能少
cursor.execute(sql)

url = 'https://baike.baidu.com/starrank?fr=lemmaxianhua'
browser = webdriver.Chrome()
browser.get(url)

for j in range(0, 50):
    time.sleep(2)
    # 在得到源代码前先sleep下,以便网页加载完毕
    pagesource = browser.page_source
    pagedata = etree.HTML(pagesource)
    paiminglist = pagedata.xpath("//td[contains(@class,'star-index star-index')]/i/text()")[:20]
    # 用xpath得到的是一个list
    xingminglist = pagedata.xpath("//td[contains(@class,'star-name')]/a/text()")[:20]
    xianhualist = pagedata.xpath("//td[contains(@class,'star-score')]/span/text()")[:20]
    topfslist = pagedata.xpath("//td[contains(@class,'star-fans')]/p[1]/text()")[:20]
    # 上述几个xpath里面用 ("//div[@data-cat='thisWeek']//td/i/text()")  更合适简便
    for i in range(len(paiminglist)):
        sqlinsert = "insert into mingxing (paiming,xingming,xianhua,topfs) values ({},'{}',{},'{}');".format(
            paiminglist[i], xingminglist[i], xianhualist[i], topfslist[i])
        # 上面的代码为什么要在varchar类型的数据外面加上  ''   请参考http://blog.csdn.net/yuanya/article/details/78173312
        cursor.execute(sqlinsert)
        # 光是指定数据不行,还得执行
        db.commit()
    # 执行完还不行,提交完数据一定要把数据库commit
    try:
        js = "document.getElementsByClassName('pTag next')[1].click();"
        browser.execute_script(js)
        # 上面使用了js,但系统内并未import  is相关的模块,疑似使用的是webdriver的内容
        # 上述代码为何不能用以下代码????:
        # button = browser.find_element_by_xpath("//div[@data-cat='thisWeek']/div/a[@class='pTag next']")
        # button.click()
    except:
        print('出错')
    # 如果不设置上面的timesleep,很容易导致点击失败!!!!!无法跳转!!!!!如果时间太短,可能会导致,下一页这个标签元素尚未被加载出来,当然就无法点击了!!!!

browser.quit()
db.close()

print('ok')
# 怎样修改为 每隔10页保存数据库一次
