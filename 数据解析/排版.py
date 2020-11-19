#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/15 11:06
# @Author  : huni
# @File    : 排版.py
# @Software: PyCharm

# coding=gbk
filename = './三国演义.txt'
line1 = "    "
with open(filename, 'r', encoding='UTF-8') as file_object:
    lines = file_object.readlines()
for line in lines:  # lines[0:10]:
    line = line.strip()
    # print(line.strip())
    if len(line) == 0:
        pass
    else:
        if line[-1:] == "。" or line[-1:] == "”":
            line = line + "\n    "
        # print (line[-4:-1],"***",line[-4:-1],"***")
        if line[0] == "”":
            if line1[-4:-1] == "    "[-4:-1]:
                line1 = line1[:-5] + "”\n    "

            else:
                line1 = line1 + "”"
            line = line[1:]
        line1 = line1 + line
# print(line1)


filename1 = './排版之后的三国.txt'
with open(filename1, 'w', encoding='UTF-8') as file_object:
    file_object.write(line1)
# for line in lines:
# print(line.rstrip())



