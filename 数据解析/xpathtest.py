#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 15:35
# @Author  : huni
# @File    : xpathtest.py
# @Software: PyCharm

from lxml import etree

if __name__ == '__main__':
    #实例化了一个etree对象，且将解析的源码加载到了该对象中
    tree = etree.parse('baidu.html',etree.HTMLParser())
    r = tree.xpath('//div[@class="head_wrapper"]/div[@id="u1"]/a[4]/@href')[0]
    print(r)