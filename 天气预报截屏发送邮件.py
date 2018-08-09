# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 22:04
@author: Jack Luo
@file: 天气预报截屏发送邮件.py
'''
# 目标:导入近7天深圳天气截屏发送到邮件
# coding='utf-8'
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from selenium import webdriver

url = 'http://www.weather.com.cn/weather1d/101280601.shtml'
picname = 'tianqi.png'

browser = webdriver.PhantomJS()
browser.get(url)
browser.maximize_window()
browser.save_screenshot(picname)
browser.close()

host = 'smtp.163.com'
user = '848'
passwd = 'sho'
sender = '18@163.com'
receivers = ['z@163.com']
mesg = MIMEMultipart()
mesg['From'] = sender
mesg['To'] = receivers[0]
mesg['subject'] = '今天天气预报'

body = """
<h1>今日天气预报</h1>
<img src="cid:image1"/>
"""

mesg.attach(MIMEText(body, 'html'))
with open('tianqi.png', 'rb') as f:
    msgImage = MIMEImage(f.read())
msgImage.add_header('Content-ID', '<image1>')
mesg.attach(msgImage)

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(host, 25)
    smtpObj.login(user, passwd)
    smtpObj.sendmail(sender, receivers, mesg.as_string())
    smtpObj.quit()
    print('ok!')
except:
    print('bad!')
