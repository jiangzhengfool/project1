#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 10:48
# @Author  : huni
# @File    : test.py
# @Software: PyCharm
from selenium.webdriver import ChromeOptions
from selenium import webdriver
#实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

#创建对象
#executable_path=path:下载好的驱动程序的路径
bro = webdriver.Chrome(executable_path='chromedriver.exe',options=option)