# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:12
@author: Jack Luo
@file: ec wait的使用.py
'''
from selenium import webdriver
import time
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def get_url(url):
    print('2')
    br.get(url)
    global page_num
    page_num = 0
    while page_num < 2:
        # while br.find_element_by_css_selector('.item.next'):
        page_num += 1
        url = br.current_url
        print('第{}页的url'.format(page_num), url)
        yield url
        print('4')
        try:  # 此处不能用if-else
            br.find_element_by_xpath('//li[@class="item next next-disabled"]')
            print('没有下一页了')
        except:
            br.find_element_by_xpath('//li[@class="item next"]').click()
            # time.sleep(0.8)
            try:
                wait.until(ec.presence_of_element_located((By.LINK_TEXT, '下一页')))
            except TimeoutException:
                print('times out')
        print('5')
        # br.find_element_by_css_selector('.item.next').click()


def get_page_source(urls):
    print('1')
    global item_num
    item_num = 0
    for url in urls:
        print('3')
        br.get(url)  # 在geturl后应该让其 timesleep一下，等页面加载完成后再getpagesource！！
        # time.sleep(0.8)
        wait.until(ec.presence_of_element_located((By.LINK_TEXT, '下一页')))
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

        # 以下可见pyquery更好用！
        html = br.page_source
        doc = pq(html)
        items = doc('.m-itemlist .items .item.J_MouserOnverReq  ').items()
        for item in items:
            biaoti = item.find('.J_ItemPic.img').attr['alt']
            shouhuo = item.find('.deal-cnt').text()[:-3]
            print({'标题': biaoti, 'shouhuo': shouhuo})


url = 'https://s.taobao.com/search?q=ipad&sort=sale-desc'
br = webdriver.Chrome()
wait = WebDriverWait(br, 10)
# br=webdriver.PhantomJS()
urls = get_url(url)
get_page_source(urls)
# br.close()


# //todo:问题1：为什么先运行处于后面的get_page_source(),然后再运行的处于前面的get_url(url)?? 问题2：timesleep怎么设置合理？顺序问题！问题3：目前错误只能打印第一页 问题4:yield应该放在那个缩进位置??

# 特别注意：由于网速可能的快慢关系，需要在br.get(url)后设置不同的timesleep让网页加载完成，否则会出现错误！！

'''为何 运行顺序：运行9999999999999999
运行666666666
'''
'''
urls=get_url(url)
get_page_source(urls)
理解两者的不同之处才能理解上面运行顺序的原因！！！

urls=get_url(url)能不能换成get_page_source(urls)的写法？？如果不能是因为get_url(url)是生成器函数的原因？
'''
