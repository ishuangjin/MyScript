#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-09 17:55:25
@LastEditTime: 2022-08-09 18:13:18
@FilePath: \\Github\\MyScript\\test.py
@Description: 小明的成绩从去年的72分提升到了今年的85分，请计算小明成绩提升的百分点，并用字符串格式化显示出'xx.x%'，只保留小数点后1位：
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
'''
last_year_score = 72
this_year_score = 85
percentage_point = (this_year_score - last_year_score) * 100 / last_year_score
print(f"提升了{percentage_point:.1f}%")
