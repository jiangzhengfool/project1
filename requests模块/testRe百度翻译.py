#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 10:33
# @Author  : Tony
# @File    : testRe网页采集器.py
# @Software: PyCharm

import requests
import json

def main():
    post_url = 'https://fanyi.baidu.com/sug'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    #处理url携带的参数，封装到字典中
    kw1 = input('搜索关键词：')
    data = {
        'kw':kw1
    }
    #对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
    response = requests.post(url=post_url,data=data,headers=headers)
    #json方法返回的是一个字典对象（如果确认服务器相应的类型是json，才能使用json方法）
    #返回的对象类型在response里面看
    #在检查页面network>name>headers>Response Headers的content-type: application/json确认相应类型是否为json类型
    dic_obj = response.json()
    # print(dic_obj)

    fileName = kw1 + '.json'
    with open(fileName,'w',encoding='utf-8') as fp:
        json.dump(dic_obj,fp=fp,ensure_ascii=False)     #返回的中文json不能同ASCII码进行编码的所以赋值false
    print(fileName,'保存成功!')

if __name__ == '__main__':
    main()