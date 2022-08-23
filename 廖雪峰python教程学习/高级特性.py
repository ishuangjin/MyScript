#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-19 18:18:57
@LastEditTime: 2022-08-19 18:19:00
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\高级特性.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 构造一个1, 3, 5, 7, ..., 99的列表，可以通过循环实现
'''

list1 = []
for i in range(0, 100):
    if i % 2 == 1:
        list1.append(i)

list2 = list(range(1, 100, 2))

list3 = list(range(1, 100)[::2])

list4 = list(range(1, 100))[::2]

print(list1, list2, list3, list4)
