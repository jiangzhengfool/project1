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
dri.get('http://scxk.nmpa.gov.cn:81/xk/')

#获取浏览器当前页面的源码数据
page_text = dri.page_source

#解析企业名称
tree = etree.HTML(page_text)
li_list = tree.xpath('//*[@id="gzlist"]/li')
for li in li_list:
    name = li.xpath('./dl/@title')[0]
    print(name)

sleep(5)
dri.quit()
