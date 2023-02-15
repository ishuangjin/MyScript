#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2023-02-13 11:23:10
@LastEditTime: 2023-02-13 14:51:53
@FilePath: \\Github\\MyScript\\baidu翻译api\\config\\env_init.py
@Copyright (c) 2023 by ${git_name}, All Rights Reserved.
@Description:
'''
import os
import sys

# 获取程序主目录
config_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.dirname(config_path)
mod_path = os.path.join(main_path, "mods")
sys.path.insert(0, mod_path)
sys.path.insert(0, main_path)

from config import Config

# 获取配置文件路径
ini_path = os.path.join(main_path, "config\\config.ini")
# print(ini_path)

# 获取配置文件中的配置信息
parser_dict = Config.ConfigParser(ini_path).get_all_parser()
# print(parser_dict)
