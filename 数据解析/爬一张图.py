#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 14:44
# @Author  : Tony
# @File    : 爬一张图.py
# @Software: PyCharm

import requests
import re

#爬取糗事百科的所有热图
def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://pic.qiushibaike.com/system/pictures/12376/123766971/medium/AN0DUC4FDLAXIZFQ.jpg'
    # text > 字符串 ， content > 二进制 ， json > 对象
    img_data = requests.get(url=url,headers=headers).content        #content返回的是二进制形式的图片数据

    with open('./1.jpg','wb') as fp:
        fp.write(img_data)

if __name__ == '__main__':
    main()