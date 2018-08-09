# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:41
@author: Jack Luo
@file: 代理ip爬取筛选存入sql.py
'''
import requests
import re
import pymysql

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


# 首先获取高匿ip地址
def ip_get(high_ip_url):
    resp = requests.get(high_ip_url, headers=head)
    pattern = re.compile('<td.*?src=.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?高匿.*?<td>(.*?)</td>.*?class="bar_inner fast"',
                         re.S)
    data = re.findall(pattern, resp.text)
    for ipdata in data:
        yield {'http': ipdata[2].lower() + '://' + ipdata[0] + ':' + ipdata[1]}


# 测试ip地址是否一致
def ip_test(ip_test_url):
    for i in ip_get(high_ip_url):
        proxies = {'http': i['http']}
        print(proxies)
        try:
            rs = requests.get(ip_test_url, proxies=proxies, headers=head, timeout=8)
            rs.encoding = rs.apparent_encoding
            pattern = re.compile('<center>您的IP是：\[(.*?)\]', re.S)
            ip_tested = re.findall(pattern, rs.text)
            # 注意! ip_tested是列表,不是上来就是字符串!!!
            print(type(ip_tested))
            if ip_tested:
                # if ip_tested[0] in proxies['http']:#注意,ip_tested是列表,需要切片才能够得到!
                print(rs.text)
                yield proxies['http']
                break
            else:
                continue
                #
        except:
            # print(rs.status_code)
            print('bad')
            continue


def ip_into_sql():
    db = pymysql.connect('localhost', 'root', '123456', 'lianxi', charset='utf8')
    # 为什么上面不能填写'utf_8',只能是'utf8'????
    cr = db.cursor()
    for i in ip_test(ip_test_url):
        sql = 'insert into ip VALUES ("{}")'.format(i)
        cr.execute(sql)
        db.commit()
    db.close()


def main():
    ip_get(high_ip_url)
    ip_test(ip_test_url)
    print('完成!')


if __name__ == '__main__':
    high_ip_url = 'http://www.xicidaili.com/nn'
    ip_test_url = 'http://2017.ip138.com/ic.asp'
    main()
