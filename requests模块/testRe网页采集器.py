#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 10:33
# @Author  : Tony
# @File    : testRe网页采集器.py
# @Software: PyCharm

import requests

def main():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome'
    }
    url = 'https://www.sogou.com/web'
    #处理url携带的参数，封装到字典中
    kw = input('搜索关键词：')
    param = {
        'query':kw
    }
    #对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
    response = requests.get(url=url,params=param,headers=headers)

    page_text = response.text

    fileName = kw + '.html'
    with open(fileName,'w',encoding='utf-8') as fp:
        fp.write(page_text)

    print(fileName,'保存成功!')

if __name__ == '__main__':
    main()