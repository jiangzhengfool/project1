#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 19:15
# @Author  : huni
# @File    : selenium淘宝自动化.py
# @Software: PyCharm

from selenium import webdriver
from time import sleep

#实例化浏览器对象，传入浏览器驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')

#浏览器打开淘宝
dri.get('https://www.taobao.com')

#搜索栏标签定位
search_input = dri.find_element_by_name('q')

#标签的交互
search_input.send_keys('iphone')

#搜索按钮的定位
btn = dri.find_element_by_css_selector('.btn-search')

#执行一组js程序
dri.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)

#点击搜索按钮
btn.click()

#浏览器打开百度
dri.get('https://www.baidu.com')
sleep(1)

#回退操作
dri.back()

#前进操作
dri.forward()

#5秒后关闭浏览器
sleep(3)
dri.quit()



