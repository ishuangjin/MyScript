#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-09-21 18:22:23
@LastEditTime: 2022-09-27 17:10:55
@FilePath: \\Github\\MyScript\\test.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''


def ff(a, *b, **c):
    print(a)
    print(bool(b))
    print(bool(c))


# ff(1232,4,5,6,7,8,ss="sadf",xx="fff",ww="asdf")

if __name__ == '__main__':
    ff(1)
