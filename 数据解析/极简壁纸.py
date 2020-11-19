#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 13:16
# @Author  : huni
# @File    : 极简壁纸.py
# @Software: PyCharm

import requests
import json
import time
import random
import threading
from queue import Queue
import os


# 返回一页的 Json数据
def get_one_page(pageNum, target):
    # pageNum：第几页
    # target：类型
    data = {
        'pageNum': pageNum,
        'target': target
    }

    # 用户头代理
    USER_AGENT_LIST = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    ]

    # 请求头
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "access": "b9abb5db9f95e0439fe7d885123696e907d1352c3909ab0035a346168cfc5679",
        "content-length": "30",
        "location": "bz.zzzmh.cn",
        "origin": "https://bz.zzzmh.cn",
        "referer": "https://bz.zzzmh.cn/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sign": "f566907d5b5fc72aa0d9df9674cfcebf",
        "timestamp": "1585403003757",
        'Content-Type': 'application/json',
        'User-Agent': random.choice(USER_AGENT_LIST)
    }

    # # 代理池，免费给的没用=.=
    # http = [
    #     'HTTP://125.110.64.117:9000'.lower(),
    #     'HTTP://110.243.30.216:9999'.lower(),
    #     'HTTP://114.99.7.3:1133'.lower(),
    #     'HTTP://14.219.16.19:8118'.lower(),
    #     'HTTP://106.1.118.115:9064'.lower(),
    #     'HTTP://117.162.204.97:8123'.lower(),
    # ]
    # https = [
    #     'https"//117.114.149.66:53281',
    #     'https"//139.196.140.179:8888',
    #     'https"/121.237.149.75:3000',
    # ]
    #
    # proxies = {
    #     'http':random.choice(http),
    #     'https':random.choice(https)
    # }

    url = "https://api.zzzmh.cn/bz/getJson"

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # print(response.json())
        return response.json(), target
    except:
        return None


# 获取一页壁纸的url地址
def get_img_url(jsons):
    if jsons == None:
        return None

    pub_url = "https://th.wallhaven.cc/small/"

    records = jsons[0]['result']['records']

    for recode in records:
        img_url = pub_url + r"/" + recode['i'][:2] + r'/' + recode['i'] + ".jpg"

        if jsons[1] == 'index':
            target = '精选'
        elif jsons[1] == 'people':
            target = '人物'
        elif jsons[1] == 'anime':
            target = '二次元'

        yield {
            'type': target,
            'img_url': img_url,
            'title': recode['i']
        }


# 下载壁纸
def write_img(item):
    if not os.path.exists('./bizhiLibs'):
        os.mkdir('./bizhiLibs')
    img = requests.get(item['img_url'])
    name = "static/{}/{}.jpg".format(item['type'], item['title'])
    img_path = 'bizhiLibs/' + name
    with open(img_path, 'wb') as f:

        f.write(img.content)

        print("{}-{} ok".format(item['type'], item['title']))


# 一只爬虫的工作流程
def worker():
    types = ['index', 'people', 'anime']

    for type in types:
        if type == 'index':
            while not indexQueue.empty():
                i = indexQueue.get()
                jsons = get_one_page(i, type)
                for item in get_img_url(jsons):
                    # 延时操作，一张图片停半秒
                    time.sleep(0.5)
                    write_img(item)
                print(jsons)
        elif type == 'people':
            while not peopleQueue.empty():
                i = peopleQueue.get()
                jsons = get_one_page(i, type)
                for item in get_img_url(jsons):
                    # 延时操作，一张图片停半秒
                    time.sleep(0.5)
                    write_img(item)
                print(jsons)
        elif type == 'anime':
            while not animeQueue.empty():
                i = animeQueue.get()
                jsons = get_one_page(i, type)
                for item in get_img_url(jsons):
                    # 延时操作，一张图片停半秒
                    time.sleep(0.5)
                    write_img(item)
                print(jsons)


# 线程爬虫
# run()：启动线程时自行调用
class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, func):
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.func = func

    def run(self):
        print("Start:", self.threadName)
        self.func()
        print("End:", self.threadName)


def main():
    threadcrawl = ['爬虫一号', '爬虫二号', '爬虫三号', '爬虫四号', '爬虫五号']
    threadlist = []


    # 开始线程爬虫
    for threadName in threadcrawl:
        thread = ThreadCrawl(threadName, worker)
        thread.start()
        threadlist.append(thread)

    # 关闭线程爬虫
    for thread in threadlist:
        thread.join()


if __name__ == '__main__':
    start = time.time()

    '''
    这里没有全爬而是每种类型爬5页，每页有120张壁纸
    1：没有可用的代理IP，可能会封IP
    2：不要给网站带来太多负担
    3：运行时间过长
'''
# 入队
indexQueue = Queue()  # 最多779页
for i in range(1, 6):
    indexQueue.put(i)
peopleQueue = Queue()
for i in range(1, 6):  # 最多327页
    peopleQueue.put(i)
animeQueue = Queue()
for i in range(1, 6):  # 最多165页
    animeQueue.put(i)

main()
end = time.time()

print("用时：", end - start)
print("OK!")