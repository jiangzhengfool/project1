#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 19:58
# @Author  : huni
# @File    : 动作链和iframe操作.py
# @Software: PyCharm

from selenium import webdriver
from time import sleep

from selenium.webdriver import ActionChains     #导入动作链类

#实例化浏览器对象，传入浏览器驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')

#浏览器打开淘宝
dri.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

#定位方框的标签.如果对应的标签存在于iframe中，则必须通过如下操作再进行标签定位
dri.switch_to.frame('iframeResult')     #切换浏览器标签定位的作用域
div = dri.find_element_by_class_name('ui-draggable')

#实例化动作链对象
action = ActionChains(dri)

#点击长按指定的标签
action.click_and_hold(div)

for i in range(5):
    #.perform()表示立即执行动作链操作
    action.move_by_offset(17,0).perform()
    sleep(0.1)

#释放动作链
action.release()

sleep(1)
dri.quit()


