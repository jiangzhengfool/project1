#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 21:24
# @Author  : huni
# @File    : 模拟12306登录(基于selenium).py
# @Software: PyCharm

from selenium import webdriver
import time                     #设置延迟，
from chaojiying import *        #解析验证码
from selenium.webdriver import ActionChains     #导入动作链类
from PIL import Image       #用作验证码图片裁剪

#实例化浏览器对象，传入浏览器驱动程序
dri = webdriver.Chrome(executable_path='./chromedriver.exe')
dri.maximize_window()       #使窗口最大化

#浏览器打开12306
dri.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(1)

#定位账号密码登录超链接
a_tag = dri.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a')

#点击账号密码登陆的超链接
a_tag.click()

#截图全屏页面
time.sleep(2)       #这里设置一个2s的延迟，预防网络比较差的条件下加载不出验证码图片
dri.save_screenshot('aa.png')

#确定验证码图片对应的左上角和右下角的坐标（裁剪的区域就确定）
code_img_ele = dri.find_element_by_xpath('//*[@id="J-loginImg"]')
location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
print('location:',location)
size = code_img_ele.size  #验证码标签对应的长和宽
print('size:',size)
#左上角和右下角坐标
rangle = (
int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
#至此验证码图片区域就确定下来了
print(rangle)

i = Image.open('./aa.png')
code_img_name = './code.png'
#crop根据指定区域进行图片裁剪
frame = i.crop(rangle)
frame.save(code_img_name)

#超级鹰解析验证码
chaojiying = Chaojiying_Client('****', '****', '	909647')	#用户中心>>软件ID 生成一个替换 96001
im = open('code.png', 'rb').read()										#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
print (chaojiying.PostPic(im, 9004)['pic_str'])

result = chaojiying.PostPic(im, 9004)['pic_str']
all_list = [] #要存储即将被点击的点的坐标  [[x1,y1],[x2,y2]]
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
print(all_list)

#遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
for l in all_list:
    x = l[0]
    y = l[1]
    #把验证码图片的坐标切换到验证码本身的坐标系点击，而不是全屏坐标系点击
    ActionChains(dri).move_to_element_with_offset(code_img_ele, x, y).click().perform()
    time.sleep(0.5)

#输入用户名密密码点击登陆
dri.find_element_by_id('J-userName').send_keys('******')
time.sleep(2)
dri.find_element_by_id('J-password').send_keys('*****')
time.sleep(2)
dri.find_element_by_id('J-login').click()



time.sleep(3)
span = dri.find_element_by_xpath('//*[@id="nc_1_n1z"]')
action = ActionChains(dri)
#点击长按指定的标签
action.click_and_hold(span).perform()
for i in range(3):
    #.perform()表示立即执行动作链操作
    action.drag_and_drop_by_offset(span,150*i,0).perform()
    time.sleep(0.1)
# action.drag_and_drop_by_offset(span,400,0).perform()
time.sleep(8)
while True:
    try:
        info=dri.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span').text
        print(info)
        if info=='哎呀，出错了，点击刷新再来一次':
            dri.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span/a').click()
            time.sleep(0.2)
            span = dri.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            action = ActionChains(dri)
            # 点击长按指定的标签
            action.click_and_hold(span).perform()
            for i in range(3):
                # .perform()表示立即执行动作链操作
                action.drag_and_drop_by_offset(span, 150*1, 0).perform()
                time.sleep(0.1)
            # action.drag_and_drop_by_offset(span, 400, 0).perform()
            time.sleep(7)
    except:
        print('ok!')
        break
#释放动作链
action.release()


time.sleep(300)
dri.quit()

