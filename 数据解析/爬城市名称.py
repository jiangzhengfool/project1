#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 20:39
# @Author  : huni
# @File    : 爬城市名称.py
# @Software: PyCharm

import requests
from lxml import etree

if __name__ == '__main__':
    #分两次解析
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    # }
    # url = 'https://www.aqistudy.cn/historydata/'
    # page_text = requests.get(url=url,headers=headers).text
    #
    # tree = etree.HTML(page_text)
    #
    # top_city_list = tree.xpath('/html/body/div[3]/div/div[1]/div[1]/div[2]/ul/li')
    # # print(top_city_list)
    # all_city_names = []
    # for li in top_city_list:
    #     top_city_name = li.xpath('./a/text()')[0]
    #     all_city_names.append(top_city_name)
    #
    # com_city_list = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li')
    # for li in com_city_list:
    #     com_city_name = li.xpath('./a/text()')[0]
    #     all_city_names.append(com_city_name)
    # print(all_city_names,len(all_city_names))


    #解析一次
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://www.aqistudy.cn/historydata/'
    page_text = requests.get(url=url, headers=headers).text

    tree = etree.HTML(page_text)

    top_city_list = tree.xpath('/html/body/div[3]/div/div[1]/div[1]/div[2]/ul/li')

    #解析热门城市和全部城市相对应的a标签
    #/html/body/div[3]/div/div[1]/div[1]/div[2]/ul/li/a         热门城市的
    #/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a      全部城市的
    all_city_list = tree.xpath('/html/body/div[3]/div/div[1]/div[1]/div[2]/ul/li/a | /html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a')
    all_city_names = []
    for li in all_city_list:
        all_city_name = li.xpath('./text()')[0]
        all_city_names.append(all_city_name)
    print(all_city_names,len(all_city_names))