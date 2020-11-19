#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 21:23
# @Author  : huni
# @File    : 爬简历模板.py
# @Software: PyCharm

import requests
from lxml import etree
import os


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    for i in range(1,3):    #爬前两页
        if i == 1:
            url = 'http://sc.chinaz.com/jianli/free.html'
            getRar(url,headers)
        else:
            url = 'http://sc.chinaz.com/jianli/free_' + str(i) + '.html'
            getRar(url,headers)

def getRar(url,headers):
    page_text = requests.get(url=url,headers=headers).text

    tree = etree.HTML(page_text)

    img_list = tree.xpath('//*[@id="container"]/div')
    # print(img_list)

    # 创建一个文件夹
    if not os.path.exists('./jianliLibs'):
        os.mkdir('./jianliLibs')

    for a in img_list:
        img_link = a.xpath('./a/@href')[0]
        # print(img_link)
        in_url = 'http:' + img_link
        in_text = requests.get(url=in_url,headers=headers).text

        in_tree = etree.HTML(in_text)
        dow_list = in_tree.xpath('//*[@id="down"]/div[2]/ul/li[6]')
        for d in dow_list:
            dow_url = d.xpath('./a/@href')[0]
            # print(dow_link)
            rarData = requests.get(url=dow_url,headers=headers).content
            rarname = dow_url.split('/')[-1]    #每个简历rar文件的名字是链接切片的/后的所有字符串
            rar_path = 'jianliLibs/' + rarname
            with open(rar_path, 'wb') as fp:
                fp.write(rarData)
                print(rarname, '下载完成')

if __name__ == '__main__':
    main()

