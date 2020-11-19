#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 20:27
# @Author  : huni
# @File    : 模拟登陆qq空间.py
# @Software: PyCharm

from selenium import webdriver
from time import sleep

from selenium.webdriver import ActionChains     #导入动作链类

#实例化浏览器对象，传入浏览器驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')

#浏览器打开qq空间
dri.get('https://i.qq.com/')

#定位方框的标签.如果对应的标签存在于iframe中，则必须通过如下操作再进行标签定位
dri.switch_to.frame('login_frame')     #切换浏览器标签定位的作用域
a_tag = dri.find_element_by_id('switcher_plogin')

#点击账号密码登陆的超链接
a_tag.click()

#定位方框的标签.如果对应的标签存在于iframe中，则必须通过如下操作再进行标签定位
# dri.switch_to.frame('login_frame')     #切换浏览器标签定位的作用域
u = dri.find_element_by_id('u')             #输入账号框
p = dri.find_element_by_id('p')             #输入密码框
btn = dri.find_element_by_id('login_button')    #登录按钮

#输入qq号和密码
sleep(1)
u.send_keys('1096005725')
sleep(1)
p.send_keys('123456')

#点击登录按钮
sleep(1)
btn.click()













