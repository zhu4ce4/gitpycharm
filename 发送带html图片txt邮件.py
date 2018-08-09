# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:56
@author: Jack Luo
@file: 发送带html图片txt邮件.py
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

host='smtp.163.com'
user='3748'
passwd='sho'

sender='1748@163.com'
receivers=['zh@163.com']

mesg=MIMEMultipart()
mesg['From']=sender
mesg['To']=receivers[0]
mesg['Subject']='日报'

with open('abc.html','r') as f:
    content=f.read()
part1=MIMEText(content,'html','utf-8')

with open('lmn.txt','r') as h:
    content2=h.read()
part2=MIMEText(content2,'plain','utf-8')

part2['Content-Type']='application/octet-stream'
part2['Content-Disposition']="attachment;filename=lmn.txt"

with open('1.jpg','rb') as fp:
    pic=MIMEImage(fp.read())
    pic['Content-Type']='application/octet-stream'
    pic['Content-Disposition']="attachment;filename=1.jpg"

mesg.attach(part1)
mesg.attach(part2)
mesg.attach(pic)

try:
    smtpObj=smtplib.SMTP()
    smtpObj.connect(host,25)
    smtpObj.login(user,passwd)
    smtpObj.sendmail(sender,receivers[0],mesg.as_string())
    print('ok!')
    smtpObj.quit()
except:
    print('bad!')

#需要在正文中加入直接加载的图片
