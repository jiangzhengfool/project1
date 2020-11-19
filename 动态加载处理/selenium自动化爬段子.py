#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 18:22
# @Author  : huni
# @File    : selenium自动化爬药监总局.py
# @Software: PyCharm

from selenium import webdriver
from lxml import etree
from time import sleep
#实例化浏览器对象,传入浏览器对象的驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')

#让浏览器发起一个指定url的请求
dri.get('https://www.qiushibaike.com/text/')

#获取浏览器当前页面的源码数据
page_text = dri.page_source

#解析企业名称
tree = etree.HTML(page_text)
li_list = tree.xpath('//*[@id="content"]/div/div[2]')
for li in li_list:
    au = li.xpath('./div[1]/a[2]/h[2]/text()')[0]
    print(au)

sleep(5)
dri.quit()
