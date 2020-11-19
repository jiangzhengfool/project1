#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/13 21:33
# @Author  : huni
# @File    : CSDN上的彼岸图.py
# @Software: PyCharm

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os
import requests
from urllib.error import HTTPError
from urllib.error import URLError
url="http://www.netbian.com/"
tempList=[]

#避开URL错误
def get_page_(imageLink,fileName):
    try:
        urlretrieve(imageLink, filename=fileName)
    except URLError as e:
        return None
#解析网页
def openhtml(label,attrs,end,url,sortUrl,urlList,):
    html = url + sortUrl + end
    page = requests.get(html)
    bso = BeautifulSoup(page.content, "html.parser")
    #找到要获取的标签
    for item in bso.findAll(label):
        if attrs in item.attrs:
            urlList.append(item.attrs[attrs])
#获取图片链接，并创建文件夹
def downimage(imageUrl,imageName,filepath):
    try:
        for index in range(0, len(imageUrl)):
            #去掉图片链接中.htm方便自定义链接
            imageUrl[index] = imageUrl[index].replace(".htm", "")
            #获取图片名称
            openhtml("img", "title", f"{imageUrl[index]}.htm", url=url, sortUrl="", urlList=imageName)
            #拼接链接
            image = requests.get(url + imageUrl[index] + "-1920x1080.htm")
            #解析图片链接获取.JPG链接
            page = BeautifulSoup(image.content, "html.parser")
            imageLink=(page.find("td").find("img").get("src"))
            #拼接下载时保存的文件名
            fileName="{}{}{}".format(filepath,imageName[index],".jpg")
            #下载到本地
            get_page_(imageLink=imageLink, fileName=fileName)
            print(imageName[index])
    except:
        print("图片异常，爬取失败")
#主体函数，整体流程在这
def wallpaperDown(sortname,sorturl,page,type):
    #新建保存到本地的文件夹
    filepath = f"E:\\1080p壁纸\\{sortname}\\"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    urlList=[]
    #打开壁纸分类地址
    openhtml("a","href",".htm",urlList=urlList,url=url,sortUrl=sorturl)
    #筛选出需要网页的连接
    urlList=[list for list in urlList if list is not None and f"{sorturl}" in list ]
    linkLength=len(sorturl)
    #获取网站页数用于循环
    if urlList==[]:
        end=""
    else:
        end = urlList[-2][2+linkLength:-4]
    #循环N页，获取下载链接

    for i in range(page,int(end)+1):
        # 下载第一页，上面的循环只能从第二页开始下载。
        if i>=int(end):
            print("正在下载第1页")
            homeImageUrl = []
            homeImageName = []
            #打开第一页
            openhtml("a", "href", ".htm", url=url, sortUrl=sorturl, urlList=homeImageUrl)
            #筛选出图片链接
            homeImageUrl=[list for list in homeImageUrl if list is not None and "/desk/" in list]
            #下载图片
            downimage(imageUrl=homeImageUrl, imageName=homeImageName, filepath=filepath)

        #判断下载类型，单类别下载则下载完尾页之后结束，多类别则继续下载其他类别
        if i >= int(end):
            if type==0:
                print(f"正在下载第{i}页",i,end)
                print(f"{sortname}壁纸已下载完毕")
                exit()
        else:
            print(f"正在下载第{i}页")
            imageUrl = []
            imageName = []
            # 找到包含下载链接的标签，并获取内容
            openhtml("a", "href", f"_{i}.htm", url=url, sortUrl=sorturl, urlList=imageUrl)
            # 筛选出需要的图片链接
            imageUrl = [list for list in imageUrl if list is not None and "/desk/" in list]
            # 下载图片
            downimage(imageUrl=imageUrl, imageName=imageName, filepath=filepath)

