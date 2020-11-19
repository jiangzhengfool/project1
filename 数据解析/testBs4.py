#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 16:09
# @Author  : huni
# @File    : testBs4.py
# @Software: PyCharm

from bs4 import BeautifulSoup

def main():
    #将本地html文档加载到该对象中
    with open('./baidu.html','r',encoding='utf-8') as fp:
        bs = BeautifulSoup(fp,'lxml')
        # print(bs)
        # print(bs.find('div',class_="head_wrapper"))
        print(bs.select(".head_wrapper > div > a")[0])







if __name__ == '__main__':
    main()