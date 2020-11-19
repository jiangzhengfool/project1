#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 10:33
# @Author  : Tony
# @File    : testRe网页采集器.py
# @Software: PyCharm

import requests
import json

def main():

    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome'
    }

    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'   # url中 ？后面的参数都可以做动态请求，可以封装进字典

    id_list = []  # 创建一个储存id的列表

    for page in range(1,6):
        page = str(page)

        #处理url携带的参数，封装到字典中
        data = {
            'on': 'true',
            'page': page,
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyname': ''
        }

        #对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
        # json方法返回的是一个列表对象（如果确认服务器相应的类型是json，才能使用json方法）
        # 返回的对象类型在response里面看

        #获取企业id的json信息
        id_json = requests.post(url=url,data=data,headers=headers).json()

        #保存企业ID的json数据
        # fileName = 'id.json'
        # with open(fileName,'w',encoding='utf-8') as fp:
        #     json.dump(id_json,fp=fp,ensure_ascii=False)
        # print(fileName,'保存成功!')



        for dic in id_json['list']:     #从id的json字典中取出list对相应的value值进行遍历
            id_list.append(dic['ID'])   #遍历出来的id存放在列表中
        # print(id_list)


    #对得到的企业id的url进行解析
    id_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'

    #此次参数为上面遍历出来的id
    for i in id_list:
        data1 = {
            'id':i
        }

        # 获取企业信息的json信息
        info_json = requests.post(url=id_url, data=data1, headers=headers).json()

        #保存企业信息的json数据
        fileName = 'info.json'
        with open(fileName,'a',encoding='utf-8') as fp:
            json.dump(info_json,fp=fp,ensure_ascii=False)
    print(fileName,'保存成功!')





if __name__ == '__main__':
    main()