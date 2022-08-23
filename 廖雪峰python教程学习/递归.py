#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-19 17:09:50
@LastEditTime: 2022-08-19 18:15:48
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\递归.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 递归函数
'''


def fact_v1(n):
    '''
    @description: 阶乘
    @param  n: 
    @return 
    '''
    if n == 1:
        return 1
    return n * fact(n - 1)


def fact(n):
    return fact_iter(n, 1)


def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)


print(fact_v1(5))


def move(n, a, b, c):
    '''
    @description: 汉诺塔的移动可以用递归函数非常简单地实现。请编写move(n, a, b, c)函数，它接收参数n，表示3个柱子A、B、C中第1个柱子A的盘子数量，然后打印出把所有盘子从A借助B移动到C的方法，例如：
    # move(3, 'A', 'B', 'C')期待输出:
    # A --> C
    # A --> B
    # C --> B
    # A --> C
    # B --> A
    # B --> C
    # A --> C
    '''
    if n == 1:
        print(a, '-->', c)
    elif n > 1:
        move(n - 1, a, c, b)
        print(a, '-->', c)
        move(n - 1, b, a, c)


move(3, 'A', 'B', 'C')
