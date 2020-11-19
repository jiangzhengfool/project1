#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 20:22
# @Author  : huni
# @File    : selenium自动刷空间访客.py
# @Software: PyCharm

from selenium import webdriver
from lxml import etree
from time import sleep
from selenium.webdriver import ActionChains     #导入动作链类


#实例化浏览器对象,传入浏览器对象的驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')

#让浏览器发起一个指定url的请求
dri.get('https://yck.ieqq.net/?cid=222')

#实例化动作链对象
action = ActionChains(dri)


#找到免费服务区
select = dri.find_element_by_xpath('//*[@id="cid"]')
value1 = dri.find_element_by_xpath('//*[@id="cid"]/option[13]')
#找到空间访客100个
info = '//option[contains(@value,"5109")]'
value2 = dri.find_element_by_xpath(info)
# select2 = dri.find_element_by_class_name('form-control')
# page_text = dri.page_source

# free = dri.find_element_by_xpath('//*[@id="submit_buy"]')

#点击长按指定的标签
action.click(select)
sleep(1)
action.click(value1)
sleep(1)

action.click(value2)
sleep(1)
# action.click(value2)
# sleep(5)
# # know = dri.find_element_by_id("layui-layer5")
# # action.click(know)
# sleep(1)
# putin = dri.find_element_by_id("inputvalue")
# putin.send_keys('1096005725')
# dri.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# sleep(1)
# action.click(free)
# sleep(5)
# click1 = dri.find_element_by_xpath('//*[@id="captcha"]/div[3]/div[2]/div[1]/div[3]')
# action.click(click1)


dri.quit()





