#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-19 18:43:48
@LastEditTime: 2022-08-23 10:01:03
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\切片.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 利用切片操作，实现一个trim()函数，去除字符串首尾的空格，注意不要调用str的strip()方法：
'''


def trim(s):
    if isinstance(s, str):
        while s[:1] == " ":
            s = s[1:]
        while s[-1:] == " ":
            s = s[:-1]
    else:
        raise ("非字符串")
    return s


# 测试:
if trim('hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')
