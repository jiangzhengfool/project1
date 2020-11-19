#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 21:04
# @Author  : huni
# @File    : 无头浏览器和规避检测.py
# @Software: PyCharm

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options       #实现无可视化界面操作
from selenium.webdriver import ChromeOptions                #实现规避检测

#创建一个参数对象，用来控制Chrome以无界面化的模式打开
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#实现规避被检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])


#如何实现让selenium规避被检测到的风险
dri = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=chrome_options,options=option)

#无可视化界面（无头浏览器）
dri.get('https://www.baidu.com')

print(dri.page_source)
sleep(2)
dri.quit()