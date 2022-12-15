#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-30 09:57:37
@LastEditTime: 2022-12-15 14:10:54
@FilePath: \\Github\\MyScript\\nmon\\nmon_analyse.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''

from model import ExcelMicro
from model import NmonResult
from model import RConfig
from model import SSHSokcet
from model.NmonLog import log
from model.NmonException import NmonException
# import time
import traceback
import os


def get_all_nmon_file(path):
    if os.path.isfile(path):
        extend = path.rsplit(".", 1)
        if (len(extend) == 2):
            if extend[1] == "nmon":
                file_list.append(path)

    elif os.path.isdir(path):
        for file in os.listdir(path):
            get_all_nmon_file(path + "\\" + file)


def analyse_file(config):
    MircoFilePath = config.nmon_analyse_file
    get_all_nmon_file(config.nmon_file_dir)
    nmon_tuple = file_list
    # path = config.nmon_result_file
    path = ""
    log.info("开始解析文件")
    result = ExcelMicro.get_nmon_result_file(MircoFilePath, nmon_tuple, path)
    log.info(result)
    log.info("解析文件结束")
    log.info("开始提取数据")
    nr = NmonResult.NmonResult(result)
    log.info("数据提取完成")
    nr.get_file(path=path)


def download_file(config):
    log.info("读取配置文件")
    localPath = config.local_dir
    hostname_list = config.hostname.replace('\n', '').strip('[]').split(',')
    for hostname in hostname_list:
        remotePath = config.remote_dir
        uesrname = config.username
        password = config.password

        ssh = SSHSokcet.sshSocket(hostname=hostname, username=uesrname, password=password)
        files = ssh.get_all_file(remotePath, remotePath, [])
        ssh.download_file(files, localPath, remotePath)
        ssh.close()


try:
    file_list = []
    config = RConfig.Config()
    config.reload_all_value()
    download_flag = config.download_flag
    if download_flag == 'True':
        download_file(config=config)
    elif download_flag != 'False':
        raise NmonException("无法识别的下载标识")

    analyse_file(config=config)
except Exception:
    error_msg = traceback.format_exc()
    log.error(error_msg)
    # time.sleep(1)
    # input("按任意键退出程序:")
