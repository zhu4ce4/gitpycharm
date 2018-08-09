# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:50
@author: Jack Luo
@file: 新闻天气头条邮件推送.py
'''
from datetime import date
import requests
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from lxml import etree
import time

def yeshu():
    url = 'http://cnepaper.com/ycrb/html/{}/{}/node_{}.htm'.format(nianyue,ri, 1)
    resp=requests.get(url,headers=headers)
    resp.encoding=resp.apparent_encoding
    pattern=re.compile('<td.*?class="default".*?id="pageLink".*?node_(.*?).htm">(.*?)</a></td>',re.S)
    res=re.findall(pattern,resp.text)
    if res:
        for i in res:
            yield {'页数':i[0],'栏目':i[1]}
    else:
        print('当日无永川日报新闻')
        with open('{}.txt'.format(nianyue + ri), 'a+') as f:
            f.write('当日无永川日报新闻!')

def meiye():
    for i in yeshu():
        url = 'http://cnepaper.com/ycrb/html/{}/{}/node_{}.htm'.format(nianyue, ri, i['页数'])
        resp=requests.get(url,headers=headers)
        resp.encoding = resp.apparent_encoding
        pattern=re.compile('<div.*?inline.*?href="(.*?)">(.*?)</a>',re.S)
        res=re.findall(pattern,resp.text)
        for j in res:
            if '广告' in j[1]:
                continue
            else:
                yield {'标题':j[1],'链接':j[0]}

def xieru():
    with open('{}.txt'.format(nianyue+ri),'a+') as f:
        for i in meiye():
            f.write(i['标题']+'http://cnepaper.com/ycrb/html/2018-01/11/'+i['链接']+'\n')
        f.write('\n'*2)

def tianqi():
    url = 'http://www.szmb.gov.cn/site/szmb/jinmingtianqiyubao/index.html'
    brs = webdriver.PhantomJS()
    brs.get(url)
    resp = brs.page_source
    pattern = re.compile('class="show_weather".*?color.*?>(.*?)</div>', re.S)
    tianqi = re.findall(pattern, resp)[0]
    with open('{}.txt'.format(nianyue + ri), 'a+') as f:
        f.write(str(tianqi)+'\n'*2)
        # f.write()
    brs.close()

def get(headers):
    # head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    resp=requests.get('http://money.163.com/',headers=headers)
    resp.encoding=resp.apparent_encoding
    data=etree.HTML(resp.text)
    biaoti=data.xpath("//ul[@class='topnews_nlist']/li/h2/a/text()|//ul[@class='topnews_nlist']/li/h3/a/text()|//ul[@class='topnews_nlist mb20 no_border']/li/h2/a/text()|//ul[@class='topnews_nlist mb20 no_border']/li/h3/a/text()")
    lianjie=data.xpath("//ul[@class='topnews_nlist']/li/h2/a/@href|//ul[@class='topnews_nlist']/li/h3/a/@href|//ul[@class='topnews_nlist mb20 no_border']/li/h2/a/@href|//ul[@class='topnews_nlist mb20 no_border']/li/h3/a/@href")
    for(x,y)in zip(biaoti,lianjie):
        yield {'标题':x,"链接":y}

def xiejin():
    with open('{}.txt'.format(nianyue+ri), 'a+') as f:
        for i in get(headers):
            f.write(i['标题']+i['链接']+'\n'*2)

def fayoujian():
    with open('{}.txt'.format(nianyue+ri),'r') as f:
        file=f.read()
    host = 'smtp.163.com'
    user = '13760338748'
    passw = 'shou4quan2ma3'
    sender = '13760338748@163.com'
    receivers = ['zhu4ce4@163.com']
    mesg = MIMEText(file, 'plain', 'utf-8')
    mesg['From'] = sender
    mesg['To'] = ','.join(receivers)
    mesg['subject'] = '{}{}永川日报+深圳天气+网易财经头条+微信搜索+永川网搜索'.format(nianyue, ri)
    try:
        smtpObj=smtplib.SMTP()
        smtpObj.connect(host,25)
        smtpObj.login(user,passw)
        smtpObj.sendmail(sender,receivers,mesg.as_string())
        smtpObj.quit()
        print('发送成功')
    except:
        print('发送失败!')

def canshu(br,city,biaoti):
    br.find_element_by_id("query").clear()
    br.find_element_by_id("query").send_keys(city)
    br.find_element_by_id("query").send_keys(Keys.ENTER)
    time.sleep(2)
    br.find_element_by_id("tool_show").click()
    br.find_element_by_id("time").click()
    br.find_element_by_link_text("一天内").click()
    getsource(br,biaoti)

def getsource(br,biaoti):
    time.sleep(0.5)
    data=br.page_source
    html=etree.HTML(data)
    biaoti0=html.xpath("//div[@class='txt-box']/h3//a//text()")
    biaoti.extend(biaoti0)
    loop(br,biaoti)

def loop(br,biaoti):
    try:
        br.find_element_by_link_text('下一页').click()
        getsource(br,biaoti)
    except:
        print('没有下一页了')
        pass

def get_data(city):
    data={'sort':'date','contentKey':'{}'.format(city),'op':'single','siteID':None}
    resp=requests.post(url='http://search.ycw.gov.cn/servlet/SearchServlet.do',headers=headers,data=data)
    pattern=re.compile('<td.*?style.*?<a href="(.*?)" target="_blank">(.*?)</a>',re.S)
    data=re.findall(pattern,resp.text)
    for i in data[0:4]:
        yield {'title':i[1].replace('</span>','').replace("<span class='highlight'>",''),'link':i[0]}

def xie_ru(city):
    with open('{}.txt'.format(nianyue+ri), 'a+') as f:
        for i in get_data(city):
            f.write(i['title'] + i['link'] + '\n' * 2)

def main():
    yeshu()
    meiye()
    xieru()
    tianqi()
    get(headers)
    xiejin()
    for city in citys:
        get_data(city)
        xie_ru(city)

    br = webdriver.PhantomJS()
    br.get('http://weixin.sogou.com/')
    for city in citys:
        biaoti = []
        canshu(br,city,biaoti)
        with open('{}.txt'.format(nianyue + ri), 'a+') as f:
            for i in biaoti:
                i = i.replace('\u200b', '')
                f.write(i + '\n')
    br.close()
    fayoujian()

if __name__ == '__main__':
    nianyue = str(date.today())[:7]
    ri = str(date.today())[8:10]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    citys = ['朱沱', '松溉', '何埂', '永川港桥']
    main()
