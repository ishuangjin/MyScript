#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-19 15:40:43
@LastEditTime: 2022-08-19 16:57:12
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\函数.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''


def my_abs(x):
    '''
    @description: 异常处理
    @param  x: 
    @return 
    '''
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


def mul(*args):
    '''
    @description: 以下函数允许计算两个数的乘积，请稍加改造，变成可接收一个或多个数并计算乘积：
    @param array args: 
    @return 
    '''
    if len(args):
        result = 1
        for num in args:
            if isinstance(num, (int, float)):
                result *= num
            else:
                raise TypeError("不是整数或浮点数")
    else:
        raise TypeError("输入的数小于1个")
    return result


if __name__ == '__main__':
    # x = input("输入一个数字：")
    # x = 'm'
    # print(my_abs(x))

    print('mul(5) =', mul(5))
    print('mul(5, 6) =', mul(5, 6))
    print('mul(5, 6, 7) =', mul(5, 6, 7))
    print('mul(5, 6, 7, 9) =', mul(5, 6, 7, 9))
    if mul(5) != 5:
        print('测试失败!')
    elif mul(5, 6) != 30:
        print('测试失败!')
    elif mul(5, 6, 7) != 210:
        print('测试失败!')
    elif mul(5, 6, 7, 9) != 1890:
        print('测试失败!')
    else:
        try:
            mul()
            print('测试失败!')
        except TypeError:
            print('测试成功!')
