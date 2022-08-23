#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-23 10:16:58
@LastEditTime: 2022-08-23 10:49:17
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\迭代.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 请使用迭代查找一个list中最小和最大值，并返回一个tuple：
'''
from collections.abc import Iterable


def findMinAndMax(L):
    if isinstance(L, Iterable) and L:
        mix = L[0]
        max = L[0]
        for value in L:
            if mix >= value:
                mix = value
            if max <= value:
                max = value
        return (mix, max)
    else:
        return (None, None)


# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
