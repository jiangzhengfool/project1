#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/13 21:06
# @Author  : huni
# @File    : github上的彼岸图.py
# @Software: PyCharm

import json
import os
import random
import sys
from concurrent.futures.thread import ThreadPoolExecutor

import pymysql
from lxml import etree
from requests import *


class Spider:
    def __init__(self):
        self.cookies = self.readCookies()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
        self.indexUrl = "http://pic.netbian.com"
        self.catelogue = self.getCatalogue()
        # 每天限量只能下载200张
        self.downCount = 0
        self.ddir = 'D:\\Data\\照片\\彼岸图网\\'

    def readCookies(self):
        cookies = {}
        with open("cookie.txt", "r", encoding="utf-8") as f:
            while True:
                c = f.readline()
                if c is not None:
                    c = c.strip()
                    if len(c) == 0:
                        break
                    else:
                        c = c.split("=")
                        cookies[c[0]] = c[1]
                else:
                    break
        return cookies

    def reqGet(self, url):
        html = get(url, headers=self.headers, cookies=self.cookies).content.decode("gbk")
        return html

    def getImg(self, url):
        return get(url, headers=self.headers, cookies=self.cookies)

    def getCatalogue(self):
        index = self.reqGet(self.indexUrl)
        h = etree.HTML(index)
        href = h.xpath('//div[@class="classify clearfix"]/a/@href')
        title = h.xpath('//div[@class="classify clearfix"]/a/text()')
        return zip(title, href)

    def getRealUrl(self, href):
        """
        ('阿尔卑斯山风景4k高清壁纸3840x2160', 'http://pic.netbian.com/downpic.php?id=21953&classid=53')
        """
        dh = self.reqGet(self.indexUrl + href)
        h = etree.HTML(dh)
        dataId = h.xpath('//div[@class="downpic"]/a/@data-id')[0]
        title = h.xpath('//div[@class="photo-hd"]/h1/text()')[0]
        url = "{0}/e/extend/downpic.php?id={1}&t={2}".format(self.indexUrl, dataId, random.random())
        msg = self.reqGet(url)
        return title, self.indexUrl + json.loads(msg)['pic']

    def getPicUrls(self, url=None, html=None):
        if html is None:
            html = self.reqGet(url)
        h = etree.HTML(html)
        hrefs = h.xpath('//ul[@class="clearfix"]/li/a/@href')
        realHrefs = []
        for href in hrefs:
            realHrefs.append(self.getRealUrl(href))
        return realHrefs

    def getMaxPage(self, html):
        h = etree.HTML(html)
        pages = h.xpath('//div[@class="page"]/a/text()')
        return int(pages[-2].strip())

    def saveToDB(self, category, v, i):
        url = "%s%sindex_%d.html" % (self.indexUrl, v, i)
        if i == 1:
            url = "%s%sindex.html" % (self.indexUrl, v)
        nus = self.getPicUrls(url=url)
        for nu in nus:
            self.add(category, nu[0], nu[1])

    def savePicInfoToDB(self):
        executor = ThreadPoolExecutor(max_workers=64)
        for c, v in self.catelogue:
            html = self.reqGet(self.indexUrl + v)
            if not os.path.exists("%s%s" % (self.ddir, c)):
                os.mkdir("%s%s" % (self.ddir, c))
            print("%s%s" % (self.ddir, c))
            maxPage = self.getMaxPage(html)
            for i in range(1, maxPage + 1):
                executor.submit(self.saveToDB, c, v, i)
        executor.shutdown(wait=True)

    def getConn(self):
        conn = pymysql.Connect(
            host="127.0.0.1",
            port=3306,
            charset='utf8',
            user='root',
            password='toor',
            db='photos'
        )
        return conn

    def add(self, category, filename, url):
        try:
            conn = self.getConn()
            cursor = conn.cursor()
            sql = "INSERT INTO purl VALUES ('{0}', '{1}', '{2}')".format(category, filename, url)
            cursor.execute(sql)
            conn.commit()
            print(filename + " was added to database successfully")
        except:
            sys.stderr.write(filename + " was existed!\n")
        finally:
            cursor.close()
            conn.close()

    def downPic(self):
        executor = ThreadPoolExecutor(max_workers=32)
        sql = "select * from purl"
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for index in range(0, len(result)):
            if self.downCount > 200:
                print("finished today, welcome come back tomorrow!")
                break
            executor.submit(self.download, result[index])
        executor.shutdown(wait=True)
        cursor.close()
        conn.close()

    def download(self, cnu):
        path = "{0}{1}\{2}.jpg".format(self.ddir, cnu[0], cnu[1])
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            return
        print("download... " + path)
        rimg = self.getImg(cnu[2])
        if (rimg.status_code != 200 or len(rimg.content) <= 1024):
            print("invalid img!")
            return
        with open(path, "wb") as f:
            f.write(rimg.content)
            self.downCount += 1
        print("finished!!! " + path)

    def start(self):
        # self.savePicInfoToDB()
        self.downPic()


if __name__ == '__main__':
    spider = Spider()
    spider.start()