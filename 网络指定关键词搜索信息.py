# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:52
@author: Jack Luo
@file: 网络指定关键词搜索信息.py
'''
import requests
import re

url='http://search.ycw.gov.cn/servlet/SearchServlet.do'
head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_data(keyword):
    data={'sort':'date','contentKey':'{}'.format(keyword),'op':'single','siteID':None}
    resp=requests.post(url,headers=head,data=data)
    pattern=re.compile('<td.*?style.*?<a href="(.*?)" target="_blank">(.*?)</a>',re.S)
    data=re.findall(pattern,resp.text)

    # html=etree.HTML(resp.text)
    # link=html.xpath('//tr[@class="TableBody1"]/td/a[1]/text()')
    # print(link)
    for i in data[0:4]:
        yield {'title':i[1].replace('</span>','').replace("<span class='highlight'>",''),'link':i[0]}

def print_out():
    for i in get_data(keyword):
        print(i['title']+':  '+i['link'])
        print('    ')

def main(keyword):
    get_data(keyword)
    print_out()

if __name__ == '__main__':
    keywords=['朱沱','松溉','何埂']
    for keyword in keywords:
        main(keyword)
        print('**************我*是*分*割*线**************')
