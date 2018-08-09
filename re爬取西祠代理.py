# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:09
@author: Jack Luo
@file: re爬取西祠代理.py
'''
import requests
import re
import telnetlib
import pymongo

headers={'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}


def get_ip():
    url = 'http://www.xicidaili.com/nn/'
    response = requests.get(url, headers=headers).text
    for (ipp, _, port, typ) in re.findall(r'<td>((\d{1,3}.){3}\d{1,3})<.*?<td>(.*?)</td>.*?高匿.*?<td>(.*?)</td>',response,re.S):
        # ip=typ.lower()+'://'+ip+':'+port
        # ip=ipp+':'+port
        # yield ip
        yield (ipp,port)


def test_ip():
    test_url = 'http://httpbin.org/get'
    for ip in ip_untest:
        pro={'https':ip[0]+':'+ip[1],'http':ip[0]+':'+ip[1]}
        # pro={'{}'.format(ip[2]):ip[0]+':'+ip[1]}
        try:
            resp=requests.get(test_url,proxies=pro,headers=headers,timeout=3).json()
            if resp['origin']==ip[0]:
        # resp=requests.get(test_url,proxies={'{}':ip,'http':ip},headers=headers).json()
                yield ip[0]+':'+ip[1]
            else:
                print(ip)
                raise ConnectionError
        except:
            try:
                telnetlib.Telnet(ip[0], port=ip[1], timeout=3)
            except:
                continue
            else:
                yield ip[0]+':'+ip[1]

def insert_mongodb():
    for ip in ip_tested:
        db = pymongo.MongoClient('localhost')['代理ip池']
        db['代理ip池'].insert_one({'ip':ip})

ip_untest=get_ip()
ip_tested=test_ip()
insert_mongodb()
# todo:把得到的ip写入代理ip池
