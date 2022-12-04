#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-30 09:55:33
@LastEditTime: 2022-11-30 09:56:34
@FilePath: \\Git\\MyScript\\tct压测\\nmon\\NmonLog.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
# -*- coding:utf-8 -*-

# create: 2019-07-29
# author:zengln
# desc: 日志输出

import logging


def get_log():
    logger = logging.Logger("nmon_analyse")
    handler_std = logging.StreamHandler()
    handler_log = logging.FileHandler(filename="error.log", encoding="utf-8")

    logger.setLevel(logging.DEBUG)
    handler_std.setLevel(logging.INFO)
    handler_log.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler_std.setFormatter(formatter)
    handler_log.setFormatter(formatter)

    logger.addHandler(handler_std)
    logger.addHandler(handler_log)
    return logger


log = get_log()
