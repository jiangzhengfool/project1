#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 10:33
# @Author  : Tony
# @File    : testRe网页采集器.py
# @Software: PyCharm

import requests
import json

def main():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome'
    }
    url = 'https://movie.douban.com/j/chart/top_list'   # url中 ？后面的参数都可以做动态请求，可以封装进字典
    #处理url携带的参数，封装到字典中
    # kw = input('搜索关键词：')
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action': '',
        'start': '0',     #从第几部电影取
        'limit': '20'       #一次请求的个数是几个
    }
    #对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
    response = requests.get(url=url,params=param,headers=headers)

    # json方法返回的是一个列表对象（如果确认服务器相应的类型是json，才能使用json方法）
    # 返回的对象类型在response里面看
    list_data = response.json()

    fileName = 'douban.json'
    with open(fileName,'w',encoding='utf-8') as fp:
        json.dump(list_data,fp=fp,ensure_ascii=False)

    print(fileName,'保存成功!')

if __name__ == '__main__':
    main()