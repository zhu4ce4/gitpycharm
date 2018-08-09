# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:53
@author: Jack Luo
@file: 免费代理ip存入sql.py
'''
import requests
import pymysql

'''
ip来源=http://proxy.nghuyong.top
教程=http://blog.csdn.net/nghuyong/article/details/78415048
'''

db=pymysql.connect('localhost','root','123456','lianxi',charset='utf8')
cr=db.cursor()
head={"User-Agent":'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def ip_in_sql():
    proxydata=requests.get('http://proxy.nghuyong.top/').json()['data']
    for i in proxydata:
        if i['anonymity']=='high_anonymity':
            ip_test(weizhi=i)


            #在写入之前还要先看看是否在数据库里面已经存在,如果已存在,则不应写入!!!该代码如何添加??????

            sql="insert into 高匿名proxy VALUES ('{}','{}',{},'{}')".format(i['country'],i['type'],i['round_trip_time'],i['ip_and_port'])
            cr.execute(sql)
            db.commit()
        else:
            pass
    print('ip已存入mysql')

def ip_out_sql():
    cr.execute('select * from 高匿名proxy')
    get_ip=cr.fetchall()
    for i in get_ip:
        yield {'type':i[1],'ip_and_port':i[-1]}


def ip_test(weizhi):
    for ip in weizhi:
        proxies={'http':ip['type']+'://'+ip['ip_and_port']}
        rs=requests.get('http://2017.ip138.com/ic.asp',proxies=proxies,headers=head)
        rs.encoding=rs.apparent_encoding
        if rs.status_code==200:
            print('成功! status_code为200')
            print(proxies)
            break
            #上面用break而不是用pass,更不是continue
        else:
            continue

if __name__ == '__main__':
    ip_in_sql()
    ip_out_sql()
    ip_test(weizhi)
    print('已跳出!')
