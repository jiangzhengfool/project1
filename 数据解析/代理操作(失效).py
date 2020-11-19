#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 11:11
# @Author  : huni
# @File    : 代理操作(失效).py
# @Software: PyCharm

import requests

url = 'http://ip293.net/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
page_text = requests.get(url=url,headers=headers,proxies={'http':'175.42.68.176'}).text

with open('ip.html','w',encoding='utf-8') as fp:
    fp.write(page_text)