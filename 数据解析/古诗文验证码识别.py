#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 8:16
# @Author  : huni
# @File    : 古诗文验证码识别.py
# @Software: PyCharm


from  lxml import etree
from chaojiying import *

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    page_text = requests.get(url=url,headers=headers).text

    tree = etree.HTML(page_text)

    img_url = 'https://so.gushiwen.cn' + tree.xpath('//*[@id="imgCode"]/@src')[0]

    img_data = requests.get(url=img_url,headers=headers).content

    with open('./gushiwencode.jpg','wb') as fp:
        fp.write(img_data)

if __name__ == '__main__':
    main()
    chaojiying = Chaojiying_Client('17633935269', '12345678', '	909647')
    im = open('./gushiwencode.jpg', 'rb').read()
    print(chaojiying.PostPic(im, 1902))