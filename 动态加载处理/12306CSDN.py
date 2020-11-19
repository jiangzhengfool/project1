#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 9:32
# @Author  : huni
# @File    : 12306CSDN.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

#验证码识别示例
import requests
from hashlib import md5
class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()
    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

#使用selenium打开登录页面
from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC, wait
#实现规避检测
from selenium.webdriver import ChromeOptions

#实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

#创建对象
#executable_path=path:下载好的驱动程序的路径
bro = webdriver.Chrome(executable_path='chromedriver.exe',options=option)
#窗口最大化
bro.maximize_window()
#12306的登录网址
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
bro.execute_script(script)

#点击账号登录
bro.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
time.sleep(1)
while True:
    try:
        #save_screenshot就是将当前页面进行截图且保存
        bro.save_screenshot('aa.png')
        #确定验证码图片对应的左上角和右下角的坐标（裁剪的区域就确定）
        code_img_ele = bro.find_element_by_xpath('//*[@id="J-loginImg"]')
        location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
        #print('location:',location)
        size = code_img_ele.size  #验证码标签对应的长和宽
        #print('size:',size)
        #左上角和右下角坐标
        rangle = (
        int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
        #至此验证码图片区域就确定下来了
        i = Image.open('./aa.png')
        code_img_name = './code.png'
        #crop根据指定区域进行图片裁剪
        frame = i.crop(rangle)
        frame.save(code_img_name)
        #将验证码图片提交给超级鹰进行识别
        chaojiying = Chaojiying_Client('******', '#######', '	909647')	#用户账号>>密码>>软件ID
        im = open('code.png', 'rb').read()									#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        id=chaojiying.PostPic(im, 9004)['pic_id']                           #截取的验证码照片以及验证码的类别代号
        result = chaojiying.PostPic(im, 9004)['pic_str']                    #识别结果
        all_list = [] #要存储即将被点击的点的坐标  [[x1,y1],[x2,y2]]
        #识别错误后，会返回题分，官网给的demo并没有这一句，哈哈哈，坑吧，就是让你多花钱
        chaojiying.ReportError(id)
        if '|' in result:
            list_1 = result.split('|')
            print(list_1)
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
        #遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
        for l in all_list:
            x = l[0]
            y = l[1]
            ActionChains(bro).move_to_element_with_offset(code_img_ele, x, y).click().perform()
            time.sleep(0.5)
        #输入账号和密码
        put1 = bro.find_element_by_id('J-userName')
        #当验证码识别错误后，需要清空账号重新输入
        put1.clear()
        put1.send_keys('*****')  #你的账号
        time.sleep(1)
        put2 = bro.find_element_by_id('J-password')
        put2.clear()
        put2.send_keys('****') #你的密码
        time.sleep(1)
        bro.find_element_by_id('J-login').click()
        #处理提示框
        time.sleep(3)
        span = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        action = ActionChains(bro)
        #点击长按指定的标签
        action.click_and_hold(span)
        action.drag_and_drop_by_offset(span,400,0).perform()
        time.sleep(8)
        while True:
            try:
                info=bro.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span').text
                print(info)
                if info=='哎呀，出错了，点击刷新再来一次':
                    bro.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span/a').click()
                    time.sleep(0.2)
                    span = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
                    action = ActionChains(bro)
                    # 点击长按指定的标签
                    action.click_and_hold(span).perform()
                    action.drag_and_drop_by_offset(span, 400, 0).perform()
                    time.sleep(7)
            except:
                print('ok!')
                break
        #释放动作链
        action.release()
        break
    except:
        time.sleep(3)
time.sleep(12)
#登录成功
bro.find_element_by_link_text('确定').click()
time.sleep(0.5)
bro.find_element_by_link_text('首页').click()
#输入起点、终点以及时间,查询车票
start_city='北京'
end_city='上海'
date='2020-08-05'
#选择起点
bro.find_element_by_xpath('//*[@id="fromStationText"]').click()
time.sleep(2)
#这只遍历了热门城市，要是想遍历其他城市，自己写一个循环就行
city_list=bro.find_elements_by_xpath('//*[@id="ul_list1"]/li')
for city in city_list:
    if city.text==start_city:
        city.click()
        break
time.sleep(2)
#选择终点
bro.find_element_by_xpath('//*[@id="toStationText"]').click()
for city in city_list:
    if city.text==end_city:
        city.click()
        break
time.sleep(2)
js  = "$('input[id=train_date]').removeAttr('readonly')"
bro.execute_script(js)
dt=bro.find_element_by_id('train_date')
dt.clear()
dt.send_keys(date)
time.sleep(2)
bro.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div/div[1]/ul/li[1]/a').click()
time.sleep(0.5)
bro.find_element_by_xpath('//*[@id="isStudentDan"]/i').click()
time.sleep(2)
bro.find_element_by_id('search_one').click()
time.sleep(2)
