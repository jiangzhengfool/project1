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
    url = 'http://www.renren.com/SysHome.do'
    page_text = requests.get(url=url,headers=headers).text
    tree = etree.HTML(page_text)
    img_url = tree.xpath('//*[@id="verifyPic_login"]/@src')[0]
    img_data = requests.get(url=img_url,headers=headers).content
    with open('./renrenlogincode.jpg','wb') as fp:
        fp.write(img_data)

def loginIn():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    login_url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2020102100997'
    login_data = {
        'email': '17633935269',
        'icode': chaojiying.PostPic(im, 1902)['pic_str'],
        'origURL': 'http://www.renren.com/home',
        'domain': 'renren.com',
        'key_id': '1',
        'captcha_type': 'web_login',
        'password': '5ae3b2b7a5162dfd21cb0a2f192793d3319b70d4c73cde3749b9f05c32ab5e74',
        'rkey': 'c5c08b36d1daef7b10b7ae3c886850e6',
        'f': 'http%3A%2F%2Fwww.renren.com%2F975386238'
    }
    login_page_text = session.post(url=login_url, headers=headers,data=login_data)
    print(login_page_text.status_code)

    with open('./renrenloginpage.html', 'w',encoding='utf-8') as fp:
        fp.write(login_page_text.text)



if __name__ == '__main__':
    #1.获取验证码图片
    getCode()
    #2.识别验证码
    chaojiying = Chaojiying_Client('17633935269', '12345678', '	909647')
    im = open('./renrenlogincode.jpg', 'rb').read()
    print(chaojiying.PostPic(im, 1902))
    #3.模拟登陆
    loginIn()