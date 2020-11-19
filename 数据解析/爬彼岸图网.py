#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 18:32
# @Author  : huni
# @File    : 爬彼岸图网.py
# @Software: PyCharm

import requests
from lxml import etree
import os
from pypinyin import lazy_pinyin

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    while True:
        typelist = ['fengjing','meinv','youxi','dongman','yingshi','mingxing','qiche','dongwu','renwu','meishi','zongjiao','beijing']

        print('4K风景,4K美女,4K游戏,4K动漫,4K影视,4K明星,4K汽车,4K动物,4K人物,4K美食,4K宗教,4K背景')
        searchtype = input('请选择爬取的图片类型：4K ')
        res = True      #判断是否全为中文 是中文就返回True
        for w in searchtype:
            if not '\u4e00' <= w <= '\u9fff':
                res = False
        if not res:     #如果不是中文直接赋值给new_searchtype
            new_searchtype = searchtype
            if new_searchtype not in typelist:
                print('输入有误,请重新输入：')
            else:
                getData(new_searchtype,headers)
                break
        else:           #如果是中文就用拼音模块转成拼音再赋值给new_searchtype
            new_searchtype = lazy_pinyin(searchtype)[0] + lazy_pinyin(searchtype)[1]
            if new_searchtype not in typelist:
                print('输入有误,请重新输入：')
            else:
                getData(new_searchtype,headers)
                break


def getData(new_searchtype,headers):

    for i in range(1,4):
        if i == 1:
            url = 'http://pic.netbian.com/4k' + new_searchtype +'/'
        else:
            url = 'http://pic.netbian.com/4k' + new_searchtype +'/' + 'index_' + str(i) + '.html'
        response = requests.get(url=url,headers=headers)
        response.encoding = 'gbk'
        page_text = response.text

        #解析src属性值，解析alt的属性值
        tree = etree.HTML(page_text)
        # with open()
        li_list = tree.xpath('//*[@id="main"]/div[3]/ul/li')

        #创建一个文件夹
        if not os.path.exists('./picLibs'):
            os.mkdir('./picLibs')

        for li in li_list:
            name = li.xpath('./a/img/@alt')[0] + '.jpg'
            src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]
            # print(name,src)

            #请求图片进行储存
            img_data = requests.get(url=src,headers=headers).content
            img_path = 'picLibs/' + name
            with open(img_path,'wb') as fp:
                fp.write(img_data)
                print(name,'下载完成')


if __name__ == '__main__':
    main()
