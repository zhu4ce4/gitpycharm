# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:02
@author: Jack Luo
@file: 企查查关键词爬取.py
'''
#已实现:指定关键字在企查查中查询注册时间最近的前10页(企查查只提供10页),并将信息存入mysql.
#未解决问题:成立时间为日期格式,但暂无法实现以日期格式写入,只能以字符串写入
import re
import time
from selenium import webdriver
import pymysql

def getlist(guanjianzi):
    time.sleep(1)
    resp=brw.page_source
    pattern=re.compile('<td>.*?class.*?>(.*?)</a>.*?href.*?>(.*?)</a>.*?class.*?>(.*?)</span>.*?class.*?>(.*?)</span>.*?<p.*?</span>.*?<p.*?>(.*?)</p>.*?ma_cbt_green.*?>(.*?)</span>',re.S)
    datalist=re.findall(pattern,resp)
    for item in datalist:
        yield {'名称':item[0].replace('<em>','').replace('</em>',''),'法人':item[1],'注册资本':item[2][5:],'成立时间':item[3][5:],'单位地址':item[4].replace(r'\n','').replace('<em>','').replace('</em>','').strip()[3:],'状态':item[5]}
    #在打开指定页面后,稍等1秒,等页面加载完成,取ajax加载后的源代码,对源代码用正则找到需要的项目赋值给datalist,在对该list的每个item分别取值,在对每个item(该item为tuple)里面的元素分别做相应的处理替换截取去空格等

def insertsql(guanjianzi):
    for item in getlist(guanjianzi):
        sqlinsert="insert into {} VALUES ('{}','{}','{}','{}','{}','{}');".format(guanjianzi,item['名称'],item['法人'],item['注册资本'],item['成立时间'],item['单位地址'],item['状态'])
        #上行代码未能将时间转换成日期,需进一步处理!!!!!!!
        cursor.execute(sqlinsert)
        db.commit()

def main(guanjianzi):
    while True:
        getlist(guanjianzi)
        insertsql(guanjianzi)
        try:
            brw.find_element_by_link_text('>').click()
        except:
            print('无下一页了')
            break
            #上面的break,如果无法点击下一页了,则break,跳出最近的循环,进入后面的流程.
        time.sleep(1)
    db.close()
    brw.quit()
    print('已完成!')

if __name__=='__main__':
    guanjianzi = input('请输入要查找的关键字:')

    url = 'https://www.qichacha.com/'
    brw = webdriver.Chrome()
    brw.get(url)
    brw.find_element_by_link_text('登录').click()
    brw.find_element_by_id('nameNormal').send_keys('13760338748')
    time.sleep(10)
    brw.find_element_by_name('key').send_keys('{}'.format(guanjianzi))
    brw.find_element_by_class_name('btn-lg').click()
    time.sleep(1)
    brw.find_element_by_partial_link_text('重庆').click()
    time.sleep(1)
    brw.find_element_by_id('closeSuspend').click()
    time.sleep(1)
    brw.find_element_by_class_name('sortDesc').click()
    time.sleep(1)
    brw.find_element_by_link_text('注册资本降序').click()

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='jackallqj86', db='lianxi', charset='utf8')
    cursor = db.cursor()
    sql = 'create table if not exists {} (mingcheng VARCHAR (50),faren VARCHAR (20),ziben VARCHAR (20),shijian VARCHAR (20),dizhi VARCHAR (200),zhuangtai VARCHAR (10));'.format(guanjianzi)
    cursor.execute(sql)

    main(guanjianzi)



    #如果是写入txt则: with open('朱沱注册公司.txt','a+') as f:
    #     f.write(str(item)+'\n')
