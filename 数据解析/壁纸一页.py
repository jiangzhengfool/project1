#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/15 8:22
# @Author  : huni
# @File    : 壁纸一页.py
# @Software: PyCharm

import requests
from lxml import etree
import os

if __name__ == '__main__':
    if not os.path.exists('./4tupian'):
        os.mkdir('./4tupian')
    # 第一步
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    # 这里是UA伪装
    url = 'https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&page=17'
    url_text = requests.get(url=url,headers=headers).text
    #   获取url内容
    tree = etree.HTML(url_text)
    li_list = tree.xpath('/html/body/div[2]/div[5]/div')
    #   这里最后要加上/div   这表示要在/div这里遍历了
    #   ---------------------------------------------------------------------------
    #   接下来准备把这一整页的图片展示，包括图片的路径，图片的名字

    for li in li_list:


        img_src = li.xpath('./div[1]/div[1]/a/@href')[0]
    #   这里试错了很多次，说明这里很需要注意，尽量一个一个秃噜下来
        img_src = 'https://wall.alphacoders.com/' + img_src
        url_text_new = requests.get(url=img_src, headers=headers).text
        tree_new = etree.HTML(url_text_new)

        img_src_new = tree_new.xpath('/html/body/div[2]/div[4]/a/@href')[0]
        img_src_new_ahead = img_src_new.split('/')[0:4]
        img_src_new_behind = img_src_new.split('/')[-1]
        img_src_new2 = '/'.join(img_src_new_ahead) + "/" + img_src_new_behind
        img_name = img_src_new_behind
        img_name = img_name.encode('iso-8859-1').decode('gbk')
    # #   通用的中文乱码处理方式
    # #   比较重要
    #   ----------------------------------------------------------------------------
        print(img_src_new2, img_name)
    #   接收url的二进制内容
        img_data = requests.get(url=img_src_new2,headers=headers).content
        img_path = '4tupian/' + img_name
    #     #   如果这里使用 ./4tupian 代码会在代码同层级的包里新创建这样的图片
        with open(img_path,'wb') as pf:
            #   这里的必须是 'wb' 而不能是 'w'
            pf.write(img_data)
            print(img_name + "下载成功！!!")
