#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-30 09:57:23
@LastEditTime: 2022-12-09 11:26:01
@FilePath: \\Git\\MyScript\\tct压测\\nmon\\RConfig.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
# -*- coding:utf-8 -*-
import configparser
import os
import sys

from nmon.NmonLog import log
from nmon.NmonException import NmonException


class Config(object):

    def __init__(self):
        self.conf = configparser.ConfigParser()
        if os.path.exists(r"F:\Git\MyScript\tct压测\nmon\config\config.ini"):
            self.conf.read(r"F:\Git\MyScript\tct压测\nmon\config\config.ini", encoding="utf-8-sig")
        else:
            raise NmonException("配置文件不存在")

    def reload_all_value(self):
        sections = self.conf.sections()
        for section in sections:
            items = self.conf.items(section)
            for item in items:
                self.__setattr__(item[0], item[1])
