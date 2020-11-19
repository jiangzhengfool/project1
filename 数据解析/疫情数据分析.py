#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 13:02
# @Author  : huni
# @File    : 疫情数据分析.py
# @Software: PyCharm

import requests
import sqlite3


def getData(url):
    headers = {
        'Referer': 'https://news.qq.com/zt2020/page/feiyan.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    data = {
        'modules': 'chinaDayList, chinaDayAddList, cityStatis, nowConfirmStatis, provinceCompare'
    }
    #这里url请求是post数据
    response = requests.post(url=url,headers=headers,data=data)
    print(response.status_code)

    dic_obj = response.json()

    all_info_list = []

    for i in dic_obj['data']['chinaDayList']:
        j = []
        for key,value in sorted(i.items()):     #这里把字典按key重新进行排序，以便方便插入数据库中

            j.append(value)
        all_info_list.append(j)
    return all_info_list


#数据保存到数据库
def saveDatadb(dbpath,all_info_list):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in all_info_list:
        for index in range(len(data)):
            data[index] = '"'+str(data[index])+'"'
        sql = '''
                replace into 疫情数据表 (
                确诊病例,日期,累计死亡,死亡率,累计治愈,治愈率,境外输入病例,无症状感染者,现有确诊,危险病例,疑似病例) 
                values(%s)'''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


#初始化数据库，创建表
def init_db(dbpath):
    sql = '''
        create table if not exists 疫情数据表
        (
        id integer primary key autoincrement,
        确诊病例 numeric ,
        日期 varchar unique ,
        累计死亡 numeric ,
        死亡率 varchar,
        累计治愈 numeric ,
        治愈率 varchar ,
        境外输入病例 numeric ,
        无症状感染者 numeric ,
        现有确诊 numeric ,
        危险病例 numeric ,
        疑似病例 numeric 
        )

    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def main():

    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare'
    all_info_list = getData(url)
    dbpath = '疫情历史数据.db'
    saveDatadb(dbpath,all_info_list)

if __name__ == '__main__':
    main()
    print('保存成功')































