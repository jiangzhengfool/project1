#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 8:21
# @Author  : huni
# @File    : 大学排名.py
# @Software: PyCharm

import requests
from lxml import etree
import sqlite3


#获取数据解析数据，因为爬取的量不大所以就写在一个函数中
def getData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    page_text = requests.get(url=url,headers=headers)
    print(page_text.status_code)

    #解决爬取过程中编码解码问题 下面两种方式都适用
    r = page_text.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(page_text.text)[0])

    # page_text1 = page_text.text.encode('ISO-8859-1', 'ignore')
    #
    tree = etree.HTML(r)

    tr_list = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr')

    #用于保存所有的信息的列表
    all_info_list = []

    #遍历所有的排名信息
    for tr in tr_list:
        #遍历所有的排名数量
        for i in range(len(tr_list) + 1):
            #每个大学信息保存在单独的列表中
            i = []
        rank = tr.xpath('./td[1]/text()')[0]    #大学排名
        name = tr.xpath('./td[2]/a/text()')[0]  #大学名称
        situ = tr.xpath('./td[3]/text()')[0]    #地理位置
        type = tr.xpath('./td[4]/text()')[0]    #办学类型
        scor = tr.xpath('./td[5]/text()')[0]    #学校评分

        ##每个大学信息保存在单独的列表中
        i.append(rank)
        i.append(name)
        i.append(situ)
        i.append(type)
        i.append(scor)
        #再把每个大学的信息都存放下大列表中
        all_info_list.append(i)
    return all_info_list

#数据保存到数据库
def saveDatadb(dbpath,all_info_list):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in all_info_list:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'
        sql = '''
                insert into rankings (
                rank,cname,situ,types,score) 
                values(%s)'''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()



#初始化数据库，创建表
def init_db(dbpath):
    sql = '''
        create table  rankings
        (
        id integer primary key autoincrement,
        rank numeric ,
        cname varchar ,
        situ varchar,
        types varchar,
        score numeric
        )

    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def main():
    url = 'http://www.shanghairanking.cn/rankings/bcur/2020'
    all_info_list = getData(url)
    dbpath = '大学排名.db'
    saveDatadb(dbpath,all_info_list)

if __name__ == '__main__':
    main()
    print('保存成功')
