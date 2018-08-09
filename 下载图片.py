# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:47
@author: Jack Luo
@file: 下载图片.py
'''
import requests
from bs4 import BeautifulSoup

url1 = 'http://www.nationalgeographic.com.cn/animals/'
html = requests.get(url1).text
data = BeautifulSoup(html, 'lxml')
imgurl = data.find_all('ul', {'class': 'img_list'})
for ul in imgurl:
    imgs = ul.find_all('img')
    for img in imgs:
        url = img['src']
        r = requests.get(url, stream=True)
        name = url.split('/')[-1]
        with open('{}'.format(name), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1280):
                f.write(chunk)
