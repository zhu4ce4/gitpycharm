# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:54
@author: Jack Luo
@file: 非ajax网页的绕过登录.py
'''
from selenium import webdriver
import pickle
import requests
from selenium.webdriver.common.keys import Keys
import time
url='https://www.jianshu.com/users/be71e0fef175/timeline'
head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

option=webdriver.ChromeOptions()
option.add_argument('user-data-dir=C:/Users/LQJ/AppData/Local/Google/Chrome/User Data')
d=webdriver.Chrome(chrome_options=option)
d.get(url)
cookies=d.get_cookies()
# with open('cook.pickle','wb') as f:
#     pickle.dump(cookies,f)
d.close()

# with open('cook.pickle','rb') as f:
#     cookies=pickle.load(f)
r=requests.Session()
for cookie in cookies:
    r.cookies.set(cookie['name'],cookie['value'])
resp = r.get(url,headers=head)
print('状态:',resp.status_code)
print(resp.text)



#只能用于非ajax的网页,如果是ajax,则不适用,因为获取的resp的text的内容是网页源代码,非ajax加载后的页面
