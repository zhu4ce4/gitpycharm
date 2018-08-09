# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:10
@author: Jack Luo
@file: 代理ip获取及测试.py
'''
from pyquery import PyQuery as pq
import requests
import telnetlib


ip_url = 'http://www.xicidaili.com/nn/1'
ip_test_url = 'http://httpbin.org/get'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'}

def get_ip(ip_url):
    response = requests.get(ip_url, headers=headers).text
    doc = pq(response)
    items = doc('#ip_list td.country').items()
    for item in items:
        if item.siblings()[3].text == '高匿':
            ip = item.siblings()[0].text
            port = item.siblings()[1].text
            # typ = item.siblings()[4].text
            # yield ('{}://{}:{}'.format(typ,ip,port).lower())
            yield [ip,port]
        else:
            continue

def test_ip():
    for ip in ips:
        proxies={'http':'http://{}:{}'.format(ip[0],ip[1]),'https':'https://{}:{}'.format(ip[0],ip[1])}
        # try:
            # global response
            # response = requests.get(ip_test_url, proxies=ip,headers=headers).json()
        response = requests.get(url='http://ip.chinaz.com/getip.aspx/', proxies=proxies,headers=headers).json()
        print(response)
        #     if response['ip'] in ip:
        #         print('生效的代理ip:', ip, '被检测的ip:', response['origin'])
        #         # yield ip
        #     elif response['origin'] == '106.80.196.179':
        #         print('真实的ip被返回，不能做代理的ip：', ip)
        #     else:
        #         print('返回为空')
        # except:
        #     print('try出错[Auth Result: 禁止外部用户]，没能测试ip:', ip)
        #     continue

        try:
            telnetlib.Telnet(ip[0],port=ip[1],timeout=4)
        except:
            print('failed:',ip)
        else:
            print(':'.join([ip[0],ip[1]]))

#TODO:将通过testip的ip写入redis

ips = get_ip(ip_url)
test_ip()
