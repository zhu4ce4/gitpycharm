# -*- coding: utf-8 -*-
'''
@time: 2018/8/10 8:35
@author: Jack Luo
@file: 移动版微博ajax爬取.py
'''
# ajax微博信息提取

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']

base_url = 'http://m.weibo.cn/api/container/getIndex?'

headers = {'Hosts': 'm.weibo.cn', 'Referer': 'https://m.weibo.cn/u/2830678474',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}


def get_page(page):
    params = {'type': 'uid', 'value': '2830678474', 'containerid': '1076032830678474', 'page': page}
    url = base_url + urlencode(params)  # 调用 urlencode （）方法将参数转化为  URL 的GET 请求参数
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # 直接调用 json （）方法将内容解析为 JSON返回
    except requests.ConnectionError as e:
        print('error', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            if item.get('card_type') == 9:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()  # 这里我们借助 pyquery 将正文中的 HTML 标签去掉
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo
            else:
                continue


def save_to_mongo(result):
    if collection.insert(result):
        print('saved to mongo')


if __name__ == '__main__':
    for page in range(1, 3):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            save_to_mongo(result)
