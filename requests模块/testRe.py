#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 9:51
# @Author  : Tony
# @File    : testRe.py
# @Software: PyCharm

import requests

def main():
    #step1:指定url
    url = 'https://www.sogou.com/'
    #step2:发起请求
    #get方法会返回一个响应对象
    response = requests.get(url=url)
    #step3:获取响应数据
    #使指定url的网页源码数据以字符串的形式返回给page_text
    page_text = response.text
    print(page_text)
    #step4:储存数据
    with open('./sougou.html','w',encoding='utf-8') as fp:
        fp.write(page_text)
    print('爬取成功！')

if __name__ == '__main__':
    main()


