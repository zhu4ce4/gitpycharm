# -*- coding: utf-8 -*-
'''
@time: 2018/8/10 8:34
@author: Jack Luo
@file: 头条街拍下载图片.py
'''
import requests
from urllib.parse import urlencode
import re
import os
from hashlib import md5
from multiprocessing.pool import Pool

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36','x-requested-with': 'XMLHttpRequest'}


def get_page(offset):
    params={'offset':offset,'format':'json','keyword':'重庆街拍','autoload':'true','count':20,'cur_tab':1}
    url='https://www.toutiao.com/search_content/?'+urlencode(params)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()  #调用 response的 json （）方法将结果转为 JSON 格式
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title'):
                title=item.get('title')
                images=item.get('image_list')
                for image in images:
                    last_url=image['url']
                    if re.search('image/(.*)',last_url):
                        last_url=re.search('image/(.*)',last_url).group(1)
                        url = 'http://p3.pstatp.com/origin/pgc-image/'+ last_url
                        yield {'image_url':url,'title':title}
                    # elif re.match('//.*/(.*)',last_url).group(1):
                    elif re.match('//.*/(.*)',last_url):
                        last_url = re.match('//.*/(.*)', last_url).group(1)
                        url = 'http://p3.pstatp.com/origin/'+ last_url
                        yield {'image_url': url, 'title': title}
                    else:
                        print('bad')
            else:
                continue

def save_image(item):
    if not os.path.exists(item['title']):
        os.mkdir(item['title'])
    try:
        response=requests.get(item['image_url'])
        if response.status_code==200:
            file_path="{}/{}.{}".format(item['title'],md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('already downloaded',file_path)
    except requests.ConnectionError:
        print('failed to save image')

def main(offset):
    json=get_page(offset)
    for item in get_images(json):
        save_image(item)

group_start=0
group_end=5

if __name__ == '__main__':
    pool=Pool()
    groups=([x*20 for x in range(group_start,group_end)])
    pool.map(main,groups)
    pool.close()
    pool.join()
