#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 10:01
# @Author  : huni
# @File    : 爬三国演义.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import Zstring


if __name__ == '__main__':
    #获取列表页
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = requests.get(url=url,headers=headers).text  #.text

    #解析详情页
    #1.实例化BeautifulSoup对象
    #这个地方有错，web在这里是一个response对象，无法用BeautifulSoup解析，如果要解析，解析对象应该是web.content
    #或者可以在page_text后面加.text转化成文本
    soup = BeautifulSoup(page_text,'lxml')

    #解析章节标题和详情页的url
    #使用层级定位
    li_list = soup.select('.book-mulu > ul > li')
    # print(li_list)

    with open('./三国演义.txt','w',encoding='utf-8') as fp:

        #分别把a标签中的url和标题遍历出来
        for li in li_list:
            title = li.a.string
            detail_url = 'https://www.shicimingju.com' + li.a['href']

            #对详情页发请求，解析出章节内容
            detail_page_text = requests.get(url=detail_url,headers=headers).text

            #解析出详情页的相关内容
            detail_soup = BeautifulSoup(detail_page_text,'lxml')
            div_tag = detail_soup.find('div',class_='chapter_content').text

            div_tag = div_tag.replace(' ', '')
            div_tag = div_tag.replace(' ', '')

            content = Zstring.String(div_tag)
            mudul = content.paragraph(50,first_line=8)

            fp.write(title + ':' + str(mudul) + '\n')
            print(title,'爬取成功')





