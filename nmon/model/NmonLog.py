#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 10:35:01
@LastEditTime: 2022-12-15 14:15:27
@FilePath: \\Github\\MyScript\\nmon\\model\\NmonLog.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 日志输出
@Reference_link：Python实用教程系列——Logging日志模块：https://zhuanlan.zhihu.com/p/166671955
'''
import logging
from logging.handlers import RotatingFileHandler


def get_log():

    # 应用程序入口，创建名为 "nmon_analyse" 的默认 Logger（日志器）
    logger = logging.Logger("nmon_analyse")

    # 创建日志记录器（处理器）
    handler_std = logging.StreamHandler()  # 日志发送到命令行
    # 日志保存到文件
    # handler_log = logging.FileHandler(filename="nmon_error.log", encoding="utf-8")  # 单文件，大小无限增长

    # 指明日志保存的路径，每个日志文件的最大值，保存的日志文件个数上限
    handler_log = RotatingFileHandler("log.txt", maxBytes=1024 * 1024, backupCount=1)

    # 设置日志等级
    # DEBUG < INFO < WARING <ERROR < CRITICAL
    logger.setLevel(logging.DEBUG)
    handler_std.setLevel(logging.INFO)
    handler_log.setLevel(logging.ERROR)

    # 创建日志记录的格式（格式器）
    formatter = logging.Formatter("%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # 为创建的日志记录器设置日志记录格式
    handler_std.setFormatter(formatter)
    handler_log.setFormatter(formatter)

    # 为全局的日志工具对象添加日志记录器
    logger.addHandler(handler_std)
    logger.addHandler(handler_log)
    return logger


log = get_log()
