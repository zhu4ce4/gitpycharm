# -*- coding: utf-8 -*-
'''
@time: 2018/8/10 8:31
@author: Jack Luo
@file: 淘宝指定关键词爬取.py
'''
from selenium import webdriver
from lxml import etree
import time
import pymongo
from pyquery import PyQuery as pq

def get_url(url):
    print('运行666666666')
    br.get(url)
    global page_num
    page_num=0
    while page_num<2:
    # while br.find_element_by_css_selector('.item.next'):
        page_num+=1
        url=br.current_url
        print('第{}页的url'.format(page_num),url)
        yield url
        time.sleep(2)
        # br.find_element_by_css_selector('.item.next').click()
        try:    #此处不能用if-else
            br.find_element_by_xpath('//li[@class="item next next-disabled"]')
            print('没有下一页了')
        except:
            br.find_element_by_xpath('//li[@class="item next"]').click()
        time.sleep(2)


def get_page_source(urls):
    print('运行9999999999999999')
    global item_num
    item_num = 0
    for url in urls:
        br.get(url)
        # ps=br.page_source
        # html=etree.HTML(ps)
        # items=html.xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
        # for item in items:
        #     item_num+=1
        #     #titles=item.xpath('//@alt')   错误！！！！
        #     titles=item.xpath('.//@alt')    #正确！！！！
        #     titles=titles[0]
        #     shouhuo=item.xpath('.//div[@class="deal-cnt"]/text()')
        #     if shouhuo:
        #         shouhuo=shouhuo[0][:-3]
        #     else:
        #         pass
        #     yield {'标题':titles,'收货数':shouhuo}

        #以下可见pyquery更好用！
        html=br.page_source
        doc=pq(html)
        items=doc('.m-itemlist .items .item.J_MouserOnverReq  ').items()
        for item in items:
            biaoti=item.find('.J_ItemPic.img').attr['alt']
            shouhuo=item.find('.deal-cnt').text()[:-3]
            yield {'标题':biaoti,'shouhuo':shouhuo}

'''
上述方法可以得到收货数据为空的数据，并将其保留为 [] 空数据，数据无缺失！！！！
用以下方法不能够取得：有一些收获数据是空的，以下方法不能够取得收获数据为空的数据，会直接略过，从而造成数据缺失！！！
html=etree.HTML(ps)
shouhuo=html.xpath('//div[@class="deal-cnt"]/text()')
print(shouhuo)
包括使用re正则表达式方法匹配也会导致 不能够获取 【】空数据，从而导致数据缺失的问题！！！
'''

def save_to_mongo(results,keywords):
    mongo_url = 'localhost'
    mongo_db = 'taobao'
    mongo_collection = '{}'.format(keywords)
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    for result in results:
        try:
            if db[mongo_collection].insert(result):
                pass
        except:
            print('failed')
    print('已存入MongoDB','\n')

if __name__ == '__main__':
    keywords=input('请输入要淘宝搜索的关键词：')
    url='https://s.taobao.com/search?q={}&sort=sale-desc'.format(keywords)
    # chrome_options=webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    br=webdriver.PhantomJS()
    print('运行8')
    urls=get_url(url)
    print('运行888')
    get_page_source(urls)
    # results=get_page_source(urls)
    # save_to_mongo(results,keywords)
    br.close()
    print('==================================统计分割线==================================')
    # print('共爬取页数:', page_num)
    # print('总共爬取数据条数：', item_num)
