#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 15:14
# @Author  : Huni
# @File    : 爬一页图（正则）.py
# @Software: PyCharm

import requests
import re
import os

#爬取糗事百科的所有热图
def main():
    #创建一个文件夹用于保存所有的图片内容
    if not os.path.exists('./qiutuLibs'):
        os.makedirs('./qiutuLibs')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    #设置一个通用的url模板
    url = 'https://www.qiushibaike.com/imgrank/page/%d/'
    # pageNum = 1
    for pageNum in range(1,10):
        new_url = format(url%pageNum)   #使页码和url合并，返回一个字符串

        #使用通用爬虫对url进行一页进行爬取
        page_text = requests.get(url=new_url,headers=headers).text       #一页源码用text

        #使用聚焦爬虫将页面中所有的糗图进行解析、提取
        ex = '<div class="thumb">.*?<img src="(.*?)" alt=.*?</div>' #正则表达式
        # 第一个参数是规则，第二个参数是被检索内容，第三个参数re.S是单行匹配
        img_src_list = re.findall(ex,page_text,re.S)
        # print(img_src_list)

        for src in img_src_list:
            src = 'https:' + src    #把图片地址url补充完整
            img_data = requests.get(url=src,headers=headers).content     #content返回的是二进制形式的图片数据
            #生成图片名称
            img_name = src.split('/')[-1]      #对src进行切分，根据'/'进行切分，根据左后一个'/'进行切分
            #图片最终存储的路径
            imgPath = './qiutuLibs/' + img_name
            with open(imgPath,'wb') as fp:
                fp.write(img_data)
                print(img_name,'下载成功')

if __name__ == '__main__':
    main()
