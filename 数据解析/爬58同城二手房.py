#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 16:27
# @Author  : huni
# @File    : 爬58同城二手房.py
# @Software: PyCharm

import requests
from lxml import etree

if __name__ == '__main__':
    #爬取页面源码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://bj.58.com/ershoufang/'
    page_text = requests.get(url=url,headers=headers).text
    # print(page_text)

    #数据解析
    tree = etree.HTML(page_text)
    #列表里面存储的就是li标签对象
    li_list = tree.xpath("//ul[@class='house-list-wrap']/li")       #xpath返回的是一个列表
    # print(li_list)
    with open('58.txt','w',encoding='utf-8') as fp:
        for li in li_list:
            title = li.xpath('./div[2]/h2/a/text()')[0].replace(' ','')
            price = li.xpath('./div[3]/p/b/text()')[0].replace(' ', '')
            fp.write(title +' 价格：' + price + '万' + '\n')
    print('爬取完成')



