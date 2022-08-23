#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-23 10:56:11
@LastEditTime: 2022-08-23 10:56:14
@FilePath: \\Github\\MyScript\\廖雪峰python教程学习\\列表生成式.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 请修改列表生成式，通过添加if语句保证列表生成式能正确地执行：-->['hello', 'world', 'apple']
'''
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [value.lower() for value in L1 if isinstance(value, str)]

# 测试:
print(L2)
if L2 == ['hello', 'world', 'apple']:
    print('测试通过!')
else:
    print('测试失败!')