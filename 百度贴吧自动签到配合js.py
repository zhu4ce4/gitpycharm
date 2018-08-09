# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:34
@author: Jack Luo
@file: 百度贴吧自动签到配合js.py
'''
from selenium import webdriver
import time

url='https://baike.baidu.com/starrank?fr=lemmaxianhua'
browser = webdriver.Chrome()
browser.get(url)

for j in range(20):
    time.sleep(2)
    try:
        js="document.getElementsByClassName('pTag next')[1].click();"
        browser.execute_script(js)
        #最后用以上js代码解决
        # button = browser.find_element_by_xpath("//div[@data-cat='thisWeek']/div/a[@class='pTag next']").click()
        #为何上述代码会出错????上述代码在大多数页面正常点击网页的下一页跳转成功,但有几个网页无法点击到网页中的下一页导致需要点击2次才能成功跳转.
        print('跳转到',j+2,'页')
    except:
        print('出错')
print('ok')

#如果要用到这个webdriver功能,一定要先把该功能调试成功正常运行后方能写其他代码,否则,该功能不正常则根本无法使用!
