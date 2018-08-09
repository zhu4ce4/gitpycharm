# -*- coding: utf-8 -*-
'''
@time: 2018/8/9 21:58
@author: Jack Luo
@file: 快递跟踪查询.py
'''
import urllib.request
import json


def getExpress(company, code):
    '''funcation: Get Express Infomation
    2 args
    company: the express company code
    code: the express bill code
    '''
    url = 'http://www.kuaidi100.com/query?type={}&postid={}'.format(company, code)
    page = urllib.request.urlopen(url)  # 打开链接，请求快递数据
    return page.read().decode('utf8')


def showResult(jsonStr):
    '''Show the result'''
    jsonObj = json.loads(jsonStr)
    print(u'当前状态：', jsonObj.get('message'), '\n')

    status = jsonObj.get('status')  # 获取状态代码(200是正常)
    if status == '200':
        for x in jsonObj.get('data'):
            print('%s %s' % (x.get('time'), x.get('context')))
            # 可以用下面代码遍历出全面键值
            # for key,value in x.items():
            #   print key,value


if __name__ == '__main__':
    # 测试，顺丰代码：shunfeng
    jsonStr = getExpress('shentong', '3345244712596')
    showResult(jsonStr)
    input('请输入')
