#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-19 13:52:44
@LastEditTime: 2022-08-19 14:03:29
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\条件判断.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
小明身高1.75，体重80.5kg。请根据BMI公式（体重除以身高的平方）帮小明计算他的BMI指数，并根据BMI指数：
低于18.5：过轻
18.5-25：正常
25-28：过重
28-32：肥胖
高于32：严重肥胖
'''

height = 1.73
weight = 60
bmi = weight / (height**2)
if bmi < 18.5:
    print("过轻")
elif 18.5 <= bmi < 25:
    print("正常")
elif 25 <= bmi < 28:
    print("过重")
elif 28 <= bmi < 32:
    print("肥胖")
elif 32 <= bmi:
    print("严重肥胖")
