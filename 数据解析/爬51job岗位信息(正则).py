#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 15:14
# @Author  : Huni
# @File    : 爬51job岗位信息(正则).py
# @Software: PyCharm

import requests
import re
import xlwt
from urllib import parse

#主函数
def main():
    savepath = "51.xls"     #定义保存路径

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('51job岗位信息', cell_overwrite_ok=True)  # 创建工作表

    # 关键字二次转译
    kw = input("请输入你要搜索的岗位关键字：")
    keyword = parse.quote(parse.quote(kw))
    pageNum = 0

    for i1 in range(0, 3):      #爬取前三页
        pageNum += 1

        url = "https://search.51job.com/list/000000,000000,0000,00,9,99," + keyword + ",2," + str(pageNum) + ".html"
        page_text = getUrl(url)
        all_list = getDate(page_text)
        if len(all_list[0]) == 0:
            print('没有搜索到职位信息')
            break
        else:
            print('正在爬取第%d页'%pageNum)
            saveDate(sheet,all_list,pageNum,book,savepath,searchNum=len(all_list[0]))

#获取一个列表页
def getUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    #使用通用爬虫对url进行一页进行爬取
    page_text = requests.get(url=url,headers=headers).text       #一页源码用text
    # print(page_text)

    return page_text

#获取列表页的所有岗位信息
def getDate(page_text):

    #正则表达式提取岗位信息
    jobHref = '"job_href":"(.*?)"'              #岗位链接
    jobName = '"job_name":"(.*?)"'              #岗位名称
    comHref = '"company_href":"(.*?)"'          #公司链接
    comName = '"company_name":"(.*?)"'          #公司名称
    salary = '"providesalary_text":"(.*?)"'     #薪资水平
    companytype = '"companytype_text":"(.*?)"'  #公司类型
    attribute = '"attribute_text":\[(.*?)\]'    #招聘条件
    workarea = '"workarea_text":"(.*?)"'        #工作地点
    companysize = '"companysize_text":"(.*?)"'  #公司规模
    companyind = '"companyind_text":"(.*?)"'    #主要业务
    jobwelf = '"jobwelf":"(.*?)"'               #福利待遇

    # 第一个参数是规则，第二个参数是被检索内容，第三个参数re.S是单行匹配
    jobHref_list = re.findall(jobHref,page_text,re.S)
    jobName_list = re.findall(jobName,page_text,re.S)
    comHref_list= re.findall(comHref,page_text,re.S)
    comName_list = re.findall(comName,page_text,re.S)
    salary_list = re.findall(salary,page_text,re.S)
    companytype_list = re.findall(companytype,page_text,re.S)
    attribute_list = re.findall(attribute,page_text,re.S)
    workarea_list = re.findall(workarea,page_text,re.S)
    companysize_list = re.findall(companysize,page_text,re.S)
    companyind_list = re.findall(companyind,page_text,re.S)
    jobwelf_list = re.findall(jobwelf,page_text,re.S)

    searchNum = len(jobHref_list)
    # print(jobName_list)
    # print(comHref_list)
    # print(comName_list)
    # print(salary_list)
    # print(companytype_list)
    # print(attribute_list)
    # print(workarea_list)
    # print(companysize_list)
    # print(companyind_list)
    # print(jobwelf_list)

    all_list = [jobHref_list, jobName_list, comHref_list, comName_list, salary_list,
                companytype_list, attribute_list, workarea_list, companysize_list,
                companyind_list, jobwelf_list]

    return all_list

#储存到excel表格中
def saveDate(sheet,all_list,pageNum,book,savepath,searchNum):
    col = ("岗位链接","岗位名称","公司链接","公司名称","薪资水平","公司类型","招聘条件","工作地点",'公司规模','主要业务','福利待遇')
    for i2 in range(0,11):
        sheet.write(0,i2,col[i2]) #列名
    for i3 in range(0,searchNum):
        b = (all_list[0])[i3]
        c = (all_list[1])[i3]
        d = (all_list[2])[i3]
        e = (all_list[3])[i3]
        f = (all_list[4])[i3]
        g = (all_list[5])[i3]
        h = (all_list[6])[i3]
        j = (all_list[7])[i3]
        k = (all_list[8])[i3]
        l = (all_list[9])[i3]
        m = (all_list[10])[i3]

        if pageNum >= 1 and searchNum <= 50:
            print("第%d条输入完成" % ((pageNum - 1) * 50 + (i3 + 1)))
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 0, b)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 1, c)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 2, d)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 3, e)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 4, f)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 5, g)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 6, h)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 7, j)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 8, k)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 9, l)
            sheet.write((pageNum - 1) * 50 + (i3 + 1), 10, m)
        elif pageNum == 1 and searchNum < 50:
            print("第%d条输入完成" % (i3 + 1))
            sheet.write((i3 + 1), 0, b)
            sheet.write((i3 + 1), 1, c)
            sheet.write((i3 + 1), 2, d)
            sheet.write((i3 + 1), 3, e)
            sheet.write((i3 + 1), 4, f)
            sheet.write((i3 + 1), 5, g)
            sheet.write((i3 + 1), 6, h)
            sheet.write((i3 + 1), 7, j)
            sheet.write((i3 + 1), 8, k)
            sheet.write((i3 + 1), 9, l)
            sheet.write((i3 + 1), 10, m)

    book.save(savepath)

if __name__ == '__main__':
    main()
    print('爬取完成')

