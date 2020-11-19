#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 8:47
# @Author  : huni
# @File    : 人人网模拟登陆(失效).py
# @Software: PyCharm



from  lxml import etree
from chaojiying import *    #超级鹰模块里面有requests模块，不用再次导入

#1.获取验证码图片文件
def getCode():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://www.chaojiying.com/user/login/'
    page_text = requests.get(url=url,headers=headers).text
    tree = etree.HTML(page_text)
    img_url = 'https://www.chaojiying.com/' + tree.xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img/@src')[0]
    img_data = requests.get(url=img_url,headers=headers).content
    with open('./chaojiyinglogincode.jpg','wb') as fp:
        fp.write(img_data)

def loginIn():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    login_url = 'https://www.chaojiying.com/user/login/'
    login_data = {
        'user': '17633935269',
        'pass': '12345678',
        'imgtxt': chaojiying.PostPic(im, 1902)['pic_str'],
        'act': '1'
    }
    login_page_text = requests.post(url=login_url, headers=headers,data=login_data)
    print(login_page_text.status_code)

    with open('./chaojiying.html', 'w',encoding='utf-8') as fp:
        fp.write(login_page_text.text)


if __name__ == '__main__':
    #1.获取验证码图片
    getCode()
    #2.识别验证码
    chaojiying = Chaojiying_Client('17633935269', '12345678', '	909647')
    im = open('./chaojiyinglogincode.jpg', 'rb').read()
    print(chaojiying.PostPic(im, 1902))
    #3.模拟登陆
    loginIn()