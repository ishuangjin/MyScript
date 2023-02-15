#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 10:33:50
@LastEditTime: 2022-12-15 15:25:00
@FilePath: \\Github\\MyScript\\nmon\\model\\RConfig.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import configparser
import os
import sys

from model.NmonLog import log
from model.NmonException import NmonException


class Config(object):

    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_path, '../config/config.ini')
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file, encoding="utf-8")
        # if os.path.exists(r"D:\Github\MyScript\nmon_auto\nmon\config\config.ini"):
        #     self.conf.read(r"D:\Github\MyScript\nmon_auto\nmon\config\config.ini", encoding="utf-8-sig")
        # else:
        #     raise NmonException("配置文件不存在")

    def reload_all_value(self):
        sections = self.conf.sections()
        for section in sections:
            items = self.conf.items(section)
            for item in items:
                self.__setattr__(item[0], item[1])